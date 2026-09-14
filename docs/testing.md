# Testing Documentation

## Multimodal AI-Based Exam Cheating Behaviour Analysis System

This document describes the testing performed on the major components of the examination monitoring system.

---

## 1. Testing Objectives

The main objectives of testing are:

* Verify that each monitoring module works correctly.
* Verify communication between frontend and backend.
* Verify that events are stored correctly in the database.
* Verify risk scores and risk levels.
* Verify machine learning predictions.
* Verify session-based event separation.
* Verify dashboard results.
* Verify the complete end-to-end system.

---

## 2. Browser Monitoring Testing

The browser monitoring module was tested by performing different browser interactions during an examination.

### Test Cases

| Test Case | Action               | Expected Result                   | Status |
| --------- | -------------------- | --------------------------------- | ------ |
| B01       | Copy text            | `copy` event generated            | PASS   |
| B02       | Paste text           | `paste` event generated           | PASS   |
| B03       | Cut text             | `cut` event generated             | PASS   |
| B04       | Right click          | `right_click` event generated     | PASS   |
| B05       | Switch tab           | `tab_hidden` event generated      | PASS   |
| B06       | Return to tab        | `tab_visible` event generated     | PASS   |
| B07       | Leave browser window | `window_blur` event generated     | PASS   |
| B08       | Return to browser    | `window_focus` event generated    | PASS   |
| B09       | Exit fullscreen      | `fullscreen_exit` event generated | PASS   |

### Result

Browser events were successfully detected and sent to the FastAPI backend.

---

## 3. Camera Monitoring Testing

The camera monitoring module was tested using the system webcam.

### Test Cases

| Test Case | Action                | Expected Result               | Status |
| --------- | --------------------- | ----------------------------- | ------ |
| C01       | Start camera          | Camera starts successfully    | PASS   |
| C02       | Face visible          | Face detected                 | PASS   |
| C03       | Move away from camera | `no_face_detected` event      | PASS   |
| C04       | Look left             | `looking_left` event          | PASS   |
| C05       | Look right            | `looking_right` event         | PASS   |
| C06       | Show mobile phone     | `mobile_phone_detected` event | PASS   |

### Result

The webcam was successfully accessed and visual behaviour events were generated.

---

## 4. Microphone Monitoring Testing

The microphone monitoring module was tested using microphone input.

### Test Cases

| Test Case | Action                | Expected Result           | Status |
| --------- | --------------------- | ------------------------- | ------ |
| M01       | Start microphone      | Microphone access granted | PASS   |
| M02       | Remain silent         | Normal audio activity     | PASS   |
| M03       | Speak near microphone | Talking activity detected | PASS   |
| M04       | Stop speaking         | Talking event stops       | PASS   |

### Result

The microphone monitoring module successfully detected audio activity and talking behaviour.

---

## 5. Risk Analysis Testing

The risk analysis system was tested using different event types.

### Test Cases

| Event                 | Risk Score | Expected Level | Status |
| --------------------- | ---------: | -------------- | ------ |
| Copy                  |        0.3 | LOW            | PASS   |
| Cut                   |        0.4 | MEDIUM         | PASS   |
| Paste                 |        0.5 | MEDIUM         | PASS   |
| Window blur           |        0.6 | MEDIUM         | PASS   |
| Tab hidden            |        0.7 | HIGH           | PASS   |
| Mobile phone detected |        0.9 | HIGH           | PASS   |

### Result

Risk scores were correctly converted into LOW, MEDIUM, and HIGH risk levels.

---

## 6. Database Testing

The SQLite database was tested to verify event and session storage.

### Verification Items

* Browser events stored correctly.
* Camera events stored correctly.
* Risk scores stored correctly.
* Risk levels stored correctly.
* Student ID stored correctly.
* Session ID stored correctly.
* Event timestamps stored correctly.
* Examination sessions stored correctly.

### Result

Monitoring events and examination sessions were successfully stored in SQLite.

---

## 7. Exam Session Testing

Session handling was tested to verify that events from different examination attempts are separated.

### Test Procedure

```text
Start Exam
    |
    v
Generate Session ID
    |
    v
Generate Monitoring Events
    |
    v
Store Events with Session ID
    |
    v
End Exam
    |
    v
Start New Exam
    |
    v
Generate New Session ID
```

### Result

Each examination attempt receives a separate session ID, preventing events from different sessions from being mixed.

---

## 8. Machine Learning Testing

The machine learning module was tested using the browser-event dataset.

### Algorithm Tested

```text
Random Forest Classifier
```

### Input Features

* Tab hidden count
* Window blur count
* Copy count
* Paste count
* Cut count
* Fullscreen exit count
* Total event count

