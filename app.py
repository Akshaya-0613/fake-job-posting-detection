from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# Load trained model and vectorizer
model = pickle.load(open("fake_job_model.pkl", "rb"))
vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    text = request.form["job_description"]

    # Convert text into numbers
    vector = vectorizer.transform([text])

    # Probability prediction
    probability = model.predict_proba(vector)

    fake_probability = probability[0][1]

    confidence = round(max(probability[0]) * 100, 2)

    # Standard threshold (50%)
    if fake_probability >= 0.50:
        result = "Fake Job Posting"
    else:
        result = "Real Job Posting"

    return render_template(
        "index.html",
        prediction=result,
        confidence=confidence
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)