# Project Modules

## Multimodal AI-Based Exam Cheating Behaviour Analysis System

This document describes the major modules implemented in the Multimodal AI-Based Exam Cheating Behaviour Analysis System.

---

## 1. Exam Interface Module

The Exam Interface provides the environment in which the student attends the online examination.

### Responsibilities

* Displays the examination interface.
* Starts an examination session.
* Generates a unique session ID.
* Enables browser, camera, and microphone monitoring.
* Provides a controlled environment for examination monitoring.
* Sends monitoring events to the backend.

---

## 2. Exam Session Management Module

The Exam Session Management module manages the beginning and end of each examination session.

### Responsibilities

* Creates a unique session ID.
* Records the student ID.
* Records session start time.
* Tracks the session status.
* Records session end time.
* Associates monitoring events with the correct examination session.

### Example

```text
Student S001
     |
     v
Start Exam
     |
     v
Generate Session ID
     |
     v
Monitor Student
     |
     v
End Exam
```

Session-based monitoring prevents events from different examination attempts from being mixed together.

---

## 3. Browser Monitoring Module

The Browser Monitoring module detects suspicious browser and user interaction events during the examination.

### Detected Events

* Tab hidden
* Tab visible
* Window blur
* Window focus
* Copy
* Paste
* Cut
* Right click
* Fullscreen exit

### Example

```text
Student switches to another tab
              |
              v
       tab_hidden event
              |
              v
        Risk calculation
              |
              v
       Event stored in DB
```

Browser events are sent to the FastAPI backend and stored in the SQLite database.

---

## 4. Camera Monitoring Module

The Camera Monitoring module uses the student's webcam to identify suspicious visual behaviour.

### Responsibilities

* Accesses the webcam.
* Detects the presence of a face.
* Detects absence of a face.
* Detects head movement.
* Detects looking-left behaviour.
* Detects looking-right behaviour.
* Detects mobile phone usage.
* Generates camera-based risk events.

### Examples of Events

```text
no_face_detected
looking_left
looking_right
mobile_phone_detected
```

Camera monitoring provides the visual component of the multimodal system.

---

## 5. Microphone Monitoring Module

The Microphone Monitoring module analyzes audio activity during the examination.

### Responsibilities

* Accesses the microphone.
* Measures microphone activity.
* Detects voice/talking activity.
* Generates talking-related events.
* Sends relevant behaviour information to the backend.

This module provides an additional behavioural signal that cannot be obtained from browser or camera monitoring alone.

---

## 6. Risk Analysis Module

The Risk Analysis module assigns risk scores to detected events.

Each detected event is assigned a risk score based on its potential relevance to suspicious examination behaviour.

### Risk Levels

| Risk Score  | Risk Level |
| ----------- | ---------- |
| 0.0 – 0.39  | LOW        |
| 0.40 – 0.69 | MEDIUM     |
| 0.70 – 1.00 | HIGH       |

### Example

```text
copy                 -> 0.3 -> LOW
paste                -> 0.5 -> MEDIUM
window_blur          -> 0.6 -> MEDIUM
tab_hidden           -> 0.7 -> HIGH
mobile_phone_detected -> 0.9 -> HIGH
```

Risk scores from multiple monitoring sources are used to calculate the student's overall risk.

---

## 7. Machine Learning Module

The Machine Learning module predicts whether the observed browser behaviour is normal or suspicious.

### Algorithm

The current implementation uses:

**Random Forest Classifier**

### Input Features

The model uses browser-related features such as:

* tab hidden count
* window blur count
* copy count
* paste count
* cut count
* fullscreen exit count
* total event count

### Output

The model produces a prediction such as:

```text
NORMAL
```

or

```text
CHEATING / SUSPICIOUS
```

The model is trained using the project's browser-event dataset.

---

## 8. Multimodal Fusion Module

The Multimodal Fusion module combines information from multiple monitoring sources.

### Input Modalities

