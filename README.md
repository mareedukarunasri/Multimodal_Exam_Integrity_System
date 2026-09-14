# Multimodal AI-Based Exam Cheating Behaviour Analysis System

## 📌 Project Overview

The **Multimodal AI-Based Exam Cheating Behaviour Analysis System** is an AI-assisted online examination monitoring system designed to identify and analyze potentially suspicious examination behaviour using multiple monitoring signals.

The system combines **browser activity, camera-based behaviour, microphone activity, risk scoring, and machine learning prediction** to provide an overall assessment of a student's examination behaviour.

---

## 🎯 Objectives

* Monitor suspicious browser activities during an online examination.
* Detect face-related and behavioural changes using the camera.
* Detect possible mobile phone usage.
* Detect possible talking or voice activity.
* Store examination events in a database.
* Calculate browser, camera, behaviour, and overall risk scores.
* Use machine learning to provide an additional risk prediction.
* Display examination events and risk information through a dashboard.
* Combine multiple monitoring signals using a multimodal approach.

---

## 🚀 Main Features

### 1. Browser Monitoring

The system monitors browser-related activities such as:

* Tab switching / tab hiding
* Window blur and focus
* Copy
* Paste
* Cut
* Right-click
* Fullscreen exit

Each detected event is sent to the backend and stored for analysis.

### 2. Camera Monitoring

The camera module monitors examination behaviour such as:

* Face presence
* No-face detection
* Looking left
* Looking right
* Head movement
* Mobile phone detection

### 3. Microphone Monitoring

The system uses microphone activity to identify possible talking or voice activity during the examination.

### 4. Risk Analysis

Different monitoring signals are converted into risk scores, including:

* Browser Risk
* Camera Risk
* Behaviour Risk
* Machine Learning Risk
* Final Risk

### 5. Machine Learning Prediction

A machine learning model provides an additional prediction based on examination event patterns.

The current implementation uses a **Random Forest Classifier** for prediction.

### 6. Dashboard

The dashboard provides information about:

* Total events
* Risk levels
* Browser events
* Camera events
* Behaviour events
* ML prediction
* Overall student risk

---

## 🧩 System Modules

1. **Exam Interface**
2. **Browser Monitoring**
3. **Camera Monitoring**
4. **Behaviour Analysis**
5. **Microphone Monitoring**
6. **Risk Scoring**
7. **Multimodal Risk Fusion**
8. **Backend API**
9. **Database Management**
10. **Machine Learning Prediction**
11. **Risk Analysis Dashboard**

---

## 🛠️ Technologies Used

* **Python**
* **FastAPI**
* **SQLite**
* **JavaScript**
* **HTML**
* **CSS**
* **scikit-learn**
* **Random Forest**
* **Computer Vision**
* **COCO-SSD / TensorFlow.js**
* **Git**
* **GitHub**

---

## 📁 Project Structure

```text
Multimodal_Exam_Integrity_System/
│
├── backend/
│   └── app/
│       ├── database.py
│       ├── main.py
│       │
│       ├── ml/
│       │   ├── dataset.csv
│       │   ├── predict.py
│       │   └── train_model.py
│       │
│       ├── routes/
│       │   └── dashboard.py
│       │
│       └── services/
│           └── browser_monitor.py
│
├── datasets/
│   └── raw/
│       └── browser/
│           └── sample_browser_events.csv
│
├── frontend/
│   ├── src/
│   │   └── monitoring/
│   │       ├── browserMonitor.js
│   │       └── camera_monitor.js
│   │
│   └── test/
│       ├── browser_monitor_test.html
│       ├── camera_test.html
│       ├── dashboard.html
│       ├── exam.html
│       └── .gitignore
│
├── .gitignore
└── README.md
```

> The local SQLite database `backend/exam_events.db` is generated during runtime and is intentionally excluded from Git using `.gitignore`.

---

## ▶️ How to Run the Project

### Step 1 — Start the Backend

Open PowerShell or the VS Code terminal:

