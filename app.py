from flask import Flask, request, render_template_string
import pickle
import re
import os

app = Flask(__name__)

# Load trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "model.pkl")
model = pickle.load(open(MODEL_PATH, "rb"))

def extract_features(url):
    features = []
    features.append(len(url))
    features.append(url.count('.'))
    features.append(1 if 'https' in url else 0)
    features.append(1 if re.search(r'\d', url) else 0)
    features.append(1 if '@' in url else 0)
    return [features]

# Paragraph points for phishing detection
PHISHING_POINTS = [
    "Misspelled or fake domains: e.g., paypa1.com, login-paypal.com",
    "HTTPS missing or unusual: secure sites usually have https://",
    "Suspicious characters: @, -, _, or random numbers",
    "Long URLs or extra subdomains: often used to trick users",
    "IP address instead of domain: e.g., http://192.168.0.1"
]

# HTML template with colorful CSS
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Phishing Detection</title>
    <style>
        /* Body and background */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to right,  #6d7da0, #c0829d);
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 50px;
            color: #2c3e50;
        }
        h2 {
            color: #fff;
            text-shadow: 1px 1px 3px #000;
        }
        p.info {
            max-width: 700px;
            text-align: center;
            background: #ffffffcc;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
            margin-bottom: 20px;
            font-size: 1.1em;
        }
        /* Form */
        form {
            margin-bottom: 20px;
            display: flex;
            justify-content: center;
        }
        form input[type="text"] {
            width: 400px;
            padding: 12px;
            border: 2px solid #2980b9;
            border-radius: 8px;
            margin-right: 10px;
            font-size: 1em;
        }
        form button {
            padding: 12px 25px;
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }
        form button:hover {
            background: linear-gradient(to right, #feb47b, #ff7e5f);
        }
        /* Phishing points list */
        ul.phishing-points {
            max-width: 700px;
            background: #fff3e0;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 2px 2px 15px rgba(0,0,0,0.2);
            list-style-type: square;
            color: #34495e;
            font-weight: 500;
            margin-bottom: 30px;
        }
        ul.phishing-points li {
            margin: 10px 0;
        }
        /* Result text */
        h3.result {
            margin-top: 20px;
            font-size: 1.3em;
            padding: 10px 20px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
        }
        h3.result.phishing {
            background: #e74c3c; /* red */
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        }
        h3.result.legit {
            background: #27ae60; /* green */
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>
    <h2>Phishing Intrusion Detection System</h2>
    <p class="info">Enter a URL below to check whether it is legitimate or phishing. Follow the points below to identify phishing URLs manually as well.</p>
    
    <form method="post">
        <input type="text" name="url" placeholder="Enter URL" size="50" required>
        <button type="submit">Check</button>
    </form>

    <!-- Points below the input box -->
    <ul class="phishing-points">
        {% for point in phishing_points %}
            <li>{{ point }}</li>
        {% endfor %}
    </ul>

    {% if result %}
        <h3 class="result {{ 'phishing' if result.startswith('Phishing') else 'legit' }}">
            Result: {{ result }}
        </h3>
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
    return render_template_string(HTML, result=result, phishing_points=PHISHING_POINTS)

if __name__ == "__main__":
    app.run(debug=True)
