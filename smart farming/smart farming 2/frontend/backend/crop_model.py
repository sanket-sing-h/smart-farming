import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# load dataset
data = pd.read_csv("Crop_recommendation.csv")

# remove spaces in column names
data.columns = data.columns.str.strip()

print(data.columns)

# features
X = data[['N','P','K','temperature','humidity','ph','rainfall']]

# target
y = data['label']

# train model
model = RandomForestClassifier()
model.fit(X,y)

# save model
pickle.dump(model, open("crop_model.pkl","wb"))

print("Model trained successfully")