"""Single gateway for ALL LLM calls in this project (CONSTITUTION section 4.2).

Backends, selected by LLM_BACKEND in .env:
  - "anthropic": direct Anthropic API (dev machine, smoke tests)
  - "bedrock":   AWS Bedrock Claude (large-scale experiment machine)

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

    def add(self, model: str, in_tok: int, out_tok: int) -> None:
        p_in, p_out = PRICES_PER_MTOK.get(model, _DEFAULT_PRICE)
        cost = in_tok * p_in / 1e6 + out_tok * p_out / 1e6
        self.spent_usd += cost
        self.calls += 1
        self.by_model[model] = self.by_model.get(model, 0.0) + cost
        if self.max_cost_usd is not None and self.spent_usd >= self.max_cost_usd:
            raise BudgetExceeded(
                f"budget cap hit: spent ~${self.spent_usd:.2f} >= ${self.max_cost_usd:.2f}"
            )


def _client():
    backend = os.environ.get("LLM_BACKEND", "anthropic").lower()
    if backend == "bedrock":
        from anthropic import AnthropicBedrock

        return AnthropicBedrock(aws_region=os.environ.get("AWS_REGION", "us-west-2"))
    from anthropic import Anthropic

    return Anthropic()


def chat(
    prompt: str,
    *,
    system: str | None = None,
    model: str | None = None,
    role: str = "agent",  # agent | optimizer | judge -> picks MODEL_* default from .env
    max_tokens: int = 4096,
    temperature: float = 1.0,
    tracker: CostTracker | None = None,
) -> str:
    """One user-turn completion. Returns the text of the reply."""
    model = model or os.environ.get(f"MODEL_{role.upper()}", "claude-sonnet-5")
    kwargs: dict = dict(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    if system:
        kwargs["system"] = system
    resp = _client().messages.create(**kwargs)
    if tracker is not None:
        tracker.add(model, resp.usage.input_tokens, resp.usage.output_tokens)
    return "".join(block.text for block in resp.content if block.type == "text")


if __name__ == "__main__":
    import sys

    if "--selftest" in sys.argv:
        t = CostTracker(max_cost_usd=0.50)
        out = chat("Reply with exactly: OK", role="judge", max_tokens=16, tracker=t)
        print(f"backend={os.environ.get('LLM_BACKEND', 'anthropic')} reply={out!r} "
              f"cost~${t.spent_usd:.4f} ({t.calls} call)")
