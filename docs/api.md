# API Documentation

## Overview

The backend API is developed using **FastAPI** and provides communication between the frontend monitoring system, risk analysis modules, machine learning model, and database.

Backend URL:

```text
http://127.0.0.1:8000
```

---

## 1. Health Check

### Endpoint

```text
GET /health
```

### Purpose

Checks whether the backend server is running correctly.

### Example

```text
http://127.0.0.1:8000/health
```

### Response

```json
{
  "status": "ok"
}
```

---

## 2. Start Examination

### Endpoint

```text
POST /api/exam/start
```

### Purpose

Creates a new examination session for a student.

### Input

The request contains the student information required to start an examination session.

### Output

Returns the newly created examination session information, including the session ID.

---

## 3. End Examination

### Endpoint

```text
POST /api/exam/end
```

### Purpose

Ends an active examination session.

### Input

The session ID is used to identify the examination session.

### Output

Returns the updated examination session information.

---

## 4. Browser Events

### Endpoint

```text
POST /api/browser-events
```

### Purpose

Stores browser monitoring events generated during the examination.

### Example Event

```json
{
  "student_id": "S001",
  "event_type": "tab_hidden",
  "event_time": "2026-09-13T15:23:37.300Z",
  "session_id": "example-session-id"
}
```

### Supported Events

* `copy`
* `paste`
* `cut`
* `right_click`
* `tab_hidden`
* `tab_visible`
* `window_blur`
* `window_focus`
* `fullscreen_exit`

The backend assigns the appropriate risk score to each event and stores it in the SQLite database.

---

## 5. Student Risk Analysis

### Endpoint

```text
GET /api/student-risk
```

### Purpose

Calculates the student's overall examination risk using monitoring information.

### Risk Inputs

* Browser risk
* Camera risk
* Behaviour risk
* Machine learning prediction
* ML risk

### Output

The endpoint provides:

* Student ID
* Total events
* Risk scores
* Risk levels
* ML prediction
* Final risk score
* Final risk level

---

## 6. ML Prediction

### Endpoint

```text
GET /api/ml-prediction
```

### Purpose

Runs the trained Random Forest machine learning model to predict the student's behaviour.

### Model

```text
Random Forest Classifier
```

### Input Features

* Tab hidden
* Window blur
* Copy
* Paste
* Cut
* Fullscreen exit
* Total events

### Prediction

The model produces one of the following classifications:

```text
NORMAL
CHEATING / SUSPICIOUS
```

---

## 7. Session Filtering

Several monitoring endpoints can use the `session_id` parameter to retrieve data belonging to a particular examination session.

### Example

```text
/api/browser-events?session_id=example-session-id
```

This prevents events from different examination sessions from being mixed together.

---

## 8. Risk Levels

The system uses the following risk classification:

| Risk Score  | Risk Level |
| ----------- | ---------- |
| 0.0 – 0.39  | LOW        |
| 0.40 – 0.69 | MEDIUM     |
| 0.70 – 1.00 | HIGH       |

---

## 9. Backend Technology

The API layer uses:

| Technology   | Purpose                |
| ------------ | ---------------------- |
| FastAPI      | Backend API framework  |
| Uvicorn      | Application server     |
| SQLite       | Database               |
| Python       | Backend implementation |
| Scikit-learn | Machine learning       |

---

## 10. API Processing Flow

```text
Frontend
   ↓
FastAPI Backend
   ↓
Database / Risk Analysis / ML Model
   ↓
Risk Results
   ↓
Dashboard
```

---

## 11. Running the Backend

Open PowerShell and run:

```powershell
cd C:\Users\maree\OneDrive\Desktop\Multimodal_Exam_Integrity_System\backend
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```
