"""Runtime compatibility patches for tau2-bench. Upstream code stays untouched
(CONSTITUTION: never edit third_party); we patch module state in-process.

Usage (order matters - BEFORE importing tau2.cli):

    from shared.tau2_compat import apply_default_model_patches, set_policy_suffix
    apply_default_model_patches("anthropic/claude-haiku-4-5-20251001")
    from tau2.cli import main as tau2_main

Patch 1 (model defaults): tau2 hardcodes gpt-4.1 for the NL-assertions judge
and the env interface agent, with no CLI flag. Root-caused in E0.1 runs
smoke_tau2_20260705_044317 / _105714.

Patch 2 (lenient JSON): Claude judges wrap their JSON verdict in markdown
fences; upstream does a bare json.loads on the reply.

Patch 3 (policy suffix): append text (e.g. an experience library) to every
Environment.get_policy() result - this is how a library reaches the agent's
system prompt. tau2 records the patched policy into simulation.policy, so
every results.json remains self-documenting.
"""
from __future__ import annotations

import json
import sys


class _LenientJson:
    """json.loads that strips markdown fences / preamble before parsing."""

    @staticmethod
    def loads(s: str):
        import re

        s = s.strip()
        m = re.search(r"```(?:json)?\s*(.*?)```", s, re.DOTALL)
        if m:
            s = m.group(1).strip()
        if not s.startswith("{") and "{" in s:
            s = s[s.index("{"): s.rindex("}") + 1]
        return json.loads(s)

    def __getattr__(self, name):  # everything else -> real json module
        return getattr(json, name)


def apply_default_model_patches(model: str) -> None:
    """Repoint tau2's hardcoded gpt-4.1 defaults to `model`. Must run before
    tau2.environment.utils.interface_agent is imported (asserted)."""
    import tau2.config as cfg

    assert "tau2.environment.utils.interface_agent" not in sys.modules, \
        "interface_agent already imported - def-time default already bound to gpt-4.1"
    cfg.DEFAULT_LLM_ENV_INTERFACE = model
    cfg.DEFAULT_LLM_NL_ASSERTIONS = model

    # this module IS already imported by tau2/__init__, but it reads the model
    # from its own globals at call time, so patching the module attrs works
    import tau2.evaluator.evaluator_nl_assertions as nl_eval

    nl_eval.DEFAULT_LLM_NL_ASSERTIONS = model
    nl_eval.DEFAULT_LLM_NL_ASSERTIONS_ARGS = {"temperature": 0.0}
    nl_eval.json = _LenientJson()


def set_policy_suffix(suffix: str | None) -> None:
    """Append `suffix` to every Environment.get_policy() (None = restore).
    Agents built by the runner receive domain_policy=env.get_policy(), so this
    injects an experience library into the agent system prompt globally."""
    from tau2.environment.environment import Environment

    if not hasattr(Environment, "_orig_get_policy"):
        Environment._orig_get_policy = Environment.get_policy
    if suffix:
        Environment.get_policy = (
            lambda self: Environment._orig_get_policy(self) + suffix)
    else:
        Environment.get_policy = Environment._orig_get_policy
