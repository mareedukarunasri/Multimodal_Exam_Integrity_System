from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.browser_monitor import analyze_browser_event

from app.database import (
    create_database,
    save_browser_event,
    get_all_browser_events,
    get_student_wise_summary,
    create_exam_session,
    end_exam_session,
    get_exam_session,
    get_active_exam_session
)

from app.ml.predict import get_ml_prediction


app = FastAPI(title="Exam Integrity Backend")


# ============================================================
# CREATE DATABASE
# ============================================================

create_database()


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# BROWSER EVENT MODEL
# ============================================================

class BrowserEvent(BaseModel):

    student_id: str

    event_type: str

    event_time: str | None = None

    session_id: str | None = None


# ============================================================
# CAMERA EVENT MODEL
# ============================================================

class CameraEvent(BaseModel):

    student_id: str

    event_type: str

    event_time: str | None = None

    session_id: str | None = None


# ============================================================
# EXAM START MODEL
# ============================================================

class ExamStartRequest(BaseModel):

    student_id: str


# ============================================================
# EXAM END MODEL
# ============================================================

class ExamEndRequest(BaseModel):

    session_id: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Exam Integrity Backend is running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# ============================================================
# START EXAM SESSION
# ============================================================

@app.post("/api/exam/start")
def start_exam(
    request: ExamStartRequest
):

    # --------------------------------------------------------
    # Check whether student already has an active session
    # --------------------------------------------------------

    active_session = get_active_exam_session(
        request.student_id
    )

    if active_session:

        return {
            "status": "already_active",
            "message": "An exam session is already active.",
            "session": active_session
        }

    # --------------------------------------------------------
    # Create new session
    # --------------------------------------------------------

    session = create_exam_session(
        request.student_id
    )

    return {
        "status": "exam_started",
        "message": "Exam session started successfully.",
        "session": session
    }


# ============================================================
# END EXAM SESSION
# ============================================================

@app.post("/api/exam/end")
def end_exam(
    request: ExamEndRequest
):

    # --------------------------------------------------------
    # Check session
    # --------------------------------------------------------

    session = get_exam_session(
        request.session_id
    )

    if session is None:

        return {
            "status": "error",
            "message": "Exam session not found."
        }

    # --------------------------------------------------------
    # Already completed
    # --------------------------------------------------------

    if session["status"] == "completed":

        return {
            "status": "already_completed",
            "message": "Exam session is already completed.",
            "session": session
        }

    # --------------------------------------------------------
    # End session
    # --------------------------------------------------------

    ended_session = end_exam_session(
        request.session_id
    )

    return {
        "status": "exam_ended",
        "message": "Exam session ended successfully.",
        "session": ended_session
    }


# ============================================================
# GET ALL EVENTS
#
# Optional:
# /api/browser-events
#
# OR:
# /api/browser-events?session_id=XXXXX
# ============================================================

@app.get("/api/browser-events")
def get_browser_events(
    session_id: str | None = None
):

    events = get_all_browser_events(
        session_id
    )

    return {
        "total_events": len(events),
        "session_id": session_id,
        "events": events
    }


# ============================================================
# STUDENT RISK SUMMARY
#
# Optional:
# /api/student-risk
#
# OR:
# /api/student-risk?session_id=XXXXX
# ============================================================

@app.get("/api/student-risk")
def get_student_risk(
    session_id: str | None = None
):

    students = get_student_wise_summary(
        session_id
    )

    return {
        "session_id": session_id,
        "students": students
    }


# ============================================================
# ML PREDICTION
# ============================================================

@app.get("/api/ml-prediction")
def ml_prediction(session_id: str | None = None):

    result = get_ml_prediction(
        session_id=session_id
    )

    return result

# ============================================================
# BROWSER EVENT API
# ============================================================

@app.post("/api/browser-events")
def receive_browser_event(
    event: BrowserEvent
):

    # --------------------------------------------------------
    # Analyze browser event
    # --------------------------------------------------------

    analysis_result = analyze_browser_event(
        event.event_type
    )

    # --------------------------------------------------------
    # Save browser event
    # --------------------------------------------------------

    save_browser_event(

        event.student_id,

        event.event_type,

        event.event_time,

        analysis_result["risk_score"],

        analysis_result["risk_level"],

        event.session_id

    )

    return {

        "status":
            "received and saved",

        "student_id":
            event.student_id,

        "event_type":
            event.event_type,

        "event_time":
            event.event_time,

        "session_id":
            event.session_id,

        "analysis":
            analysis_result
    }


# ============================================================
# CAMERA EVENT API
# ============================================================

@app.post("/api/camera-events")
def receive_camera_event(
    event: CameraEvent
):

    # ========================================================
    # CAMERA RISK LEVELS
    # ========================================================

    camera_risk_scores = {

        # ----------------------------------------------------
        # Normal
        # ----------------------------------------------------

        "face_detected": {

            "risk_score":
                0.0,

            "risk_level":
                "normal"
        },


        # ----------------------------------------------------
        # No Face
        # ----------------------------------------------------

        "no_face_detected": {

            "risk_score":
                0.7,

            "risk_level":
                "high"
        },


        # ----------------------------------------------------
        # Multiple Faces
        # ----------------------------------------------------

        "multiple_faces_detected": {

            "risk_score":
                0.9,

            "risk_level":
                "high"
        },


        # ----------------------------------------------------
        # Looking Left
        # ----------------------------------------------------

        "looking_left": {

            "risk_score":
                0.5,

            "risk_level":
                "medium"
        },


        # ----------------------------------------------------
        # Looking Right
        # ----------------------------------------------------

        "looking_right": {

            "risk_score":
                0.5,

            "risk_level":
                "medium"
        },


        # ----------------------------------------------------
        # Head Looking Away
        # ----------------------------------------------------

        "head_looking_away": {

            "risk_score":
                0.8,

            "risk_level":
                "high"
        },


        # ----------------------------------------------------
        # Mobile Phone Detected
        # ----------------------------------------------------

        "mobile_phone_detected": {

            "risk_score":
                0.9,

            "risk_level":
                "high"
        },


        # ----------------------------------------------------
        # Speech Detected
        # ----------------------------------------------------

        "speech_detected": {

            "risk_score":
                0.8,

            "risk_level":
                "high"
        }
    }


    # ========================================================
    # GET RISK ANALYSIS
    # ========================================================

    analysis_result = camera_risk_scores.get(

        event.event_type,

        {
            "risk_score":
                0.0,

            "risk_level":
                "normal"
        }
    )


    # ========================================================
    # SAVE CAMERA EVENT
    # ========================================================

    save_browser_event(

        event.student_id,

        event.event_type,

        event.event_time,

        analysis_result["risk_score"],

        analysis_result["risk_level"],

        event.session_id

    )


    # ========================================================
    # RESPONSE
    # ========================================================

    return {

        "status":
            "camera event received and saved",

        "student_id":
            event.student_id,

        "event_type":
            event.event_type,

        "event_time":
            event.event_time,

        "session_id":
            event.session_id,

        "analysis":
            analysis_result
    }