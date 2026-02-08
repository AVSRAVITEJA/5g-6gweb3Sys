import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

df = pd.read_csv("ml/network_dataset.csv")

X = df.drop("decision", axis=1)
y = df["decision"]

traffic_encoder = LabelEncoder()
decision_encoder = LabelEncoder()

X["traffic_type"] = traffic_encoder.fit_transform(X["traffic_type"])
y = decision_encoder.fit_transform(y)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "ml/slice_model.pkl")
joblib.dump(traffic_encoder, "ml/label_encoder.pkl")

print("ML model trained and saved")
