import json
import re
from pathlib import Path
from html import unescape


CONFIG_PATH = Path("config/job_preferences.json")


# Technical skill groups. Each group represents a useful skill area.
SKILL_GROUPS = {
    "cloud": [
        "aws", "amazon web services", "ec2", "s3",
        "rds", "iam", "vpc", "gcp"
    ],
    "linux": [
        "linux", "rhel", "red hat", "ubuntu"
    ],
    "containers": [
        "docker", "kubernetes", "k8s", "helm"
    ],
    "infrastructure": [
        "terraform", "ansible", "infrastructure as code"
    ],
    "cicd": [
        "ci/cd", "github actions", "jenkins",
        "gitlab ci", "continuous integration"
    ],
    "scripting": [
        "python", "bash", "shell scripting", "powershell"
    ],
    "monitoring": [
        "cloudwatch", "prometheus", "grafana",
        "elk", "splunk", "monitoring"
    ]
}

TARGET_ROLE_KEYWORDS = [
    "devops engineer",
    "devops",
    "site reliability engineer",
    "sre",
    "cloud engineer",
    "cloud operations",
    "cloud ops",
    "aws sysops",
    "sysops engineer",
    "linux engineer",
    "linux administrator",
    "platform engineer"
]

SENIORITY_EXCLUSIONS = [
    "engineering manager",
    "cloud engineering manager",
    "devops manager",
    "director",
    "vice president",
    "vp of",
    "head of engineering"
]


def load_preferences():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def clean_text(value):
    """Remove HTML and normalize text."""
    value = str(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = unescape(value)
    value = re.sub(r"\s+", " ", value)
    return value.lower().strip()


def get_job_title(job):
    return clean_text(
        job.get("title") or job.get("jobTitle")
    )


def get_job_description(job):
    return clean_text(
        job.get("description")
        or job.get("jobDescription")
        or job.get("jobExcerpt")
    )


def check_role(title):
    return any(
        keyword in title
        for keyword in TARGET_ROLE_KEYWORDS
    )


def check_experience(text):
    """
    Find experience requirements when explicitly mentioned.
    Unknown experience is not automatically rejected.
    """

    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+(?:of\s+)?experience",
        r"minimum\s+of\s+(\d+(?:\.\d+)?)\s+years?",
        r"at\s+least\s+(\d+(?:\.\d+)?)\s+years?"
    ]

    values = []

    for pattern in patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            try:
                values.append(float(match))
            except ValueError:
                continue

    if not values:
        return None

    return max(values)


def calculate_skill_score(text):
    matched_groups = []

    for group, keywords in SKILL_GROUPS.items():

        if any(keyword in text for keyword in keywords):
            matched_groups.append(group)

    return matched_groups


def match_job(job):

    preferences = load_preferences()

    title = get_job_title(job)
    description = get_job_description(job)

    combined_text = f"{title} {description}"

    # 1. Check job title
    role_match = check_role(title)

    # 2. Exclude management-level positions
    seniority_excluded = any(
        keyword in title
        for keyword in SENIORITY_EXCLUSIONS
    )

    # 3. Check technical skill categories
    matched_groups = calculate_skill_score(combined_text)

    # 4. Check experience requirements
    experience_required = check_experience(combined_text)

    target_experience = preferences.get(
        "target_experience_years", 4.5
    )

    minimum_experience = preferences.get(
        "minimum_experience_years", 3
    )

    experience_match = True

    if experience_required is not None:
        experience_match = (
            experience_required <= target_experience + 1
        )

    # 5. Calculate score
    score = 0

    if role_match:
        score += 3

    score += len(matched_groups)

    if experience_match:
        score += 1

    if seniority_excluded:
        score = 0

    # 6. Final decision
    minimum_score = preferences.get(
        "minimum_match_score", 3
    )

    is_relevant = (
        role_match
        and not seniority_excluded
        and experience_match
        and len(matched_groups) >= 2
        and score >= minimum_score
    )

    # Save matching information
    job["match_score"] = score
    job["matched_skill_groups"] = matched_groups
    job["experience_required"] = experience_required
    job["is_relevant"] = is_relevant

    return job


def match_jobs(jobs):

    matched = []

    for job in jobs:

        result = match_job(job)

        if result["is_relevant"]:
            matched.append(result)

    return matched


def filter_jobs(jobs):

    return [
        match_job(job)
        for job in jobs
    ]
