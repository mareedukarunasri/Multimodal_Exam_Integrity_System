from fastapi import APIRouter
import sqlite3
from pathlib import Path

router = APIRouter()

DATABASE_NAME = Path(__file__).resolve().parent.parent.parent / "exam_events.db"


@router.get("/api/browser-events")
def get_browser_events():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, student_id, event_type, event_time, risk_score, risk_level
        FROM browser_events
        ORDER BY id DESC
        LIMIT 100
    """)

    events = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return {
        "total_events": len(events),
        "events": events
    }