import json
from pathlib import Path


# Load job preferences
CONFIG_FILE = Path("config/job_preferences.json")


def load_preferences():

    with open(CONFIG_FILE, "r") as file:
        return json.load(file)


def match_jobs(jobs):

    preferences = load_preferences()

    target_roles = [
        role.lower()
        for role in preferences["target_roles"]
    ]

    preferred_skills = [
        skill.lower()
        for skill in preferences["preferred_skills"]
    ]

    preferred_locations = [
        location.lower()
        for location in preferences["preferred_locations"]
    ]

    minimum_score = preferences["minimum_match_score"]

    matched_jobs = []

    print("\n========== INTELLIGENT JOB MATCHING ==========\n")

    for job in jobs:

        title = job.get("jobTitle", "")
        description = job.get("jobDescription", "")
        location = job.get("jobGeo", "")

        searchable_text = (
            title + " " + description
        ).lower()

        # Check whether job title matches target roles
        role_match = any(
            role in title.lower()
            for role in target_roles
        )

        # Check matching technical skills
        matching_skills = [
            skill
            for skill in preferred_skills
            if skill in searchable_text
        ]

        score = len(matching_skills)

        # Check preferred location
        location_match = any(
            preferred_location in location.lower()
            for preferred_location in preferred_locations
        )

        # Accept only relevant roles with enough matching skills
        if role_match and location_match and score >= minimum_score:

            matched_jobs.append(job)

            print("--------------------------------")
            print("Company:", job.get("companyName"))
            print("Role:", title)
            print("Location:", location)
            print("Matching Skills:", matching_skills)
            print("Match Score:", score)
            print("Job URL:", job.get("url"))

    print("\n========== MATCHING SUMMARY ==========")
    print("Total jobs received:", len(jobs))
    print("Relevant jobs found:", len(matched_jobs))

    return matched_jobs
