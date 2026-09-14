# Database Documentation

## 1. Overview

The Multimodal AI-Based Exam Cheating Behaviour Analysis System uses **SQLite** to store examination sessions and detected monitoring events.

The database is lightweight, local, and suitable for the academic prototype.

---

## 2. Database Technology

* Database: SQLite
* Database File: `backend/exam_events.db`
* Database Access: Python `sqlite3`
* Storage Type: Local relational database

The database file is generated automatically when the backend starts and is excluded from GitHub because it contains runtime data.

---

## 3. Database Tables

The system mainly uses two tables:

1. `exam_sessions`
2. `browser_events`

---

## 4. Exam Sessions Table

The `exam_sessions` table stores information about individual examination sessions.

### Main Fields

| Field        | Description                            |
| ------------ | -------------------------------------- |
| `session_id` | Unique identifier for the exam session |
| `student_id` | Unique student identifier              |
| `start_time` | Examination start time                 |
| `end_time`   | Examination end time                   |
| `status`     | Current session status                 |

### Purpose

This table allows the system to:

* Start a new examination session
* Track the active session
* Identify completed sessions
* Associate monitoring events with a particular examination

---

## 5. Browser Events Table

The `browser_events` table stores events detected from the student's browser.

### Main Fields

| Field        | Description                      |
| ------------ | -------------------------------- |
| `id`         | Unique event ID                  |
| `student_id` | Student identifier               |
| `event_type` | Type of browser event            |
| `event_time` | Time when the event occurred     |
| `risk_score` | Risk score assigned to the event |
| `risk_level` | LOW, MEDIUM, or HIGH             |
| `session_id` | Associated examination session   |

### Example Events

* `copy`
* `paste`
* `cut`
* `right_click`
* `tab_hidden`
* `tab_visible`
* `window_blur`
* `window_focus`
* `fullscreen_exit`

---

## 6. Risk Score Storage

Each detected event can be assigned a risk score.

| Risk Score  | Risk Level |
| ----------- | ---------- |
| 0.0 – 0.39  | LOW        |
| 0.40 – 0.69 | MEDIUM     |
| 0.70 – 1.00 | HIGH       |

These values are used by the risk analysis module to calculate the student's overall behaviour risk.

---

## 7. Session-Based Data

Each browser event is associated with a `session_id`.

This prevents events from different examinations from being mixed together.

For example:

```text
Session A
   ├── tab_hidden
   ├── copy
   └── window_blur

Session B
   ├── paste
   ├── fullscreen_exit
   └── tab_hidden
```

The dashboard can therefore display data for a specific examination session.

---

## 8. Database Operations

The backend performs the following database operations:

### Create Database

Creates the SQLite database and required tables.

### Insert Event

Stores a newly detected monitoring event.

### Retrieve Events

Retrieves browser events for a student or examination session.

### Start Session

Creates a new examination session.

### End Session

Marks an examination session as completed.

### Retrieve Session

Retrieves information about a particular examination session.

### Risk Calculation

Retrieves stored events and calculates risk information for the student.

---

## 9. Data Flow

```text
Browser / Camera / Behaviour Monitoring
                ↓
          Risk Analysis
                ↓
          Backend API
                ↓
          SQLite Database
                ↓
       Student Risk Analysis
                ↓
             Dashboard
```

---

## 10. Database and Multimodal Analysis

The database stores monitoring information that can be used by the multimodal risk analysis system.

The system combines information from:

* Browser monitoring
* Camera monitoring
* Behaviour monitoring
* Machine learning prediction

The resulting risk information is presented on the dashboard.

---

## 11. Example Stored Event

Example browser event:

```text
Student ID: S001
Event Type: tab_hidden
Event Time: 2026-09-13T15:23:37.300Z
Risk Score: 0.70
Risk Level: HIGH
Session ID: bf0d0803-091d-401b-aa11-14589f6e1f05
```

---

## 12. Database Security and Privacy

The project is an academic prototype. Examination monitoring data is stored locally in the SQLite database.

The database file is not committed to GitHub because it contains runtime examination data.

The system should be used only with appropriate student awareness and institutional permission.

---

## 13. Database File and Git

The database file is excluded using `.gitignore`:

```text
backend/exam_events.db
```

This keeps runtime examination data separate from the source code repository.

---

## 14. Conclusion

SQLite provides a simple and reliable storage layer for the project.

It enables the system to maintain:

* Examination sessions
* Student identifiers
* Browser events
* Event timestamps
* Risk scores
* Risk levels
* Session associations

This stored information supports the risk analysis and dashboard components of the Multimodal AI-Based Exam Cheating Behaviour Analysis System.
