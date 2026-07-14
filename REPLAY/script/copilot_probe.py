"""E0.5: feasibility probe for the GitHub Copilot backend (LLM_BACKEND=copilot).

Motivation: Gate 1 stalled when the pay-per-token Anthropic balance ran out.
Copilot access rides a flat-rate GitHub subscription, so it is an attractive
alternative *for cheap smoke / log-generation work* (reproducibility caveats
make it unsuitable for headline E1 numbers - Copilot model versions are opaque
and rolling). This probe answers, empirically and cheaply, three questions:

  Stage "chat" (no tau2): does litellm's github_copilot/ route authenticate
     (device flow) and return a plain completion through shared.llm.chat()?
  Stage "tau2": can a Copilot-served model act as the tau2 *agent* - i.e. does
     Copilot's Chat API expose the OpenAI tool/function-calling that tau2's
     domain tools require - and does a reward come back on one retail task?

The tau2 stage reuses the two upstream patches from shared/tau2_compat.py
(gpt-4.1 default repoint + lenient judge-JSON), pointing them at the Copilot
model too. Upstream code stays untouched (CONSTITUTION: never edit third_party).

Auth note: the FIRST run prints a github.com/login/device URL + code; complete
it once and the token caches under ~/.config/litellm/github_copilot/. Run the
"chat" stage first so tau2 inherits the cached token.

Run:
  uv run python REPLAY/script/copilot_probe.py                 # both stages
  uv run python REPLAY/script/copilot_probe.py --stage chat    # auth check only
  uv run python REPLAY/script/copilot_probe.py --model gpt-4o  # pick a model
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys

# tau2's rich console banner prints non-cp1252 glyphs (e.g. U+2192 "->"); on a
# Windows console that raises UnicodeEncodeError before any task runs. Force
# UTF-8 on our own streams so the harness works cross-platform.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    except Exception:  # noqa: BLE001 - non-reconfigurable stream, ignore
        pass

# Force the Copilot backend BEFORE importing shared.llm, so load_dotenv (which
# does not override already-set env vars) cannot pin us back to anthropic.
os.environ["LLM_BACKEND"] = "copilot"

from shared.llm import CostTracker, chat  # noqa: E402
from shared.paths import PROJECT_ROOT, REPLAY_RESULTS, new_run_id  # noqa: E402
from shared.runharness import Run  # noqa: E402


def stage_chat(run: Run, model: str) -> bool:
    """Plain completion through shared.llm copilot backend. Returns pass/fail."""
    run.log(f"[chat] LLM_BACKEND=copilot model={model} - first call may prompt "
            f"device-flow login (visit the printed github.com URL + code)")
    tracker = CostTracker()  # flat-rate: meters tokens+calls, no USD cap
    try:
        reply = chat(
            "Reply with exactly: OK",
            model=model, max_tokens=32, temperature=0.0, tracker=tracker,
        )
    except Exception as e:  # noqa: BLE001 - probe: report, don't crash the run
        run.log(f"[chat] FAILED: {type(e).__name__}: {e}")
        run.metric("chat_ok", False)
        run.metric("chat_error", f"{type(e).__name__}: {e}")
        return False
    ok = "ok" in reply.lower()
    run.metric("chat_ok", ok)
    run.metric("chat_reply", reply.strip()[:120])
    run.metric("chat_tokens", f"in={tracker.tokens_in} out={tracker.tokens_out}")
    run.log(f"[chat] reply={reply.strip()!r} tokens_in={tracker.tokens_in} "
            f"tokens_out={tracker.tokens_out}")
    return ok


def stage_tau2(run: Run, model: str, domain: str, num_tasks: int,
               max_steps: int, seed: int) -> bool:
    """One tau2 task with a Copilot-served agent - tests domain tool-calling."""
    lm = f"github_copilot/{model}"
    run.log(f"[tau2] agent/user/env/judge all -> {lm}")

    # Patch tau2's hardcoded gpt-4.1 defaults + lenient judge JSON to the
    # Copilot model BEFORE tau2 imports interface_agent (order asserted inside).
    from shared.tau2_compat import apply_default_model_patches
    try:
        apply_default_model_patches(lm)
    except AssertionError as e:
        run.log(f"[tau2] SKIPPED: patch window missed ({e})")
        run.metric("tau2_ran", False)
        return False

    from tau2.cli import main as tau2_main  # noqa: E402  (after patch)

    save_id = run.run_id + "_tau2"
    argv = [
        "tau2", "run",
        "--domain", domain, "--task-set-name", domain,
        "--num-tasks", str(num_tasks), "--num-trials", "1",
        "--agent", "llm_agent", "--agent-llm", lm,
        "--user", "user_simulator", "--user-llm", lm,
        "--max-steps", str(max_steps), "--seed", str(seed),
        "--max-concurrency", "1", "--save-to", save_id,
    ]
    run.log("[tau2] in-process argv: " + " ".join(argv))
    sys.argv = argv
    try:
        tau2_main()
        exit_code = 0
    except SystemExit as e:
        exit_code = int(e.code or 0)
    except Exception as e:  # noqa: BLE001 - capture tool-calling failures etc.
        run.log(f"[tau2] EXCEPTION: {type(e).__name__}: {e}")
        run.metric("tau2_ran", False)
        run.metric("tau2_error", f"{type(e).__name__}: {e}")
        return False
    run.metric("tau2_exit_code", exit_code)

    results_file = (PROJECT_ROOT / "third_party/tau2-bench/data/simulations"
                    / save_id / "results.json")
    if not results_file.exists():
        run.log(f"[tau2] no results.json (exit={exit_code})")
        run.metric("tau2_ran", False)
        return False
    shutil.copy(results_file, run.dir / "results.json")
    data = json.loads(results_file.read_text())
    sims = data["simulations"] if isinstance(data, dict) and "simulations" in data else data

    rewards, terms = [], []
    for s in sims:
        rewards.append((s.get("reward_info") or {}).get("reward"))
        terms.append(s.get("termination_reason"))
    completed = sum(1 for r in rewards if r is not None)
    run.metric("tau2_ran", True)
    run.metric("tau2_n_simulations", len(sims))
    run.metric("tau2_terminations", terms)
    run.metric("tau2_rewards", rewards)
    run.log(f"[tau2] completed={completed}/{len(sims)} rewards={rewards} terms={terms}")
    # "tool-calling works" = at least one episode ran to a verdict without an
    # infrastructure_error termination.
    tool_calling_ok = completed == len(sims) and not any(
        t == "infrastructure_error" for t in terms)
    run.metric("tau2_tool_calling_ok", tool_calling_ok)
    return tool_calling_ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage", choices=["chat", "tau2", "both"], default="both")
    ap.add_argument("--model", default="gpt-4o",
                    help="Copilot model id (github_copilot/ prefix added automatically)")
    ap.add_argument("--domain", default="retail")
    ap.add_argument("--num-tasks", type=int, default=1)
    ap.add_argument("--max-steps", type=int, default=30)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    run_id = new_run_id("copilot_probe")
    run = Run(REPLAY_RESULTS, run_id, config={
        "experiment": "E0.5", "backend": "copilot", "model": args.model,
        "stage": args.stage, "domain": args.domain, "num_tasks": args.num_tasks,
        "max_steps": args.max_steps, "seed": args.seed,
        "note": "flat-rate Copilot subscription; no per-token USD metering",
    })

    chat_ok = tau2_ok = None
    if args.stage in ("chat", "both"):
        chat_ok = stage_chat(run, args.model)
    if args.stage in ("tau2", "both"):
        if args.stage == "both" and chat_ok is False:
            run.log("[tau2] skipped: chat stage failed (auth/model unreachable)")
        else:
            tau2_ok = stage_tau2(run, args.model, args.domain, args.num_tasks,
                                 args.max_steps, args.seed)

    verdict = "GO" if (chat_ok in (True, None) and tau2_ok in (True, None)
                       and (chat_ok or tau2_ok)) else "NO-GO / CHECK"
    run.finish(conclusion=(
        f"E0.5 copilot probe [{verdict}]: chat_ok={chat_ok}, "
        f"tau2_tool_calling_ok={tau2_ok} (model={args.model}). "
        f"If tau2_tool_calling_ok is True, Copilot supports the domain "
        f"function-calling tau2 needs -> viable for smoke/log-gen. Reproducibility "
        f"caveat (rolling model versions) still bars it from headline E1 numbers."))


if __name__ == "__main__":
    main()
