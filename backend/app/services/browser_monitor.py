# backend/app/services/browser_monitor.py

def analyze_browser_event(event_type: str) -> dict:
    suspicious_events = {
        "copy": 0.30,
        "paste": 0.50,
        "cut": 0.40,
        "right_click": 0.20,
        "tab_hidden": 0.70,
        "tab_visible": 0.00,
        "window_blur": 0.60,
        "window_focus": 0.00,
        "fullscreen_exit": 0.80,
        "normal_activity": 0.00,
        "exam_started": 0.00,
        "exam_submitted": 0.00
    }

    risk_score = suspicious_events.get(event_type, 0.0)

    if risk_score >= 0.70:
        risk_level = "high"
    elif risk_score >= 0.40:
        risk_level = "medium"
    elif risk_score > 0:
        risk_level = "low"
    else:
        risk_level = "normal"

    return {
        "event_type": event_type,
        "risk_score": risk_score,
        "risk_level": risk_level
    }