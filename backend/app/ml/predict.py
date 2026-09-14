import pandas as pd

from sklearn.ensemble import RandomForestClassifier

from app.database import (
    get_all_browser_events,
    get_active_exam_session
)


def get_ml_prediction(session_id=None):

    # -----------------------------------------
    # 1. Load ML training dataset
    # -----------------------------------------

    data = pd.read_csv("app/ml/dataset.csv")

    X = data[
        [
            "tab_hidden",
            "window_blur",
            "copy",
            "paste",
            "cut",
            "fullscreen_exit",
            "total_events"
        ]
    ]

    y = data["cheating"]

    # -----------------------------------------
    # 2. Train Random Forest model
    # -----------------------------------------

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    # -----------------------------------------
    # 3. Determine session
    # -----------------------------------------

    if session_id:

        print("ML using selected session:", session_id)

    else:

        active_session = get_active_exam_session("S001")

        if active_session:

            session_id = active_session["session_id"]

            print(
                "ML using active session:",
                session_id
            )

        else:

            print("No exam session selected or active.")

    # -----------------------------------------
    # 4. Get browser events
    # -----------------------------------------

    if session_id:

        events = get_all_browser_events(
            session_id=session_id
        )

    else:

        events = []

    # -----------------------------------------
    # 5. Count event types
    # -----------------------------------------

    tab_hidden = 0
    window_blur = 0
    copy = 0
    paste = 0
    cut = 0
    fullscreen_exit = 0

    for event in events:

        event_type = event["event_type"]

        if event_type == "tab_hidden":

            tab_hidden += 1

        elif event_type == "window_blur":

            window_blur += 1

        elif event_type == "copy":

            copy += 1

        elif event_type == "paste":

            paste += 1

        elif event_type == "cut":

            cut += 1

        elif event_type == "fullscreen_exit":

            fullscreen_exit += 1

    total_events = len(events)

    # -----------------------------------------
    # 6. Prepare student data
    # -----------------------------------------

    student_data = [[
        tab_hidden,
        window_blur,
        copy,
        paste,
        cut,
        fullscreen_exit,
        total_events
    ]]

    # -----------------------------------------
    # 7. Predict
    # -----------------------------------------

    prediction = model.predict(student_data)

    if prediction[0] == 1:

        result = "CHEATING / SUSPICIOUS"

    else:

        result = "NORMAL"

    # -----------------------------------------
    # 8. Return result
    # -----------------------------------------

    return {
        "prediction": result,
        "session_id": session_id,
        "total_events": total_events,
        "tab_hidden": tab_hidden,
        "window_blur": window_blur,
        "copy": copy,
        "paste": paste,
        "cut": cut,
        "fullscreen_exit": fullscreen_exit
    }


if __name__ == "__main__":

    result = get_ml_prediction()

    print(
        "ML Prediction for Current Exam Session"
    )

    print("----------------------------------------")

    for key, value in result.items():

        print(
            f"{key}: {value}"
        )