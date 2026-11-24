"""Locations of the data files in this repository."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"

SCENARIOS_FILE = DATA_DIR / "rvig-gezag" / "scenarios.json"
EXAMPLES_DIR = DATA_DIR / "rvig-gezag" / "examples"
SNAPSHOT_FILE = DATA_DIR / "algoritmeregister" / "gezag-61781447.json"
UITLEG_FILE = DATA_DIR / "uitleg" / "gezag.yaml"
BESLUITEN_DIR = DATA_DIR / "besluiten"
SCHEMA_DIR = DATA_DIR / "schemas"
