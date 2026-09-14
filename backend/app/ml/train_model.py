import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# Load dataset
data = pd.read_csv("app/ml/dataset.csv")


# Input features
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


# Target
y = data["cheating"]


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create ML model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Train model
model.fit(X_train, y_train)


# Test model
predictions = model.predict(X_test)


# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)


print("ML Model Training Completed")
print("----------------------------")
print("Accuracy:", round(accuracy * 100, 2), "%")


# Test one new student's behavior
new_student = [[
    12,   # tab_hidden
    12,   # window_blur
    2,    # copy
    3,    # paste
    1,    # cut
    2,    # fullscreen_exit
    60    # total_events
]]


prediction = model.predict(new_student)


if prediction[0] == 1:
    print("Prediction: CHEATING / SUSPICIOUS")
else:
    print("Prediction: NORMAL")