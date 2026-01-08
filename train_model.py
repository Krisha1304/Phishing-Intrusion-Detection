import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
import os
import re

def extract_features(url):
    features = []
    features.append(len(url))
    features.append(url.count('.'))
    features.append(1 if 'https' in url else 0)
    features.append(1 if re.search(r'\d', url) else 0)
    features.append(1 if '@' in url else 0)
    return features

# Load dataset
data = pd.read_csv("dataset/phishing.csv")

X = data["url"].apply(extract_features).tolist()
y = data["label"]

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Create model directory
os.makedirs("model", exist_ok=True)

# Save trained model
with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved successfully!")
