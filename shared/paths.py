"""Project path constants. CONSTITUTION rule: no absolute-path literals anywhere else.

PROJECT_ROOT is derived from this file's location, so the repo works unchanged
after being cloned to another machine (CONSTITUTION section 4).
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA = PROJECT_ROOT / "data"
DATA_RAW = DATA / "raw"                      # read-only originals
DATA_GENERATED_LOGS = DATA / "generated_logs"  # weak-agent "historical logs"
THIRD_PARTY = PROJECT_ROOT / "third_party"

REPLAY = PROJECT_ROOT / "REPLAY"
REPLAY_RESULTS = REPLAY / "results"
REPLAY_SCRIPT = REPLAY / "script"

WILDLOOP = PROJECT_ROOT / "WildLoop"
WILDLOOP_RESULTS = WILDLOOP / "results"
WILDLOOP_SCRIPT = WILDLOOP / "script"


def new_run_id(script_name: str) -> str:
    """run_id = <script_name>_<YYYYMMDD_HHMMSS>  (CONSTITUTION section 3)."""
    from datetime import datetime

    return f"{script_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
