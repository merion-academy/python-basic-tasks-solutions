from pathlib import Path

BASE_DIR = Path(__file__).parent

DB_FILE = BASE_DIR / "db.sqlite3"
DB_URL = f"sqlite:///{DB_FILE}"
