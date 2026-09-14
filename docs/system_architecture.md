# System Architecture

## Multimodal AI-Based Exam Cheating Behaviour Analysis System

### 1. Overview

The system is designed to monitor and analyze multiple behavioural signals during an online examination and identify potentially suspicious or cheating-related behaviour.

The system combines:

* Browser activity monitoring
* Camera-based behaviour monitoring
* Microphone-based activity monitoring
* Machine Learning prediction
* Multimodal risk analysis
* Real-time dashboard visualization

The different signals are collected independently and combined to calculate an overall examination risk level.

---

## 2. High-Level Architecture

```text
                    ONLINE EXAM
                         |
                         v
              +---------------------+
              |   Exam Interface    |
              |     exam.html       |
              +----------+----------+
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
   Browser Monitor   Camera Monitor   Microphone
          |              |              |
          v              v              v
   Browser Events   Camera Events   Behaviour Events
          |              |              |
          +--------------+--------------+
                         |
                         v
                 +---------------+
                 | FastAPI Backend|
                 +-------+-------+
                         |
                         v
                  +-------------+
                  | SQLite DB   |
                  | exam_events |
                  +------+------+
                         |
             +-----------+-----------+
             |                       |
             v                       v
      Risk Analysis             ML Prediction
             |                       |
             +-----------+-----------+
                         |
                         v
                  Multimodal Fusion
                         |
                         v
                +----------------+
                | Risk Assessment|
                +-------+--------+
                        |
                        v
                +---------------+
                |   Dashboard   |
                | dashboard.html|
                +---------------+
```

---

## 3. Major Components

### 3.1 Exam Interface

The exam interface provides the environment in which the student attends the examination.

Main file:

```text
frontend/test/exam.html
```

It starts the exam session and loads the required monitoring components.

---

### 3.2 Browser Monitoring

Browser monitoring detects activities that may indicate suspicious behaviour.

Examples include:

* Copy
* Paste
* Cut
* Right-click
* Tab hidden
* Tab visible
* Window blur
* Window focus
* Full-screen exit

Main file:

```text
frontend/src/monitoring/browserMonitor.js
```

Browser events are sent to the FastAPI backend.

---

### 3.3 Camera Monitoring

The camera monitoring module analyzes the student's visual behaviour.

The system can detect events such as:

* No face detected
* Looking left
* Looking right
* Head movement
* Mobile phone detected
* Other suspicious visual behaviour

Main file:

```text
frontend/src/monitoring/camera_monitor.js
```

Camera events are sent to the backend with the active examination session ID.

---

### 3.4 Microphone Monitoring

The microphone monitoring component analyzes audio activity during the examination.

It can identify voice/talking activity using microphone input and generate behavioural events when suspicious audio activity is detected.

The system can also provide an audio warning or alert when required.

---

### 3.5 FastAPI Backend

The backend provides APIs for communication between the frontend monitoring modules, database and analysis components.

Main files:

```text
backend/app/main.py
backend/app/database.py
```

The backend is responsible for:

* Starting examination sessions
* Ending examination sessions
* Receiving browser events
* Receiving camera events
* Storing events
* Retrieving session events
* Calculating risk
* Providing ML predictions
* Providing dashboard data

---

### 3.6 SQLite Database

The system uses SQLite for local event storage.

Database file:

```text
backend/exam_events.db
```

The database stores:

* Examination sessions
* Browser events
* Camera events
* Risk-related information
* Session identifiers
* Event timestamps

The database file is generated locally at runtime and is intentionally excluded from GitHub.

---

### 3.7 Machine Learning Module

The ML module uses a Random Forest classifier to predict whether the observed browser behaviour is normal or suspicious.

Main files:

```text
backend/app/ml/dataset.csv
backend/app/ml/train_model.py
backend/app/ml/predict.py
```

The model uses behavioural features such as:

* Tab hidden count
* Window blur count
* Copy count
* Paste count
* Cut count
* Full-screen exit count
* Total event count

The prediction result can be:

```text
NORMAL
```

or

```text
CHEATING / SUSPICIOUS
```

---

### 3.8 Multimodal Risk Analysis

The system does not depend on a single monitoring source.

Risk information is obtained from multiple modalities:

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
Multimodal Risk Assessment
```

This approach allows the system to consider multiple behavioural signals before producing the final risk assessment.

---

### 3.9 Dashboard

The dashboard displays the collected examination information in a user-friendly format.

Main file:

```text
frontend/test/dashboard.html
```

The dashboard can display:

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
* Final risk
* Final risk level
* Event history

---

## 4. Session-Based Architecture

Each examination is associated with an examination session ID.

Example:

```text
Student
   |
   v
Start Exam
   |
   v
Generate Session ID
   |
   +---- Browser Events
   |
   +---- Camera Events
   |
   +---- Behaviour Events
   |
   v
Store Events with Session ID
   |
   v
Analyze Current Session
   |
   v
Display Risk on Dashboard
```

This prevents events from previous examinations from being incorrectly included in the current examination's risk calculation.

---

## 5. Data Flow

The overall data flow is:

```text
Student
   |
   v
Exam Interface
   |
   +-------------------+
   |                   |
   v                   v
Browser Monitoring   Camera Monitoring
   |                   |
   +---------+---------+
             |
             v
        FastAPI Backend
             |
             v
        SQLite Database
             |
      +------+------+
      |             |
      v             v
Risk Analysis    ML Prediction
      |             |
      +------+------+
             |
             v
     Multimodal Fusion
             |
             v
        Final Risk
             |
             v
         Dashboard
```

---

## 6. Backend API Layer

The main API operations include:

```text
POST /api/exam/start
POST /api/exam/end
POST /api/browser-events
POST /api/camera-events
GET  /api/student-risk
GET  /api/ml-prediction
GET  /health
```

These APIs provide communication between the monitoring modules, backend services and dashboard.

---

## 7. Risk Levels

The system categorizes observed behaviour into different risk levels.

```text
NORMAL
LOW
MEDIUM
HIGH
```

Individual events can contribute different risk scores depending on their type and severity.

The final assessment considers the combined information from the available monitoring modalities.

---

## 8. Design Goals

The architecture is designed to provide:

1. Real-time monitoring
2. Session-specific event tracking
3. Multimodal behavioural analysis
4. Machine Learning-based prediction
5. Centralized event storage
6. Risk-level classification
7. Dashboard-based visualization
8. Modular system design
9. Extensibility for future AI models

---

## 9. Future Extensions

The architecture can be extended with:

* Advanced facial behaviour analysis
* Eye-gaze estimation
* Object detection improvements
* Speech-to-text analysis
* Advanced audio classification
* Deep Learning models
* Improved multimodal fusion
* Historical student behaviour analysis
* Cloud-based deployment
* Authentication and role-based access
* Automated examination reports

---

## 10. Conclusion

The proposed architecture combines browser, visual and audio behavioural signals with Machine Learning and risk analysis.

The modular architecture allows each monitoring component to operate independently while the backend provides centralized event management and the dashboard presents the final analysis.

This design provides a foundation for developing a scalable and extensible AI-assisted examination integrity system.
