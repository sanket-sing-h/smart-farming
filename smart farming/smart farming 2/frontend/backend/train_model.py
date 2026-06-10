import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
import pickle

# Get current folder path
base_path = os.path.dirname(__file__)

# Correct dataset name (YOUR FILE)
file_path = os.path.join(base_path, "Crop_recommendation.csv")

# Load dataset
df = pd.read_csv(file_path)

# Split data
X = df.drop("label", axis=1)
y = df["label"]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model with YOUR filename
model_path = os.path.join(base_path, "crop_model.pkl")
pickle.dump(model, open(model_path, "wb"))

print("Model Trained ✅")