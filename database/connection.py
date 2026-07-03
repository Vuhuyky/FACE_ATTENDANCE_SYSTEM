from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "attendance.db"

PHOTOS_DIR = BASE_DIR / "student_photos"

PHOTOS_DIR.mkdir(exist_ok=True)


def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn