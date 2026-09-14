# Testing Documentation

## 1. Overview

The **Multimodal AI-Based Exam Cheating Behaviour Analysis System** was tested to verify that its monitoring modules, backend services, database, machine learning prediction, risk analysis, and dashboard work correctly together.

Testing was performed using the complete examination workflow.

---

## 2. Testing Environment

| Component        | Technology            |
| ---------------- | --------------------- |
| Operating System | Windows               |
| Frontend         | HTML, CSS, JavaScript |
| Backend          | Python, FastAPI       |
| Database         | SQLite                |
| Machine Learning | Scikit-learn          |
| Browser          | Google Chrome         |
| Camera           | Webcam                |
| Audio            | Microphone            |

---

## 3. Browser Monitoring Testing

The browser monitoring module was tested using different browser activities.

| Test Event         | Expected Result            |
| ------------------ | -------------------------- |
| Copy text          | Copy event detected        |
| Paste text         | Paste event detected       |
| Cut text           | Cut event detected         |
| Right click        | Right-click event detected |
| Switch tab         | Tab hidden event detected  |
| Return to exam tab | Tab visible event detected |
| Change window      | Window blur detected       |
| Return to window   | Window focus detected      |
| Exit fullscreen    | Fullscreen exit detected   |

Detected events are sent to the backend and stored in the database.

---

## 4. Camera Monitoring Testing

The camera monitoring module was tested using different student behaviours.

| Test Condition       | Expected Result               |
| -------------------- | ----------------------------- |
| Face visible         | Face detected                 |
| Face not visible     | No-face event detected        |
| Student looks left   | Looking-left event detected   |
| Student looks right  | Looking-right event detected  |
| Student looks away   | Suspicious behaviour detected |
| Mobile phone visible | Mobile-phone event detected   |

Camera events are converted into risk scores.

---

## 5. Microphone Monitoring Testing

The microphone monitoring module was tested for audio activity.

| Test Condition            | Expected Result                 |
| ------------------------- | ------------------------------- |
| No talking                | Normal audio state              |
| Student speaks            | Talking/audio activity detected |
| Continuous audio activity | Behaviour risk signal generated |

---

## 6. Risk Analysis Testing

Risk scores were tested using different event types.

| Risk Score  | Risk Level |
| ----------- | ---------- |
| 0.0 – 0.39  | LOW        |
| 0.40 – 0.69 | MEDIUM     |
| 0.70 – 1.00 | HIGH       |

The system correctly maps detected event scores to their corresponding risk levels.

---

## 7. Machine Learning Testing

The Random Forest model was tested using the available browser behaviour features.

### Input Features

* Tab hidden
* Window blur
* Copy
* Paste
* Cut
* Fullscreen exit
* Total events

### Expected Output

```text
NORMAL
```

or

```text
CHEATING / SUSPICIOUS
```

The ML prediction is displayed in the student risk analysis and dashboard.

---

## 8. Database Testing

The SQLite database was tested to verify that monitoring information is stored correctly.

### Verified Data

* Student ID
* Event type
* Event time
* Risk score
* Risk level
* Session ID
* Examination session details

The stored events can be retrieved successfully for risk analysis and dashboard display.

---

## 9. API Testing

The following backend APIs were tested:

| Endpoint              | Test Result |
| --------------------- | ----------- |
| `/health`             | Passed      |
| `/api/exam/start`     | Passed      |
| `/api/exam/end`       | Passed      |
| `/api/browser-events` | Passed      |
| `/api/student-risk`   | Passed      |
| `/api/ml-prediction`  | Passed      |

---

## 10. Dashboard Testing

The dashboard was tested to verify that the monitoring results are displayed correctly.

### Verified Dashboard Information

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
* Event history

---

## 11. End-to-End Testing

The complete system was tested using an active examination session.

### Example Test Result

```text
Total Events: 39
High Risk Events: 9
Medium Risk Events: 12
Low Risk Events: 1
Normal Events: 17

Browser Risk: 38%
Camera Risk: 40%
Behaviour Risk: 38%
ML Risk: 0%

Final Risk: 40%
Final Risk Level: MEDIUM
```

The system successfully collected monitoring events, calculated risk scores, generated an ML prediction, performed multimodal risk analysis, and displayed the results on the dashboard.

---

## 12. Test Conclusion

The testing confirms that the major components of the system work together successfully.

The system can:

* Monitor browser behaviour.
* Monitor camera-based behaviour.
* Monitor microphone activity.
* Store monitoring events.
* Calculate risk scores.
* Generate machine learning predictions.
* Combine multiple monitoring signals.
* Display the final assessment through the dashboard.

The project is therefore ready for demonstration and further evaluation.
