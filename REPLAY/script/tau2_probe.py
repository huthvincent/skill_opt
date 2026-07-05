"""E0.0: zero-LLM structure probe of tau2-bench.

Verifies, without any API call, the four facts REPLAY's protocol depends on:
  1. task sets load programmatically; per-set counts
  2. Task fields we need exist (persona, structured instructions, evaluation_criteria)
  3. post-hoc evaluation entrypoint (evaluate_simulation) is importable & pure-callable
  4. persona injection point (PersonaConfig) exists  [WildLoop risk item]

Run:  uv run python REPLAY/script/tau2_probe.py
"""
from __future__ import annotations

import json
from collections import Counter

from shared.paths import REPLAY_RESULTS, new_run_id
from shared.runharness import Run

run = Run(REPLAY_RESULTS, new_run_id("tau2_probe"), config={
    "experiment": "E0.0",
    "llm_calls": 0,
    "tau2_commit": "1901a301961cbbe3fd11f3e84a2a376530c759e3",
})

findings: list[str] = []

# --- 1. task sets & counts -------------------------------------------------
from tau2.registry import registry

task_sets = registry.get_task_sets()
run.metric("task_sets", ",".join(task_sets))
for name in ["retail", "airline", "telecom"]:
    try:
        tasks = registry.get_tasks_loader(name)()
        run.metric(f"n_tasks_{name}", len(tasks))
    except Exception as e:  # noqa: BLE001 - probe must survive and report
        run.log(f"FAIL loading {name}: {e}")
        findings.append(f"task set `{name}` failed to load: {e}")

# --- 2. task structure (retail as reference) --------------------------------
tasks = registry.get_tasks_loader("retail")()
t0 = tasks[0]
sample = json.loads(t0.model_dump_json())
(run.dir / "sample_task_retail.json").write_text(
    json.dumps(sample, indent=2, ensure_ascii=False))
run.log(f"sample task {t0.id} dumped to sample_task_retail.json")

persona_cov = sum(1 for t in tasks if t.user_scenario and t.user_scenario.persona)
run.metric("retail_persona_coverage", f"{persona_cov}/{len(tasks)}")

basis = Counter()
for t in tasks:
    if t.evaluation_criteria and t.evaluation_criteria.reward_basis:
        basis.update(str(b) for b in t.evaluation_criteria.reward_basis)
run.metric("retail_reward_basis_dist", dict(basis))

# --- 3. post-hoc evaluation entrypoint --------------------------------------
try:
    from tau2.evaluator.evaluator import EvaluationType, evaluate_simulation  # noqa: F401

    run.metric("posthoc_eval_importable", True)
    run.metric("evaluation_types", [e.name for e in EvaluationType])
except Exception as e:  # noqa: BLE001
    run.metric("posthoc_eval_importable", False)
    findings.append(f"evaluate_simulation import failed: {e}")

# --- 4. persona injection point (WildLoop) ----------------------------------
try:
    from tau2.data_model.persona import PersonaConfig  # noqa: F401
    import inspect

    from tau2.user.user_simulator import UserSimulator

    ok = "persona_config" in inspect.signature(UserSimulator.__init__).parameters
    run.metric("persona_config_injectable", ok)
    if not ok:
        findings.append("UserSimulator.__init__ has no persona_config param")
except Exception as e:  # noqa: BLE001
    run.metric("persona_config_injectable", False)
    findings.append(f"PersonaConfig probe failed: {e}")

# --- 5. environment constructor (best-effort) --------------------------------
try:
    ctor = registry.get_env_constructor("retail")
    env = ctor()
    run.metric("env_constructible_no_llm", True)
    run.metric("env_type", type(env).__name__)
except Exception as e:  # noqa: BLE001
    run.metric("env_constructible_no_llm", False)
    findings.append(f"env construction: {e} (may need kwargs - check at E0.1)")

extra = ("## Findings / follow-ups\n\n" + "\n".join(f"- {f}" for f in findings)) if findings else ""
ok_core = run.metrics.get("posthoc_eval_importable") and run.metrics.get("persona_config_injectable")
run.finish(
    conclusion=(
        "tau2-bench structure probe "
        + ("PASSED: task loading, post-hoc evaluate_simulation, and PersonaConfig "
           "injection all confirmed without any LLM call - hidden-verifier protocol "
           "and WildLoop grounding are implementable."
           if ok_core else "FOUND ISSUES - see findings.")
    ),
    extra_md=extra,
)