```powershell
cd C:\Users\maree\OneDrive\Desktop\Multimodal_Exam_Integrity_System\backend
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

### Step 2 — Check Backend Health

Open:

```text
http://127.0.0.1:8000/health
```

### Step 3 — Start the Frontend

Open the project using **VS Code Live Server**.

### Exam

```text
http://127.0.0.1:5500/frontend/test/exam.html
```

### Dashboard

```text
http://127.0.0.1:5500/frontend/test/dashboard.html
```

The browser may ask for permission to access the **camera and microphone**. Allow these permissions for monitoring features to work.

---

## 📊 Risk Analysis

The system analyzes multiple sources of examination behaviour.

### Browser Risk

Calculated from suspicious browser events such as:

* Tab hidden
* Window blur
* Copy
* Paste
* Cut
* Fullscreen exit

### Camera Risk

Calculated from camera-related observations such as:

* No face
* Looking away
* Mobile phone detection
* Other detected camera behaviours

### Behaviour Risk

Represents suspicious behavioural activity detected from available monitoring signals.

### Machine Learning Risk

The machine learning module provides an additional prediction based on examination event patterns.

### Final Risk

The system combines multiple risk signals to produce an overall examination risk assessment.

---

## 🤖 Machine Learning

The current machine learning implementation uses:

**Algorithm:** Random Forest Classifier

The model uses examination event information such as:

```text
tab_hidden
window_blur
copy
paste
cut
fullscreen_exit
total_events
```

The model predicts whether the observed event pattern is:

```text
NORMAL
```

or

```text
CHEATING / SUSPICIOUS
```

The ML prediction is used as an additional signal along with browser, camera, and behaviour analysis.

---

## 💾 Database

The project uses **SQLite** for storing examination data.

The database stores information related to:

* Browser events
* Camera events
* Examination sessions
* Student IDs
* Event timestamps
* Risk scores
* Risk levels
* Session information

The runtime database file is not committed to GitHub because it contains locally generated examination data.

---

## 🔄 Multimodal Analysis

The main concept of this project is to combine multiple monitoring sources instead of depending on a single signal.

```text
                 Online Examination
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
      Browser         Camera       Microphone
     Monitoring      Monitoring     Monitoring
          │             │             │
          └─────────────┼─────────────┘
                        │
                        ▼
                 Behaviour Analysis
                        │
                        ▼
                  Risk Calculation
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        ML Prediction       Risk Fusion
              │                   │
              └─────────┬─────────┘
                        ▼
                  Final Risk
                        │
                        ▼
                    Dashboard
```

---

## 📈 Example Output

A completed examination session can provide information such as:

```text
Total Events
High Risk Events
Medium Risk Events
Low Risk Events
Normal Events

Browser Risk
Camera Risk
Behaviour Risk
ML Risk
Final Risk

ML Prediction
Risk Level
```

---

## 👥 Team Members

| Name                    | Role        |
| ----------------------- | ----------- |
| **Mareedu Karuna Sri**  | Team Lead   |
| **Akshitha Devarajula** | Team Member |
| **Neelima Cheemala**    | Team Member |
| **Harshini Mogunuri**   | Team Member |

---

## 🎓 Academic Details

**College:**
Swarna Bharathi Institute Of Science And Technology

**Project Guide:**
Dr. Rahul N. Nawkhare

**Project:**
Multimodal AI-Based Exam Cheating Behaviour Analysis System

---

## 🔐 Privacy and Ethical Considerations

This project is developed as an **academic prototype** for examination behaviour analysis.

Camera, microphone, and browser monitoring should be used only with appropriate authorization and user awareness.

The system's risk score and ML prediction should be treated as **supporting evidence**, not as the sole basis for disciplinary decisions. Suspicious results should be reviewed by authorized examination staff.

---

## 📌 Project Status

The current prototype includes:

* Browser monitoring
* Camera monitoring
* Face detection
* Looking-away detection
* Mobile phone detection
* Microphone/talking detection
* Risk scoring
* Multimodal risk analysis
* Machine learning prediction
* SQLite database
* Exam sessions
* Dashboard
* Git/GitHub project management

---

## 📜 License

This project is developed for **academic and educational purposes**.
