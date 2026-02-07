import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load dataset
df = pd.read_csv("../data/raw/power_data.csv")

# Features (X)
X = df[
    [
        "hour",
        "is_peak_hour",
        "house1_current",
        "house2_current",
        "house3_current",
        "house4_current",
        "house5_current",
        "total_current",
        "current_change_rate",
    ]
]

# Target (y) — overload prediction
y = df["overload_flag"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(n_estimators=120)

# Train
model.fit(X_train, y_train)

# Evaluate
pred = model.predict(X_test)
print(classification_report(y_test, pred))

# Save model
joblib.dump(model, "../models/overload_model.pkl")

print("✅ Model trained and saved as overload_model.pkl")
