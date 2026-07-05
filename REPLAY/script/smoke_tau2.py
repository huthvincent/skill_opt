"""E0.1: first real end-to-end smoke - 5 retail tasks, haiku agent x haiku user sim.

Verifies with real API calls: tau2 episode loop works with our Anthropic key
(via litellm), rewards come back, per-episode cost is measured (this number
feeds Doc/budget_estimate.md), and results land in our run-harness contract.

tau2 has three hardcoded gpt-4.1 defaults (agent/user we override via CLI
flags; DEFAULT_LLM_ENV_INTERFACE has NO flag and caused infrastructure_error
on tasks whose environment needs an interface LLM). Per CONSTITUTION we never
edit upstream code, so we run the CLI in-process and patch tau2.config BEFORE
tau2 imports interface_agent (verified import-order window exists).

Budget: hard-capped by design well under $10 (5 tasks, max 30 steps, haiku
everywhere); actual spend read back from tau2's per-simulation cost fields.

Run:  uv run python REPLAY/script/smoke_tau2.py
"""
from __future__ import annotations

import json
import shutil
import sys

from shared.paths import PROJECT_ROOT, REPLAY_RESULTS, new_run_id
from shared.runharness import Run

CAP_USD = 10.0
MODEL = "anthropic/claude-haiku-4-5-20251001"
N_TASKS, MAX_STEPS, SEED = 5, 30, 42

# --- patch tau2's hardcoded gpt-4.1 defaults BEFORE anything else of tau2 loads
import tau2.config as tau2_config  # noqa: E402

assert "tau2.environment.utils.interface_agent" not in sys.modules, \
    "interface_agent already imported - patch would not take effect"
tau2_config.DEFAULT_LLM_ENV_INTERFACE = MODEL
tau2_config.DEFAULT_LLM_NL_ASSERTIONS = MODEL

# evaluator_nl_assertions is ALREADY imported by tau2/__init__, and it reads
# the model name from its own module globals at call time - patch those too
# (root cause of infrastructure_error on the 112/114 retail tasks that carry
# NL assertions; verified via error traceback in run smoke_tau2_..._045003).
import tau2.evaluator.evaluator_nl_assertions as nl_eval  # noqa: E402

nl_eval.DEFAULT_LLM_NL_ASSERTIONS = MODEL
nl_eval.DEFAULT_LLM_NL_ASSERTIONS_ARGS = {"temperature": 0.0}


class _LenientJson:
    """haiku wraps judge JSON in markdown fences (gpt-4.1 does not); the
    upstream evaluator calls json.loads on the raw reply. Shim the module's
    `json` reference so loads() strips fences/preamble first."""

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


nl_eval.json = _LenientJson()

run_id = new_run_id("smoke_tau2")
run = Run(REPLAY_RESULTS, run_id, config={
    "experiment": "E0.1", "domain": "retail", "n_tasks": N_TASKS,
    "max_steps": MAX_STEPS, "seed": SEED,
    "agent_llm": MODEL, "user_llm": MODEL, "env_interface_llm": MODEL,
    "cap_usd": CAP_USD, "upstream_patch": "in-process tau2.config override",
})

from tau2.cli import main as tau2_main  # noqa: E402  (after patch)

argv = [
    "tau2", "run",
    "--domain", "retail", "--task-set-name", "retail",
    "--num-tasks", str(N_TASKS), "--num-trials", "1",
    "--agent", "llm_agent", "--agent-llm", MODEL,
    "--user", "user_simulator", "--user-llm", MODEL,
    "--max-steps", str(MAX_STEPS), "--seed", str(SEED),
    "--max-concurrency", "2", "--save-to", run_id,
]
run.log("in-process argv: " + " ".join(argv))
sys.argv = argv
try:
    tau2_main()
    exit_code = 0
except SystemExit as e:
    exit_code = int(e.code or 0)
run.metric("tau2_exit_code", exit_code)

results_file = PROJECT_ROOT / "third_party/tau2-bench/data/simulations" / run_id / "results.json"
if not results_file.exists():
    run.finish(conclusion=f"FAILED: tau2 exit={exit_code}, no results.json")
    raise SystemExit(1)

shutil.copy(results_file, run.dir / "results.json")  # keep our own permanent copy
data = json.loads(results_file.read_text())
sims = data["simulations"] if isinstance(data, dict) and "simulations" in data else data

rewards, costs, terms = [], [], []
for s in sims:
    ri = s.get("reward_info") or {}
    rewards.append(ri.get("reward"))
    costs.append((s.get("agent_cost") or 0) + (s.get("user_cost") or 0))
    terms.append(s.get("termination_reason"))
run.metric("n_simulations", len(sims))
run.metric("terminations", terms)
run.metric("rewards", rewards)
run.metric("success_rate", f"{sum(1 for r in rewards if r == 1.0)}/{len(rewards)}")
run.metric("cost_per_episode_usd", [round(c, 4) for c in costs])
total = sum(costs)
run.metric("total_cost_usd", round(total, 4))
run.metric("under_cap", total < CAP_USD)

completed = sum(1 for r in rewards if r is not None)
run.finish(conclusion=(
    f"E0.1 {'PASSED' if exit_code == 0 and completed == len(sims) and total < CAP_USD else 'CHECK NEEDED'}: "
    f"{completed}/{len(sims)} episodes completed, success {run.metrics['success_rate']}, "
    f"total ~${total:.2f} (avg ${total / max(completed, 1):.3f}/episode, haiku all roles) - "
    f"per-episode number seeds Doc/budget_estimate.md."))
