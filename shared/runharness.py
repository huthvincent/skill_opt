"""Run harness: enforces the CONSTITUTION section 3 contract for every experiment run.

Usage pattern (every experiment script):

    from shared.paths import REPLAY_RESULTS, new_run_id
    from shared.runharness import Run

    run = Run(REPLAY_RESULTS, new_run_id("tau2_probe"), config={...})
    run.log("starting")
    ...
    run.metric("n_tasks", 114)
    run.finish(conclusion="one-sentence conclusion for REPORT.md and the LEDGER")

Produces results/<run_id>/ with config.json (incl. git commit hash), log.txt,
and an auto-generated REPORT.md. Reminds you (stdout) to add the LEDGER line -
the harness cannot edit LEDGER.md safely in parallel, so that stays manual.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from shared.paths import PROJECT_ROOT


def _git_hash() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10,
        ).stdout.strip() or "unknown"
    except Exception:
        return "unknown"


class Run:
    def __init__(self, results_root: Path, run_id: str, config: dict | None = None):
        self.run_id = run_id
        self.dir = results_root / run_id
        self.dir.mkdir(parents=True, exist_ok=False)
        self.started = datetime.now().isoformat(timespec="seconds")
        self.metrics: dict = {}
        self._logf = open(self.dir / "log.txt", "w", buffering=1)
        cfg = dict(config or {})
        cfg.setdefault("run_id", run_id)
        cfg.setdefault("git_commit", _git_hash())
        cfg.setdefault("started_at", self.started)
        cfg.setdefault("argv", sys.argv)
        self.config = cfg
        (self.dir / "config.json").write_text(json.dumps(cfg, indent=2, ensure_ascii=False))

    def log(self, msg: str) -> None:
        line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
        print(line)
        self._logf.write(line + "\n")

    def metric(self, key: str, value) -> None:
        self.metrics[key] = value
        self.log(f"metric {key} = {value}")

    def finish(self, conclusion: str, extra_md: str = "") -> None:
        (self.dir / "metrics.json").write_text(
            json.dumps(self.metrics, indent=2, ensure_ascii=False))
        rows = "\n".join(f"| {k} | {v} |" for k, v in self.metrics.items()) or "| - | - |"
        report = (
            f"# REPORT - {self.run_id}\n\n"
            f"- started: {self.started}  finished: {datetime.now().isoformat(timespec='seconds')}\n"
            f"- git commit: `{self.config['git_commit']}`\n"
            f"- config: see `config.json`\n\n"
            f"## Metrics\n\n| metric | value |\n|---|---|\n{rows}\n\n"
            f"## Conclusion\n\n{conclusion}\n"
            + (f"\n{extra_md}\n" if extra_md else "")
        )
        (self.dir / "REPORT.md").write_text(report)
        self._logf.close()
        print(f"\nREPORT: {self.dir / 'REPORT.md'}")
        print(f"REMINDER (CONSTITUTION 5.3): add one line to the paper's LEDGER.md:")
        print(f"  | {self.run_id} | {self.started[:10]} | <exp id> | <purpose> | "
              f"{list(self.metrics)[:2]} | {conclusion[:40]}... | ? |")
