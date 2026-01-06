import re
import pandas as pd
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# -------------------------------
# Feature Extraction Function
# -------------------------------
def extract_features(url):
    features = []

    features.append(len(url))                  # URL length
    features.append(url.count('.'))             # Number of dots
    features.append(1 if 'https' in url else 0) # HTTPS present
    features.append(1 if re.search(r'\d', url) else 0)  # Digits
    features.append(1 if '@' in url else 0)     # @ symbol

    return features


# -------------------------------
# ML Training Logic
# -------------------------------
# Load dataset
data = pd.read_csv("dataset/phishing.csv")

X = data["url"].apply(extract_features).tolist()
y = data["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save trained model
pickle.dump(model, open("model.pkl", "wb"))
