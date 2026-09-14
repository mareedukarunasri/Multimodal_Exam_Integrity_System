from pathlib import Path
import sqlite3
import uuid
from datetime import datetime


DATABASE_NAME = Path(__file__).resolve().parent.parent / "exam_events.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


# =========================================================
# CREATE DATABASE
# =========================================================

def create_database():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # -----------------------------------------------------
    # EXISTING EVENTS TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS browser_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_time TEXT,
            risk_score REAL,
            risk_level TEXT,
            session_id TEXT
        )
    """)

    # -----------------------------------------------------
    # MIGRATION FOR OLD DATABASE
    #
    # Your existing database was created without session_id.
    # This safely adds the column without deleting old data.
    # -----------------------------------------------------

    cursor.execute("PRAGMA table_info(browser_events)")

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    if "session_id" not in columns:

        cursor.execute("""
            ALTER TABLE browser_events
            ADD COLUMN session_id TEXT
        """)

    # -----------------------------------------------------
    # EXAM SESSIONS TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exam_sessions (
            session_id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            started_at TEXT NOT NULL,
            ended_at TEXT,
            status TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# =========================================================
# CREATE EXAM SESSION
# =========================================================

def create_exam_session(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    session_id = str(uuid.uuid4())

    started_at = datetime.utcnow().isoformat() + "Z"

    cursor.execute("""
        INSERT INTO exam_sessions
        (
            session_id,
            student_id,
            started_at,
            ended_at,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        session_id,
        student_id,
        started_at,
        None,
        "active"
    ))

    connection.commit()
    connection.close()

    return {
        "session_id": session_id,
        "student_id": student_id,
        "started_at": started_at,
        "status": "active"
    }


# =========================================================
# END EXAM SESSION
# =========================================================

def end_exam_session(session_id):

    connection = get_connection()
    cursor = connection.cursor()

    ended_at = datetime.utcnow().isoformat() + "Z"

    cursor.execute("""
        UPDATE exam_sessions
        SET
            ended_at = ?,
            status = ?
        WHERE session_id = ?
    """, (
        ended_at,
        "completed",
        session_id
    ))

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    if updated == 0:
        return None

    return {
        "session_id": session_id,
        "ended_at": ended_at,
        "status": "completed"
    }


# =========================================================
# GET EXAM SESSION
# =========================================================

def get_exam_session(session_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            session_id,
            student_id,
            started_at,
            ended_at,
            status
        FROM exam_sessions
        WHERE session_id = ?
    """, (session_id,))

    session = cursor.fetchone()

    connection.close()

    if session is None:
        return None

    return dict(session)


# =========================================================
# GET ACTIVE SESSION FOR STUDENT
# =========================================================

def get_active_exam_session(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            session_id,
            student_id,
            started_at,
            ended_at,
            status
        FROM exam_sessions
        WHERE student_id = ?
          AND status = 'active'
        ORDER BY started_at DESC
        LIMIT 1
    """, (student_id,))

    session = cursor.fetchone()

    connection.close()

    if session is None:
        return None

    return dict(session)


# =========================================================
# SAVE EVENT
# =========================================================

def save_browser_event(
    student_id,
    event_type,
    event_time,
    risk_score,
    risk_level,
    session_id=None
):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO browser_events
        (
            student_id,
            event_type,
            event_time,
            risk_score,
            risk_level,
            session_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        student_id,
        event_type,
        event_time,
        risk_score,
        risk_level,
        session_id
    ))

    connection.commit()
    connection.close()


# =========================================================
# GET ALL EVENTS
# =========================================================

def get_all_browser_events(session_id=None):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # -------------------------------------------------
        # GET EVENTS FOR A SPECIFIC SESSION
        # -------------------------------------------------

        if session_id:

            cursor.execute("""
                SELECT
                    id,
                    student_id,
                    event_type,
                    event_time,
                    risk_score,
                    risk_level,
                    session_id
                FROM browser_events
                WHERE session_id = ?
                ORDER BY id DESC
            """, (session_id,))

        # -------------------------------------------------
        # GET ALL HISTORICAL EVENTS
        # -------------------------------------------------

        else:

            cursor.execute("""
                SELECT
                    id,
                    student_id,
                    event_type,
                    event_time,
                    risk_score,
                    risk_level,
                    session_id
                FROM browser_events
                ORDER BY id DESC
            """)

        events = cursor.fetchall()

        return [
            dict(event)
            for event in events
        ]

    finally:

        connection.close()


