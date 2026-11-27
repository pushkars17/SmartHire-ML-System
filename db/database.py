import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path(__file__).resolve().parent / "smarthire.db"


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path = DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_name TEXT,
                cgpa REAL NOT NULL,
                coding_score REAL NOT NULL,
                interview_score REAL NOT NULL,
                soft_skills REAL NOT NULL,
                college_tier INTEGER NOT NULL,
                selection_probability REAL NOT NULL,
                tier TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def save_evaluation(
    record: Dict[str, Any],
    db_path: Path = DB_PATH,
) -> int:
    init_db(db_path)
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO evaluations (
                candidate_name,
                cgpa,
                coding_score,
                interview_score,
                soft_skills,
                college_tier,
                selection_probability,
                tier
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.get("candidate_name") or "Anonymous",
                float(record["cgpa"]),
                float(record["coding_score"]),
                float(record["interview_score"]),
                float(record["soft_skills"]),
                int(record["college_tier"]),
                float(record["selection_probability"]),
                str(record["tier"]),
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def fetch_evaluations(
    limit: int = 50,
    tier: Optional[str] = None,
    db_path: Path = DB_PATH,
) -> List[Dict[str, Any]]:
    init_db(db_path)
    query = "SELECT * FROM evaluations"
    params: List[Any] = []

    if tier and tier.upper() != "ALL":
        query += " WHERE UPPER(tier) = UPPER(?)"
        params.append(tier)

    query += " ORDER BY id DESC LIMIT ?"
    params.append(int(limit))

    with get_connection(db_path) as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]