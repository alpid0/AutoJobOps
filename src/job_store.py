import json
import os

DATA_FILE = "data/jobs.json"


def load_existing_jobs():

    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_new_jobs(matched_jobs):

    os.makedirs("data", exist_ok=True)

    existing_jobs = load_existing_jobs()

    existing_urls = {
        job.get("url")
        for job in existing_jobs
    }

    new_jobs = []

    for job in matched_jobs:

        job_url = job.get("url")

        if job_url and job_url not in existing_urls:

            new_jobs.append(job)
            existing_urls.add(job_url)

    all_jobs = existing_jobs + new_jobs

    with open(DATA_FILE, "w") as file:

        json.dump(
            all_jobs,
            file,
            indent=4
        )

    print("\n========== JOB STORAGE ==========")

    print("Previously stored jobs:", len(existing_jobs))
    print("New jobs discovered:", len(new_jobs))
    print("Total stored jobs:", len(all_jobs))

    return new_jobs