# =========================================================
# STUDENT-WISE MULTIMODAL RISK
# =========================================================

def get_student_wise_summary(session_id=None):

    connection = get_connection()
    cursor = connection.cursor()

    # =====================================================
    # GET STUDENTS
    # =====================================================

    if session_id:

        cursor.execute("""
            SELECT
                student_id,
                COUNT(*) AS total_events
            FROM browser_events
            WHERE session_id = ?
            GROUP BY student_id
            ORDER BY student_id
        """, (session_id,))

    else:

        cursor.execute("""
            SELECT
                student_id,
                COUNT(*) AS total_events
            FROM browser_events
            GROUP BY student_id
            ORDER BY student_id
        """)

    students = cursor.fetchall()

    result = []

    # =====================================================
    # CAMERA EVENT TYPES
    # =====================================================

    camera_event_types = [
        "face_detected",
        "no_face_detected",
        "multiple_faces_detected",
        "looking_left",
        "looking_right",
        "head_looking_away",
        "mobile_phone_detected",
        "speech_detected"
    ]

    # =====================================================
    # GET ML PREDICTION
    #
    # NOTE:
    # ML prediction is still using the existing ML system.
    # Session-specific ML filtering will be handled later
    # when we modify the ML prediction file.
    # =====================================================

    ml_prediction = "NORMAL"
    ml_risk = 0

    try:

        from app.ml.predict import get_ml_prediction

        ml_result = get_ml_prediction()

        ml_prediction = ml_result.get(
            "prediction",
            "NORMAL"
        )

        if "CHEATING" in ml_prediction.upper():

            ml_risk = 100

        elif "SUSPICIOUS" in ml_prediction.upper():

            ml_risk = 100

        else:

            ml_risk = 0

    except Exception as error:

        print(
            "ML prediction error:",
            error
        )

        ml_prediction = "ML UNAVAILABLE"
        ml_risk = 0

    # =====================================================
    # PROCESS EACH STUDENT
    # =====================================================

    for student in students:

        student_id = student["student_id"]

        # -------------------------------------------------
        # GET EVENTS
        # -------------------------------------------------

        if session_id:

            cursor.execute("""
                SELECT
                    event_type,
                    risk_score,
                    risk_level,
                    event_time,
                    session_id
                FROM browser_events
                WHERE student_id = ?
                  AND session_id = ?
                ORDER BY id DESC
            """, (
                student_id,
                session_id
            ))

        else:

            cursor.execute("""
                SELECT
                    event_type,
                    risk_score,
                    risk_level,
                    event_time,
                    session_id
                FROM browser_events
                WHERE student_id = ?
                ORDER BY id DESC
            """, (student_id,))

        events = cursor.fetchall()

        total_events = len(events)

        # =================================================
        # SEPARATE BROWSER AND CAMERA EVENTS
        # =================================================

        browser_events = []
        camera_events = []

        for event in events:

            if event["event_type"] in camera_event_types:

                camera_events.append(event)

            else:

                browser_events.append(event)

        # =================================================
        # BROWSER RISK
        # =================================================

        browser_risk_total = 0

        for event in browser_events:

            if event["risk_score"] is not None:

                browser_risk_total += float(
                    event["risk_score"]
                )

        if len(browser_events) > 0:

            browser_risk = (
                browser_risk_total /
                len(browser_events)
            ) * 100

        else:

            browser_risk = 0

        # =================================================
        # BROWSER REPEATED BEHAVIOUR
        # =================================================

        tab_hidden = 0
        fullscreen_exit = 0
        copy_paste_cut = 0

        for event in browser_events:

            event_type = event["event_type"]

            if event_type == "tab_hidden":

                tab_hidden += 1

            if event_type == "fullscreen_exit":

                fullscreen_exit += 1

            if event_type in [
                "copy",
                "paste",
                "cut"
            ]:

                copy_paste_cut += 1

        # -------------------------------------------------
        # REPEATED SUSPICIOUS BEHAVIOUR
        # -------------------------------------------------

        if tab_hidden >= 10:

            browser_risk += 10

        if fullscreen_exit >= 2:

            browser_risk += 10

        if copy_paste_cut >= 3:

            browser_risk += 5

        browser_risk = min(
            round(browser_risk),
            100
        )

        # =================================================
        # CAMERA RISK
        # =================================================

        camera_risk_total = 0

        for event in camera_events:

            if event["risk_score"] is not None:

                camera_risk_total += float(
                    event["risk_score"]
                )

        if len(camera_events) > 0:

            camera_risk = (
                camera_risk_total /
                len(camera_events)
            ) * 100

        else:

            camera_risk = 0

        camera_risk = min(
            round(camera_risk),
            100
        )

        # =================================================
        # COUNT RISK EVENTS
        # =================================================

        high = 0
        medium = 0
        low = 0

        for event in events:

            risk_level = event["risk_level"]

            if risk_level == "high":

                high += 1

            elif risk_level == "medium":

                medium += 1

            elif risk_level == "low":

                low += 1

        # =================================================
        # BEHAVIOUR RISK
        # =================================================

        if total_events > 0:

            high_ratio = high / total_events

            medium_ratio = medium / total_events

        else:

            high_ratio = 0

            medium_ratio = 0

        behaviour_risk = (
            (high_ratio * 100) +
            (medium_ratio * 50)
        )

        behaviour_risk = min(
            behaviour_risk,
            100
        )

        # =================================================
        # MULTIMODAL BASE RISK
        #
        # Browser   = 40%
        # Camera    = 35%
        # Behaviour = 10%
        # ML        = 15%
        # =================================================

        browser_weight = 0.40
        camera_weight = 0.35
        behaviour_weight = 0.10
        ml_weight = 0.15

        base_risk = (

            (browser_risk * browser_weight) +

            (camera_risk * camera_weight) +

            (behaviour_risk * behaviour_weight) +

            (ml_risk * ml_weight)

        )

        # =================================================
        # REPEATED HIGH-RISK EVENT BONUS
        # =================================================

        repetition_bonus = min(
            high_ratio * 30,
            20
        )

        # =================================================
        # LATEST EVENT BONUS
        # =================================================

        latest_event = None
        latest_risk_level = None

        if events:

            latest_event = events[0]["event_type"]

            latest_risk_level = events[0]["risk_level"]

        latest_event_bonus = 0

        if latest_risk_level == "high":

            latest_event_bonus = 5

        elif latest_risk_level == "medium":

            latest_event_bonus = 2

        # =================================================
        # FINAL MULTIMODAL AI RISK
        # =================================================

        final_risk = (

            base_risk +

            repetition_bonus +

            latest_event_bonus

        )

        final_risk = min(
            round(final_risk),
            100
        )

        # =================================================
        # FINAL RISK LEVEL
        # =================================================

        if final_risk >= 70:

            final_risk_level = "high"

        elif final_risk >= 40:

            final_risk_level = "medium"

        elif final_risk > 0:

            final_risk_level = "low"

        else:

            final_risk_level = "normal"

        # =================================================
        # FINAL STUDENT RESULT
        # =================================================

        result.append({

            "student_id": student_id,

            "total_events": total_events,

            "browser_risk": browser_risk,

            "camera_risk": camera_risk,

            "behaviour_risk": round(
                behaviour_risk
            ),

            "ml_prediction": ml_prediction,

            "ml_risk": ml_risk,

            "risk_score": final_risk,

            "risk_level": final_risk_level,

            "high_risk_events": high,

            "medium_risk_events": medium,

            "low_risk_events": low,

            "latest_event": latest_event,

            "session_id": session_id

        })

    connection.close()

    return result