"""Gate 1 (sanity check): does a good experience library raise success at all?

Protocol (docs/sanity_check.md, Gate 1 - ceiling test):
  A. baseline: 30 retail tasks x 2 trials, haiku agent+user, NO library
  B. a strong model writes a "cheating-allowed" library from A's failures +
     gold evaluation criteria (generalizable entries only - no task-specific
     IDs; we measure the ceiling of experience-style guidance, not a lookup
     table)
  C. same 30 tasks x 2 trials WITH the library injected into the agent prompt
Gate verdict: PASS if episode success rate improves by >= +10pp.

Budget: design ~$13, hard abort projection above CAP_USD=$20 (anthropic backend).
Copilot backend is flat-rate (subscription), so the USD projection cap does not
apply - budget discipline there is request-count / rate-limit based.

Run (anthropic, full):  uv run python REPLAY/script/gate1_ceiling.py
Run (copilot pilot):    uv run python REPLAY/script/gate1_ceiling.py \
                          --backend copilot --model github_copilot/gpt-4o \
                          --n-tasks 5 --trials 1 --concurrency 2
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

# tau2's rich banner emits non-cp1252 glyphs (U+2192); force UTF-8 so this runs
# on a Windows console (root-caused in REPLAY/script/copilot_probe.py).
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    except Exception:  # noqa: BLE001 - non-reconfigurable stream, ignore
        pass

ap = argparse.ArgumentParser(description="Gate 1 ceiling test (see docs/sanity_check.md)")
ap.add_argument("--backend", choices=["anthropic", "copilot"], default="anthropic",
                help="LLM_BACKEND for shared.llm AND tau2's litellm model prefix")
ap.add_argument("--model", default=None,
                help="agent/user/judge model id (backend-appropriate); default per backend")
ap.add_argument("--optimizer-model", default=None,
                help="model that writes the ceiling library; default per backend")
ap.add_argument("--n-tasks", type=int, default=30)
ap.add_argument("--trials", type=int, default=2)
ap.add_argument("--concurrency", type=int, default=6,
                help="tau2 --max-concurrency (lower for Copilot rate limits)")
ap.add_argument("--cap-usd", type=float, default=20.0,
                help="hard USD projection cap (anthropic only; copilot is flat-rate)")
ap.add_argument("--resume-baseline", default=None,
                help="prior run dir containing base_results.json (skips phase A)")
args = ap.parse_args()

# backend must be set BEFORE importing shared.llm (load_dotenv won't override it)
os.environ["LLM_BACKEND"] = args.backend

# Model defaults per backend. tau2 routes through litellm, so the agent/user
# model string must carry the provider prefix (anthropic/... | github_copilot/...).
# The optimizer goes through shared.llm.chat(): the copilot backend adds the
# github_copilot/ prefix itself, so OPTIMIZER_MODEL is prefix-less there.
if args.backend == "copilot":
    MODEL = args.model or "github_copilot/gpt-4o"
    OPTIMIZER_MODEL = args.optimizer_model or "gpt-4o"
else:
    MODEL = args.model or "anthropic/claude-haiku-4-5-20251001"
    OPTIMIZER_MODEL = args.optimizer_model  # None -> MODEL_OPTIMIZER from .env

from shared.llm import CostTracker, chat  # noqa: E402
from shared.paths import PROJECT_ROOT, REPLAY_RESULTS, new_run_id  # noqa: E402
from shared.runharness import Run  # noqa: E402
from shared.tau2_compat import apply_default_model_patches, set_policy_suffix  # noqa: E402

CAP_USD = args.cap_usd
N_TASKS, TRIALS, MAX_STEPS, SEED, CONC = args.n_tasks, args.trials, 30, 42, args.concurrency
GATE_PP = 0.10  # +10 percentage points
FLAT_RATE = args.backend == "copilot"

apply_default_model_patches(MODEL)
from tau2.cli import main as tau2_main  # noqa: E402  (after patches)
from tau2.registry import registry  # noqa: E402

run_id = new_run_id("gate1_ceiling")
run = Run(REPLAY_RESULTS, run_id, config={
    "experiment": "Gate1", "domain": "retail", "n_tasks": N_TASKS,
    "trials": TRIALS, "max_steps": MAX_STEPS, "seed": SEED,
    "backend": args.backend, "model": MODEL, "optimizer_model": OPTIMIZER_MODEL,
    "concurrency": CONC, "flat_rate": FLAT_RATE,
    "cap_usd": CAP_USD, "gate_pp": GATE_PP,
    "resumed_baseline_from": args.resume_baseline,
})


def tau2_run(save_to: str, suffix: str | None) -> list[dict]:
    set_policy_suffix(suffix)
    sys.argv = [
        "tau2", "run", "--domain", "retail", "--task-set-name", "retail",
        "--num-tasks", str(N_TASKS), "--num-trials", str(TRIALS),
        "--agent", "llm_agent", "--agent-llm", MODEL,
        "--user", "user_simulator", "--user-llm", MODEL,
        "--max-steps", str(MAX_STEPS), "--seed", str(SEED),
        "--max-concurrency", str(CONC), "--save-to", save_to,
    ]
    try:
        tau2_main()
    except SystemExit as e:
        if e.code:
            raise RuntimeError(f"tau2 exited {e.code} for {save_to}")
    finally:
        set_policy_suffix(None)
    src = PROJECT_ROOT / "third_party/tau2-bench/data/simulations" / save_to / "results.json"
    shutil.copy(src, run.dir / f"{save_to.rsplit('_', 1)[-1]}_results.json")
    d = json.loads(src.read_text())
    return d["simulations"] if isinstance(d, dict) else d


def stats(sims: list[dict]) -> dict:
    ok = [1.0 if (s.get("reward_info") or {}).get("reward") == 1.0 else 0.0
          for s in sims if s.get("termination_reason") != "infrastructure_error"]
    cost = sum((s.get("agent_cost") or 0) + (s.get("user_cost") or 0) for s in sims)
    per_task: dict[str, list[float]] = {}
    for s in sims:
        r = (s.get("reward_info") or {}).get("reward")
        if r is not None:
            per_task.setdefault(str(s["task_id"]), []).append(float(r == 1.0))
    return {"n": len(ok), "success": sum(ok) / max(len(ok), 1),
            "cost": cost, "per_task": {k: sum(v) / len(v) for k, v in per_task.items()},
            "errors": sum(1 for s in sims
                          if s.get("termination_reason") == "infrastructure_error")}


# ---------- Phase A: baseline ----------
if args.resume_baseline:
    src = Path(args.resume_baseline) / "base_results.json"
    run.log(f"Phase A: resuming baseline from {src} (cost already sunk, not re-run)")
    d = json.loads(src.read_text())
    sims_a = d["simulations"] if isinstance(d, dict) else d
    shutil.copy(src, run.dir / "base_results.json")
else:
    run.log("Phase A: baseline (no library)")
    sims_a = tau2_run(f"{run_id}_base", None)
a = stats(sims_a)
run.metric("A_success", round(a["success"], 3))
run.metric("A_episodes", a["n"])
run.metric("A_errors", a["errors"])
run.metric("A_cost_usd", round(a["cost"], 2))

projected = a["cost"] * 2 + 2.5  # phase C similar cost + optimizer + NL-eval slack
run.metric("projected_total_usd", round(projected, 2))
if not FLAT_RATE and projected > CAP_USD:
    run.finish(conclusion=f"ABORTED before phase C: projection ${projected:.2f} > cap ${CAP_USD}")
    raise SystemExit(1)

# ---------- Phase B: strong model writes the ceiling library ----------
run.log("Phase B: generating ceiling library from failures + gold criteria")
tasks = {str(t.id): t for t in registry.get_tasks_loader("retail")()}
policy_doc = ""  # agent already sees the policy; library must ADD beyond it
failed_ids = sorted({str(s["task_id"]) for s in sims_a
                     if (s.get("reward_info") or {}).get("reward") not in (None, 1.0)})
run.metric("A_failed_task_ids", failed_ids)

blocks = []
for tid in failed_ids[:8]:
    sim = next(s for s in sims_a
               if str(s["task_id"]) == tid and (s.get("reward_info") or {}).get("reward") != 1.0)
    traj = "\n".join(
        f"{m['role']}: {m.get('content') or json.dumps(m.get('tool_calls'), ensure_ascii=False)}"
        for m in (sim.get("messages") or []) if m.get("content") or m.get("tool_calls"))
    crit = tasks[tid].evaluation_criteria
    blocks.append(
        f"### Failed task {tid}\nTRAJECTORY (truncated):\n{traj[:2500]}\n\n"
        f"GOLD CRITERIA (what should have happened):\n"
        f"{crit.model_dump_json(exclude_none=True)[:1500]}")

tracker = CostTracker(max_cost_usd=3.0)
library = chat(
    "You are optimizing a customer-service agent for the tau2-bench retail domain. "
    "Below are failed episodes (agent behavior) and the gold evaluation criteria for each. "
    "Write an EXPERIENCE LIBRARY: 10-16 bullet entries, each 1-3 imperative sentences, "
    "that would prevent these failure patterns.\n"
    "HARD RULES: entries must be GENERALIZABLE procedures/pitfalls - never mention "
    "specific order numbers, product names, user names or emails; do not restate the "
    "domain policy the agent already has; focus on process mistakes (e.g. verification "
    "steps, tool-call ordering, when to check before acting, exchange vs return rules "
    "misapplication). Max 700 tokens total. Output ONLY the markdown bullet list.\n\n"
    + "\n\n".join(blocks),
    role="optimizer", model=OPTIMIZER_MODEL, max_tokens=8000, tracker=tracker)  # reasoning models need headroom
(run.dir / "library.md").write_text(library)
if not library.strip() or (library.count("\n- ") + library.count("\n* ")) < 3:
    run.finish(conclusion="ABORTED before phase C: optimizer produced an empty/"
                          "degenerate library - fix generation before spending on C")
    raise SystemExit(1)
run.metric("B_optimizer_cost_usd", round(tracker.spent_usd, 3))
run.metric("B_library_entries", library.count("\n- ") + library.count("\n* ")
           + (1 if library.lstrip().startswith(("-", "*")) else 0))
run.log(f"library written ({len(library)} chars)")

# ---------- Phase C: with library ----------
run.log("Phase C: with library injected")
suffix = "\n\n# Experience Library (tips learned from past interactions)\n" + library
sims_c = tau2_run(f"{run_id}_lib", suffix)
c = stats(sims_c)
run.metric("C_success", round(c["success"], 3))
run.metric("C_episodes", c["n"])
run.metric("C_errors", c["errors"])
run.metric("C_cost_usd", round(c["cost"], 2))

# ---------- verdict ----------
delta = c["success"] - a["success"]
run.metric("delta_pp", round(delta * 100, 1))
paired = {tid: (a["per_task"].get(tid), c["per_task"].get(tid))
          for tid in sorted(a["per_task"]) if a["per_task"].get(tid, 1) < 1}
total_spend = a["cost"] + c["cost"] + tracker.spent_usd
run.metric("total_spend_usd", round(total_spend, 2))
verdict = "PASS" if delta >= GATE_PP else "FAIL"
run.metric("gate1_verdict", verdict)

run.finish(
    conclusion=(
        f"Gate 1 {verdict}: baseline {a['success']:.1%} -> with-library {c['success']:.1%} "
        f"({delta * 100:+.1f}pp, gate >= +10pp), spend ~${total_spend:.2f} "
        f"(+ untracked NL-judge calls ~$1)."),
    extra_md=("## Per-task (baseline<1.0) paired success\n\n| task | base | lib |\n|---|---|---|\n"
              + "\n".join(f"| {t} | {b} | {l} |" for t, (b, l) in paired.items())
              + "\n\n## Library used\n\nsee `library.md` in this run dir\n"))