```text
Browser Monitoring
       |
Camera Monitoring
       |
Microphone Monitoring
       |
Machine Learning Prediction
       |
       v
Multimodal Fusion
       |
       v
Final Risk Analysis
```

The system does not depend on a single signal. Instead, information from different modalities contributes to the final assessment.

---

## 9. Backend API Module

The backend is implemented using **FastAPI**.

It provides APIs for communication between the frontend monitoring system, database, risk analysis components, and machine learning module.

### Main APIs

```text
POST /api/exam/start
POST /api/exam/end

POST /api/browser-events
POST /api/camera-events

GET /api/student-risk
GET /api/ml-prediction

GET /health
```

The backend validates incoming information and processes monitoring events.

---

## 10. Database Module

The project uses **SQLite** for local event and session storage.

### Main Data

The database stores:

* Browser events
* Camera events
* Risk scores
* Risk levels
* Student ID
* Session ID
* Event timestamps
* Examination session information

### Database Flow

```text
Monitoring Event
       |
       v
FastAPI Backend
       |
       v
SQLite Database
       |
       v
Risk Analysis
       |
       v
Dashboard
```

---

## 11. Dashboard Module

The Dashboard provides a visual summary of the examination monitoring results.

### Displays

* Total events
* High-risk events
* Medium-risk events
* Low-risk events
* Normal events
* Browser risk
* Camera risk
* Behaviour risk
* ML prediction
* Final risk
* Event history

The dashboard allows an evaluator or administrator to understand the student's examination behaviour.

---

## 12. Warning and Alert Module

The system provides real-time warnings when suspicious behaviour is detected.

### Alert Types

* Visual warning overlay
* Speech warning
* Siren/alert sound

For high-risk behaviour, the system can display a prominent warning to the student.

Example:

```text
Suspicious Behaviour Detected
Please return to the examination.
```

This module provides immediate feedback instead of waiting until the examination is completed.

---

## 13. Event Logging Module

Every detected monitoring event is recorded with important information.

### Example Event

```text
Student ID: S001
Event Type: mobile_phone_detected
Risk Score: 0.9
Risk Level: HIGH
Event Time: 2026-09-14T10:20:00
Session ID: <exam-session-id>
```

Event logging allows the system to maintain an auditable history of examination behaviour.

---

## 14. Student Risk Summary Module

The Student Risk Summary module combines the available monitoring information to calculate an overall risk assessment.

### Risk Components

```text
Browser Risk
     +
Camera Risk
     +
Behaviour Risk
     +
ML Prediction
     |
     v
Final Risk
```

The final result is categorized into levels such as:

```text
NORMAL
LOW
MEDIUM
HIGH
```

---

## 15. Privacy and Ethical Monitoring Module

The system is designed as an academic examination-monitoring prototype.

Important considerations include:

* Monitoring should be performed with appropriate user consent.
* Camera and microphone access should be clearly communicated.
* Collected examination data should be protected.
* Risk predictions should be treated as indicators rather than absolute proof of cheating.
* Human review should be considered before taking disciplinary action.
* The system should avoid unnecessary collection of personal information.

---

## Overall Module Architecture

```text
                    EXAM INTERFACE
                          |
            +-------------+-------------+
            |             |             |
            v             v             v
       BROWSER         CAMERA       MICROPHONE
       MONITORING      MONITORING    MONITORING
            |             |             |
            +-------------+-------------+
                          |
                          v
                   FASTAPI BACKEND
                          |
                          v
                    SQLITE DATABASE
                          |
              +-----------+-----------+
              |                       |
              v                       v
        RISK ANALYSIS          ML PREDICTION
              |                       |
              +-----------+-----------+
                          |
                          v
                  MULTIMODAL FUSION
                          |
                          v
                   FINAL RISK SCORE
                          |
                          v
                     DASHBOARD
```

---

## Conclusion

The project combines browser monitoring, camera-based analysis, microphone activity detection, risk scoring, machine learning, database storage, and multimodal fusion into a single examination integrity system.

The modular architecture allows individual components to be improved or replaced independently while maintaining communication through the backend API layer.
