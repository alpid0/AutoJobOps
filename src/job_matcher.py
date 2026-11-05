import json
from pathlib import Path


CONFIG_PATH = Path("config/job_preferences.json")


def load_preferences():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize(text):
    return str(text or "").lower().strip()


def match_job(job):
    preferences = load_preferences()

    title = normalize(job.get("title") or job.get("jobTitle"))
    location = normalize(job.get("location") or job.get("jobGeo"))
    description = normalize(
        job.get("description") or job.get("jobDescription")
    )

    target_roles = [
        normalize(role)
        for role in preferences["target_roles"]
    ]

    preferred_skills = [
        normalize(skill)
        for skill in preferences["preferred_skills"]
    ]

    preferred_locations = [
        normalize(loc)
        for loc in preferences["preferred_locations"]
    ]

    role_match = any(role in title for role in target_roles)

    location_match = any(
        loc in location for loc in preferred_locations
    )

    combined_text = f"{title} {description}"

    matched_skills = [
        skill for skill in preferred_skills
        if skill in combined_text
    ]

    score = len(matched_skills)

    minimum_score = preferences.get("minimum_match_score", 3)

    is_relevant = (
        role_match
        and location_match
        and score >= minimum_score
    )

    job["match_score"] = score
    job["matched_skills"] = matched_skills
    job["is_relevant"] = is_relevant

    return job


def filter_jobs(jobs):
    return [match_job(job) for job in jobs]
