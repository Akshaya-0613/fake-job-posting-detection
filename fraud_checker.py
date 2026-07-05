import re

# Suspicious keywords commonly found in fake job postings
fraud_keywords = [
    "registration fee",
    "security deposit",
    "document verification fee",
    "document verification charges",
    "processing fee",
    "pay",
    "payment",
    "advance payment",
    "refundable",
    "whatsapp",
    "telegram",
    "immediate joining",
    "limited seats",
    "100% selection",
    "guaranteed job"
]

# Free email domains
free_email_domains = [
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com"
]


def check_fraud(text):

    text = text.lower()

    fraud_score = 0
    reasons = []

    # Check suspicious keywords
    for keyword in fraud_keywords:
        if keyword in text:
            fraud_score += 1
            reasons.append(f"Detected '{keyword}'")

    # Check email domains
    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    emails = re.findall(email_pattern, text)

    for email in emails:
        domain = email.split("@")[1]

        if domain in free_email_domains:
            fraud_score += 2
            reasons.append(f"Unofficial email detected ({email})")

    return fraud_score, reasons