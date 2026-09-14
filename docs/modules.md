# Project Modules

## 1. Student / Exam Interface

The exam interface provides the environment where the student attends the online examination.

### Main Functions

* Displays examination questions.
* Allows students to submit answers.
* Starts and ends the examination session.
* Connects the exam interface with monitoring modules.
* Maintains the active examination session.

---

## 2. Browser Monitoring

The browser monitoring module detects suspicious browser-related activities during the examination.

### Detected Events

| Event           | Description                    |
| --------------- | ------------------------------ |
| Copy            | Student copies content         |
| Paste           | Student pastes content         |
| Cut             | Student cuts content           |
| Right Click     | Student performs a right-click |
| Tab Hidden      | Exam tab becomes hidden        |
| Tab Visible     | Exam tab becomes visible       |
| Window Blur     | Exam window loses focus        |
| Window Focus    | Exam window regains focus      |
| Fullscreen Exit | Student exits fullscreen mode  |

Each detected event is assigned a risk score and stored in the database.

---

## 3. Camera Monitoring

The camera monitoring module analyzes the student's visual behaviour using the webcam.

### Detection Capabilities

* Face detection
* No-face detection
* Looking-left detection
* Looking-right detection
* Looking-away behaviour
* Mobile phone detection

Camera events are converted into risk scores and sent to the backend for further analysis.

---

## 4. Microphone Monitoring

The microphone monitoring module observes audio activity during the examination.

### Detection

* Detects voice or talking activity.
* Generates an audio-related risk signal.
* Supports multimodal behaviour analysis.

The microphone module provides an additional behavioural signal along with browser and camera monitoring.

---

## 5. Risk Analysis

The risk analysis module calculates risk scores from detected events.

### Risk Levels

| Risk Score  | Risk Level |
| ----------- | ---------- |
| 0.0 – 0.39  | LOW        |
| 0.40 – 0.69 | MEDIUM     |
| 0.70 – 1.00 | HIGH       |

Higher risk scores indicate a greater possibility of suspicious examination behaviour.

---

## 6. Machine Learning Prediction

The project uses a **Random Forest Classifier** for machine-learning-based behaviour prediction.

### Input Features

* Tab hidden events
* Window blur events
* Copy events
* Paste events
* Cut events
* Fullscreen exit events
* Total browser events

### Prediction Output

The ML model predicts:

* **NORMAL**
* **CHEATING / SUSPICIOUS**

The ML prediction is used as an additional signal during multimodal risk assessment.

---

## 7. Multimodal Risk Fusion

The multimodal fusion module combines information from different monitoring sources.

### Input Signals

* Browser risk
* Camera risk
* Behaviour risk
* ML prediction
* ML risk

The combined information is used to generate the final student risk assessment.

---

## 8. Database Module

The system uses **SQLite** to store examination monitoring data.

### Stored Information

* Student ID
* Event type
* Event time
* Risk score
* Risk level
* Session ID
* Examination session information

The database allows monitoring events and student risk information to be retrieved for dashboard analysis.

---

## 9. Dashboard

The dashboard provides a centralized view of the examination monitoring results.

### Dashboard Information

* Total events
* High-risk events
* Medium-risk events
* Low-risk events
* Normal events
* Browser risk
* Camera risk
* Behaviour risk
* ML prediction
* ML risk
* Final risk score
* Final risk level
* Detected events

The dashboard helps the examiner understand the overall behaviour and risk status of a student.

---

## 10. Backend API

The backend is implemented using **FastAPI**.

### Main API Operations

| API                   | Purpose                         |
| --------------------- | ------------------------------- |
| `/api/exam/start`     | Start an examination session    |
| `/api/exam/end`       | End an examination session      |
| `/api/browser-events` | Store browser monitoring events |
| `/api/student-risk`   | Calculate student risk          |
| `/api/ml-prediction`  | Generate ML prediction          |
| `/health`             | Check backend status            |

---

## 11. Overall Processing Flow

```text
Student
   ↓
Exam Interface
   ↓
Multimodal Monitoring
   ├── Browser Monitoring
   ├── Camera Monitoring
   └── Microphone Monitoring
   ↓
Risk Analysis
   ↓
Machine Learning Prediction
   ↓
Multimodal Risk Fusion
   ↓
Monitoring Dashboard
```

---

## 12. Module Summary

| Module                | Main Purpose                            |
| --------------------- | --------------------------------------- |
| Exam Interface        | Conducts the online examination         |
| Browser Monitoring    | Detects suspicious browser activity     |
| Camera Monitoring     | Detects visual suspicious behaviour     |
| Microphone Monitoring | Detects audio/talking activity          |
| Risk Analysis         | Calculates risk scores                  |
| ML Prediction         | Predicts normal or suspicious behaviour |
| Multimodal Fusion     | Combines multiple risk signals          |
| Database              | Stores monitoring information           |
| Backend API           | Handles system communication            |
| Dashboard             | Displays monitoring and risk results    |
