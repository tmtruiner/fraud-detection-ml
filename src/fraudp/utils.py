from yaml import safe_load
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def load_config(path: Path | str = PROJECT_ROOT / "conf" / "config.yaml") -> dict:
    with open(path) as f:
        cfg = safe_load(f)

    return cfg

def resolve_path(path: str) -> Path:
    return PROJECT_ROOT / path