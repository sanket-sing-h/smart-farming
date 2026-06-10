import joblib
import numpy as np

model = joblib.load("crop_model.pkl")

sample = np.array([[45,28,60]])

prediction = model.predict(sample)

print("Recommended Crop:", prediction[0])