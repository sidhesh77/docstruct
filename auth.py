"""
Authentication and user management for DocStruct.
Uses SQLite + bcrypt for secure password storage.
"""

import os
import sqlite3
from datetime import datetime, timezone
from typing import Optional

import bcrypt

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "docstruct.db")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with _connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS extraction_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                extracted_json TEXT NOT NULL,
                validation_score TEXT NOT NULL,
                extraction_mode TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            """
        )

        existing = conn.execute(
            "SELECT id FROM users WHERE username = ?", ("demo",)
        ).fetchone()
        if not existing:
            _create_user(conn, "demo", "demo@docstruct.app", "demo123")


def _hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _verify_password(password: str, password_hash: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash)


def _create_user(
    conn: sqlite3.Connection, username: str, email: str, password: str
) -> int:
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.execute(
        """
        INSERT INTO users (username, email, password_hash, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (username.lower().strip(), email.lower().strip(), _hash_password(password), now),
    )
    conn.commit()
    return cursor.lastrowid


def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
    username = username.strip()
    email = email.strip()

    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if "@" not in email or len(email) < 5:
        return False, "Please enter a valid email address."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    try:
        with _connect() as conn:
            _create_user(conn, username, email, password)
        return True, "Account created successfully. Please sign in."
    except sqlite3.IntegrityError:
        return False, "Username or email already exists."


def authenticate(username: str, password: str) -> tuple[bool, Optional[dict], str]:
    username = username.strip().lower()
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, username, email, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if not row or not _verify_password(password, row["password_hash"]):
        return False, None, "Invalid username or password."

    return True, {"id": row["id"], "username": row["username"], "email": row["email"]}, ""


def save_extraction(
    user_id: int,
    filename: str,
    extracted_json: str,
    validation_score: str,
    extraction_mode: str,
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO extraction_history
            (user_id, filename, extracted_json, validation_score, extraction_mode, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, filename, extracted_json, validation_score, extraction_mode, now),
        )
        conn.commit()


def get_user_stats(user_id: int) -> dict:
    with _connect() as conn:
        total = conn.execute(
            "SELECT COUNT(*) AS count FROM extraction_history WHERE user_id = ?",
            (user_id,),
        ).fetchone()["count"]
        recent = conn.execute(
            """
            SELECT filename, validation_score, extraction_mode, created_at
            FROM extraction_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 5
            """,
            (user_id,),
        ).fetchall()
    return {"total_extractions": total, "recent": [dict(row) for row in recent]}