import sqlite3
import yapom.utils as utils

from pathlib import Path

DATABASE = "pomodoro.db"


def get_db_path() -> Path:
    home_dir_path = utils.home_dir()
    if not (db_path := home_dir_path / Path(DATABASE)).exists():
        db_path.touch()
    return db_path


def get_db_connection() -> sqlite3.Connection:
    return sqlite3.connect(get_db_path())


def create_db_table():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """CREATE TABLE IF NOT EXISTS sessions (
        start TEXT,
        end TEXT,
        runtime INTEGER,
        status TEXT)"""
        cursor.execute(query)
        conn.commit()


def archive_pomodoro_session(session_data: dict):
    start_str = session_data["start"]
    end_str = session_data["end"]
    runtime = int(session_data["runtime"])
    status_str = utils.Status(session_data["status"]).value
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """INSERT INTO sessions (start, end, runtime, status)
                   VALUES (?, ?, ?, ?)"""
        cursor.execute(query, (start_str, end_str, runtime, status_str))
        conn.commit()
