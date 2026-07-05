from flask import Flask, render_template, request
import pickle
import os

from job_validator import is_valid_job_post
from fraud_checker import check_fraud

app = Flask(__name__)

# Load trained model and vectorizer
model = pickle.load(open("fake_job_model.pkl", "rb"))
vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # Get user input
    text = request.form["job_description"]

    # -----------------------------
    # STEP 1 : Validate Job Posting
    # -----------------------------
    if not is_valid_job_post(text):
        return render_template(
            "index.html",
            prediction="Invalid Job Posting",
            confidence=0,
            reasons=["The provided text is not recognized as a valid job posting."],
            recommendation="Please provide a complete job posting that includes details such as the company name, job title, responsibilities, qualifications, and other relevant information."
        )

    # -----------------------------
    # STEP 2 : Fraud Detection Rules
    # -----------------------------
    fraud_score, reasons = check_fraud(text)

    # -----------------------------
    # STEP 3 : Machine Learning Prediction
    # -----------------------------
    vector = vectorizer.transform([text])

    probability = model.predict_proba(vector)

    fake_probability = probability[0][1]

    confidence = round(max(probability[0]) * 100, 2)

    # -----------------------------
    # STEP 4 : Final Decision
    # -----------------------------
    if fraud_score >= 3:

        result = "Fake Job Posting"

        confidence = min(95, confidence + 10)

    elif fake_probability >= 0.50:

        result = "Fake Job Posting"

    else:

        result = "Real Job Posting"

    # -----------------------------
    # STEP 5 : Recommendation
    # -----------------------------
    if result == "Fake Job Posting":
        recommendation = (
            "This job posting contains one or more suspicious indicators. "
            "Do not pay any registration, processing, or verification fees. "
            "Always verify the opportunity through the company's official careers website before sharing personal information."
        )

    elif result == "Real Job Posting":
        recommendation = (
            "This job posting appears legitimate based on the available information. "
            "However, always verify the job through the company's official careers website before applying."
        )

    else:
        recommendation = (
            "Please provide a valid and complete job posting for analysis."
        )

    # -----------------------------
    # STEP 6 : Return Result
    # -----------------------------
    return render_template(
        "index.html",
        prediction=result,
        confidence=confidence,
        reasons=reasons,
        recommendation=recommendation
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)