### Test Result

The model successfully produced predictions such as:

```text
NORMAL
```

and

```text
CHEATING / SUSPICIOUS
```

The ML prediction was successfully integrated into the student risk analysis.

---

## 9. Multimodal Fusion Testing

The multimodal fusion system was tested using information from multiple monitoring sources.

### Input Sources

```text
Browser Monitoring
       +
Camera Monitoring
       +
Microphone Monitoring
       +
ML Prediction
       |
       v
Multimodal Risk Analysis
```

### Verification

The system successfully combined:

* Browser risk
* Camera risk
* Behaviour risk
* ML prediction

to produce a final risk assessment.

### Result

Multimodal information was successfully combined into the final student risk result.

---

## 10. Dashboard Testing

The dashboard was tested to verify that examination results are displayed correctly.

### Verified Information

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
* Final risk level
* Event history

### Result

The dashboard successfully displayed the monitoring and risk analysis results.

---

## 11. Warning and Alert Testing

The warning system was tested using high-risk events.

### Test Cases

| Test Case | Trigger              | Expected Result     | Status |
| --------- | -------------------- | ------------------- | ------ |
| A01       | High-risk event      | Red warning overlay | PASS   |
| A02       | Suspicious behaviour | Speech warning      | PASS   |
| A03       | High-risk behaviour  | Siren/alert sound   | PASS   |

### Result

Visual and audio warnings were successfully triggered for suspicious behaviour.

---

## 12. Backend API Testing

The FastAPI endpoints were tested to verify communication between frontend and backend.

### Tested APIs

| API                   | Method | Purpose                | Status |
| --------------------- | ------ | ---------------------- | ------ |
| `/health`             | GET    | Backend health check   | PASS   |
| `/api/exam/start`     | POST   | Start session          | PASS   |
| `/api/exam/end`       | POST   | End session            | PASS   |
| `/api/browser-events` | POST   | Store browser event    | PASS   |
| `/api/camera-events`  | POST   | Store camera event     | PASS   |
| `/api/student-risk`   | GET    | Retrieve risk summary  | PASS   |
| `/api/ml-prediction`  | GET    | Retrieve ML prediction | PASS   |

### Result

The tested API endpoints successfully communicated between the frontend and backend.

---

## 13. End-to-End Testing

A complete examination session was performed to verify the integrated system.

### Test Flow

```text
Open Examination
       |
       v
Start Exam Session
       |
       v
Generate Session ID
       |
       v
Start Browser Monitoring
       |
       v
Start Camera Monitoring
       |
       v
Start Microphone Monitoring
       |
       v
Generate Behaviour Events
       |
       v
Store Events in SQLite
       |
       v
Calculate Risk
       |
       v
Run ML Prediction
       |
       v
Multimodal Fusion
       |
       v
Display Dashboard
       |
       v
End Exam
```

### Final Integration Test

A fresh end-to-end test session was successfully completed.

```text
Session ID:
bf0d0803-091d-401b-aa11-14589f6e1f05

Total Events: 39

High Risk Events: 9
Medium Risk Events: 12
Low Risk Events: 1
Normal Events: 17

Browser Risk: 38%
Camera Risk: 40%
Behaviour Risk: 38%

ML Prediction:
CHEATING / SUSPICIOUS

Final Risk: 40%
Final Risk Level: MEDIUM
```

### Result

The complete multimodal examination monitoring pipeline successfully worked from examination start through event detection, database storage, risk analysis, machine learning prediction, multimodal fusion, dashboard display, and examination completion.

---

## 14. Test Summary

| Module                 | Tested | Result |
| ---------------------- | ------ | ------ |
| Exam Interface         | Yes    | PASS   |
| Session Management     | Yes    | PASS   |
| Browser Monitoring     | Yes    | PASS   |
| Camera Monitoring      | Yes    | PASS   |
| Microphone Monitoring  | Yes    | PASS   |
| Risk Analysis          | Yes    | PASS   |
| Machine Learning       | Yes    | PASS   |
| Multimodal Fusion      | Yes    | PASS   |
| Backend APIs           | Yes    | PASS   |
| SQLite Database        | Yes    | PASS   |
| Dashboard              | Yes    | PASS   |
| Warning System         | Yes    | PASS   |
| End-to-End Integration | Yes    | PASS   |

---

## 15. Testing Conclusion

Testing confirms that the major components of the Multimodal AI-Based Exam Cheating Behaviour Analysis System work together successfully.

The system was tested at module level, API level, database level, and complete end-to-end level. The final integration test confirmed that browser, camera, microphone, machine learning, risk analysis, database, and dashboard components can operate together as a unified examination monitoring system.
