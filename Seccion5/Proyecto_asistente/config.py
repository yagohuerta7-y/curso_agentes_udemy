from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / 'services' / "Data"
VDB_DIR = ROOT_DIR / 'services' / "VDB"

DATA_DIR.mkdir(parents=True, exist_ok=True)
VDB_DIR.mkdir(parents=True, exist_ok=True)