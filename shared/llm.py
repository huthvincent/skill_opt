"""Single gateway for ALL LLM calls in this project (CONSTITUTION section 4.2).

Backends, selected by LLM_BACKEND in .env:
  - "anthropic": direct Anthropic API (dev machine, smoke tests)
  - "bedrock":   AWS Bedrock Claude (large-scale experiment machine)
  - "copilot":   GitHub Copilot Chat API via litellm's github_copilot/ route
                 (acts as a Copilot IDE *client* on your GitHub entitlement;
                 no per-token USD, first call triggers device-flow login).
                 Model names differ from Anthropic - set MODEL_* to Copilot
                 model ids (e.g. gpt-4o, claude-sonnet-4); the "github_copilot/"
                 prefix is added here.

Experiment scripts must never import anthropic/boto3 directly - they call
chat() below, so switching machines is a .env change, zero code change.

Also enforces the budget discipline of CONSTITUTION section 6: every call is
metered; when the tracker hits its cap, BudgetExceeded is raised so the run
stops instead of silently overspending.

Self-test:  uv run python -m shared.llm --selftest
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

from shared.paths import PROJECT_ROOT

load_dotenv(PROJECT_ROOT / ".env")

# USD per 1M tokens (input, output). Rough numbers for budget *guarding*, not
# accounting; update from the provider price page when models change.
PRICES_PER_MTOK: dict[str, tuple[float, float]] = {
    "claude-fable-5": (20.0, 100.0),
    "claude-opus-4-8": (15.0, 75.0),
    "claude-sonnet-5": (3.0, 15.0),
    "claude-haiku-4-5-20251001": (1.0, 5.0),
}
_DEFAULT_PRICE = (20.0, 100.0)  # unknown model -> assume expensive (pessimistic)


class BudgetExceeded(RuntimeError):
    pass


@dataclass
class CostTracker:
    """Accumulates estimated USD cost across calls; raises at the cap."""

    max_cost_usd: float | None = None
    spent_usd: float = 0.0
    calls: int = 0
    by_model: dict = field(default_factory=dict)
    tokens_in: int = 0
    tokens_out: int = 0

    def add(self, model: str, in_tok: int, out_tok: int) -> None:
        p_in, p_out = PRICES_PER_MTOK.get(model, _DEFAULT_PRICE)
        cost = in_tok * p_in / 1e6 + out_tok * p_out / 1e6
        self.spent_usd += cost
        self.calls += 1
        self.tokens_in += in_tok
        self.tokens_out += out_tok
        self.by_model[model] = self.by_model.get(model, 0.0) + cost
        if self.max_cost_usd is not None and self.spent_usd >= self.max_cost_usd:
            raise BudgetExceeded(
                f"budget cap hit: spent ~${self.spent_usd:.2f} >= ${self.max_cost_usd:.2f}"
            )

    def add_flat(self, model: str, in_tok: int, out_tok: int) -> None:
        """Flat-rate backend (Copilot subscription): no marginal USD, so we
        meter tokens + call count only. Budget discipline for this backend is
        request-count / rate-limit based, not USD (CONSTITUTION section 6)."""
        self.calls += 1
        self.tokens_in += in_tok
        self.tokens_out += out_tok
        self.by_model[model] = self.by_model.get(model, 0.0) + 0.0


def _client():
    backend = os.environ.get("LLM_BACKEND", "anthropic").lower()
    if backend == "bedrock":
        from anthropic import AnthropicBedrock

        return AnthropicBedrock(aws_region=os.environ.get("AWS_REGION", "us-west-2"))
    from anthropic import Anthropic

    return Anthropic()


def _mock_chat(prompt: str, model: str, tracker: CostTracker | None) -> str:
    """LLM_BACKEND=mock: zero-cost canned reply for offline pipeline tests."""
    if tracker is not None:
        tracker.add(model, in_tok=0, out_tok=0)
    return f"[mock reply to {len(prompt)} chars]"


def _copilot_chat(
    prompt: str,
    *,
    system: str | None,
    model: str,
    max_tokens: int,
    temperature: float | None,
    tracker: CostTracker | None,
) -> str:
    """LLM_BACKEND=copilot: call GitHub Copilot's Chat API via litellm.

    litellm's github_copilot/ route acts as a Copilot IDE client: on first use
    it runs the GitHub device-flow login (prints a URL + code), caches the
    token under ~/.config/litellm/github_copilot/, then posts to Copilot's
    endpoint. Inference runs on GitHub's servers, billed to your Copilot
    entitlement (no per-token USD)."""
    import litellm

    messages: list[dict] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    kwargs: dict = dict(
        model=f"github_copilot/{model}",
        messages=messages,
        max_tokens=max_tokens,
    )
    if temperature is not None:
        kwargs["temperature"] = temperature
    try:
        resp = litellm.completion(**kwargs)
    except Exception as e:  # some models reject temperature outright
        if "temperature" in kwargs and "temperature" in str(e).lower():
            kwargs.pop("temperature")
            resp = litellm.completion(**kwargs)
        else:
            raise
    if tracker is not None:
        u = getattr(resp, "usage", None)
        tracker.add_flat(
            model,
            int(getattr(u, "prompt_tokens", 0) or 0),
            int(getattr(u, "completion_tokens", 0) or 0),
        )
    text = resp.choices[0].message.content or ""
    if not text.strip():
        raise RuntimeError(
            f"empty text reply from copilot/{model} (usage="
            f"{getattr(resp, 'usage', None)}) - raise max_tokens or pick "
            f"another model")
    return text


def chat(
    prompt: str,
    *,
    system: str | None = None,
    model: str | None = None,
    role: str = "agent",  # agent | optimizer | judge -> picks MODEL_* default from .env
    max_tokens: int = 4096,
    temperature: float | None = None,
    tracker: CostTracker | None = None,
) -> str:
    """One user-turn completion. Returns the text of the reply."""
    model = model or os.environ.get(f"MODEL_{role.upper()}", "claude-sonnet-5")
    backend = os.environ.get("LLM_BACKEND", "anthropic").lower()
    if backend == "mock":
        return _mock_chat(prompt, model, tracker)
    if backend == "copilot":
        return _copilot_chat(
            prompt, system=system, model=model, max_tokens=max_tokens,
            temperature=temperature, tracker=tracker)
    kwargs: dict = dict(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    if temperature is not None:
        kwargs["temperature"] = temperature
    if system:
        kwargs["system"] = system
    try:
        resp = _client().messages.create(**kwargs)
    except Exception as e:  # some models (fable-5) reject temperature outright
        if "temperature" in kwargs and "temperature" in str(e):
            kwargs.pop("temperature")
            resp = _client().messages.create(**kwargs)
        else:
            raise
    if tracker is not None:
        tracker.add(model, resp.usage.input_tokens, resp.usage.output_tokens)
    text = "".join(block.text for block in resp.content if block.type == "text")
    if not text.strip():
        # never return empty silently - a reasoning model can burn the whole
        # max_tokens budget on thinking and emit zero text (bit us in Gate 1)
        raise RuntimeError(
            f"empty text reply from {model} (max_tokens={max_tokens} likely "
            f"consumed by reasoning; usage={resp.usage}) - raise max_tokens "
            f"or use a non-reasoning model for this role")
    return text


if __name__ == "__main__":
    import sys

    if "--selftest" in sys.argv:
        t = CostTracker(max_cost_usd=0.50)
        out = chat("Reply with exactly: OK", role="judge", max_tokens=16, tracker=t)
        print(f"backend={os.environ.get('LLM_BACKEND', 'anthropic')} reply={out!r} "
              f"cost~${t.spent_usd:.4f} ({t.calls} call)")
