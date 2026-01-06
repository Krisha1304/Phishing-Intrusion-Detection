from flask import Flask, request, render_template_string
import pickle
import re

app = Flask(__name__)

# Load trained model
model = pickle.load(open("model/model.pkl", "rb"))

def extract_features(url):
    features = []
    features.append(len(url))
    features.append(url.count('.'))
    features.append(1 if 'https' in url else 0)
    features.append(1 if re.search(r'\d', url) else 0)
    features.append(1 if '@' in url else 0)
    return [features]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Phishing Detection</title>
</head>
<body>
    <h2>Phishing Intrusion Detection System</h2>
    <form method="post">
        <input type="text" name="url" placeholder="Enter URL" size="50" required>
        <button type="submit">Check</button>
    </form>
    {% if result %}
        <h3>Result: {{ result }}</h3>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form["url"]
        prediction = model.predict(extract_features(url))[0]
        result = "Phishing URL 🚨" if prediction == 1 else "Legitimate URL ✅"
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(debug=True)
