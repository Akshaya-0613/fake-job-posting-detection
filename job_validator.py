job_keywords = [
    "job",
    "position",
    "company",
    "experience",
    "salary",
    "location",
    "skills",
    "qualification",
    "responsibilities",
    "requirements",
    "apply",
    "candidate",
    "employment",
    "vacancy",
    "role",
    "designation",
    "hiring",
    "recruitment",
    "interview",
    "joining",
    "benefits"
]


def is_valid_job_post(text):

    text = text.lower()

    score = 0

    for keyword in job_keywords:
        if keyword in text:
            score += 1

    # Must have at least 15 words
    if len(text.split()) < 15:
        return False

    # Must contain at least 3 job-related keywords
    if score >= 3:
        return True

    return False