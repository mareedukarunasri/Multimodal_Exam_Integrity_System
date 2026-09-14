# Database Documentation

## Multimodal AI-Based Exam Cheating Behaviour Analysis System

The project uses **SQLite** as the local database for storing examination sessions and monitoring events.

---

## 1. Database Technology

The database technology used is:

```text
SQLite
```

The database file is created automatically by the backend:

```text
backend/exam_events.db
```

The database is intentionally excluded from GitHub because it contains local runtime examination data.

---

## 2. Database Architecture

The database stores information generated during examination sessions.

```text
Browser Monitoring
       |
Camera Monitoring
       |
Microphone / Behaviour Monitoring
       |
       v
FastAPI Backend
       |
       v
SQLite Database
       |
       +-------------------+
       |                   |
       v                   v
browser_events       exam_sessions
       |                   |
       +---------+---------+
                 |
                 v
           Risk Analysis
                 |
                 v
             Dashboard
```

---

## 3. Browser Events Table

The `browser_events` table stores browser monitoring events generated during an examination.

### Main Fields

| Field        | Description                      |
| ------------ | -------------------------------- |
| `id`         | Unique event ID                  |
| `student_id` | Student identifier               |
| `event_type` | Type of browser event            |
| `event_time` | Time when event occurred         |
| `risk_score` | Risk score assigned to the event |
| `risk_level` | LOW, MEDIUM, or HIGH             |
| `session_id` | Examination session identifier   |

### Example Events

```text
copy
paste
cut
right_click
tab_hidden
tab_visible
window_blur
window_focus
fullscreen_exit
```

---

## 4. Examination Sessions Table

The `exam_sessions` table stores information about each examination attempt.

### Main Fields

| Field        | Description                   |
| ------------ | ----------------------------- |
| `session_id` | Unique examination session ID |
| `student_id` | Student identifier            |
| `started_at` | Examination start time        |
| `ended_at`   | Examination end time          |
| `status`     | Current session status        |

### Session Status

A session can be tracked using statuses such as:

```text
active
completed
```

---

## 5. Session-Based Event Storage

Each monitoring event is associated with an examination session using `session_id`.

```text
Student
   |
   v
Start Examination
   |
   v
Generate Session ID
   |
   v
Monitoring Events
   |
   +---- Browser Events
   |
   +---- Camera Events
   |
   +---- Behaviour Events
   |
   v
Store with Session ID
```

This prevents events from different examination attempts from being mixed together.

---

## 6. Event Risk Information

Each detected event can contain risk information.

### Risk Score Ranges

| Risk Score  | Risk Level |
| ----------- | ---------- |
| 0.0 – 0.39  | LOW        |
| 0.40 – 0.69 | MEDIUM     |
| 0.70 – 1.00 | HIGH       |

### Examples

```text
copy
0.3
LOW
```

```text
tab_hidden
0.7
HIGH
```

```text
mobile_phone_detected
0.9
HIGH
```

---

## 7. Example Browser Event Record

A typical event stored in the database can contain:

```text
ID: 95
Student ID: S001
Event Type: tab_hidden
Event Time: 2026-09-14T10:20:00Z
Risk Score: 0.7
Risk Level: HIGH
Session ID: <exam-session-id>
```

---

## 8. Database Flow

The complete database flow is:

```text
Monitoring Module
       |
       v
Event Generated
       |
       v
FastAPI API
       |
       v
Risk Score Calculation
       |
       v
SQLite Database
       |
       v
Retrieve Session Data
       |
       v
Risk Analysis
       |
       v
Dashboard
```

---

## 9. Database Operations

The backend performs operations such as:

### Create Database

Creates the SQLite database and required tables.

### Store Event

Stores a monitoring event with its student ID, event type, timestamp, risk information, and session ID.

### Create Session

Creates a new examination session.

### End Session

Updates the examination session when the examination is completed.

### Retrieve Events

Retrieves events belonging to a particular examination session.

### Retrieve Risk Summary

Calculates and retrieves student risk information from stored events.

---

## 10. Database and Machine Learning

The database provides examination event information that can also be used by the machine learning module.

```text
SQLite Events
      |
      v
Extract Browser Features
      |
      v
Machine Learning Model
      |
      v
Prediction
```

Browser-event counts such as tab hiding, window blur, copy, paste, cut, fullscreen exit, and total events can be used as machine learning input features.

---

## 11. Database and Dashboard

The dashboard retrieves processed information from the backend.

```text
SQLite Database
       |
       v
FastAPI Backend
       |
       v
Student Risk API
       |
       v
Dashboard
```

The dashboard can display:

* Total events
* High-risk events
* Medium-risk events
* Low-risk events
* Browser risk
* Camera risk
* Behaviour risk
* ML prediction
* Final risk
* Event history

---

## 12. Data Privacy

The SQLite database contains examination monitoring information and should therefore be treated as sensitive project data.

Important considerations:

* Examination data should be stored securely.
* Access should be restricted to authorized users.
* Real student information should not be exposed unnecessarily.
* Test data should preferably use anonymized student IDs.
* Runtime database files should not be committed to public repositories.

The project's `.gitignore` excludes:

```text
backend/exam_events.db
```

from Git tracking.

---

## 13. Database Testing

The database was tested by verifying:

* Browser events are stored.
* Camera events are stored.
* Risk scores are stored.
* Risk levels are stored.
* Student IDs are stored.
* Session IDs are stored.
* Event timestamps are stored.
* Examination sessions are created.
* Examination sessions can be ended.
* Events can be retrieved for a selected session.

### Result

The SQLite database successfully stored and retrieved examination session and monitoring event information.

---

## Conclusion

SQLite provides a lightweight local storage solution for the examination monitoring prototype.

The session-based database design ensures that browser, camera, and behavioural events can be associated with the correct examination attempt. The stored information is then used by the risk analysis, machine learning, and dashboard modules.
