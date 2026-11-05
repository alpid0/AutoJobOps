import requests

from job_matcher import match_jobs
from job_store import save_new_jobs
from himalayas_fetcher import fetch_himalayas_jobs


JOBICY_API_URL = "https://jobicy.com/api/jobs"


def fetch_jobicy_jobs():
    print("\nConnecting to Jobicy API...")

    params = {
        "count": 100,
        "geo": "anywhere",
        "industry": "engineering"
    }

    response = requests.get(
        JOBICY_API_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()
    jobs = data.get("jobs", [])

    print("Jobicy jobs fetched:", len(jobs))

    return jobs


def fetch_all_jobs():
    all_jobs = []

    # Source 1: Jobicy
    try:
        jobicy_jobs = fetch_jobicy_jobs()
        all_jobs.extend(jobicy_jobs)

    except Exception as error:
        print("Jobicy fetch failed:", error)

    # Source 2: Himalayas
    try:
        himalayas_jobs = fetch_himalayas_jobs()
        all_jobs.extend(himalayas_jobs)

    except Exception as error:
        print("Himalayas fetch failed:", error)

    print("\n========== FETCH SUMMARY ==========")
    print("Total jobs from all sources:", len(all_jobs))

    return all_jobs


def main():

    print("Starting AutoJobOps...")
    
    # Fetch jobs from all sources
    jobs = fetch_all_jobs()

    if not jobs:
        print("No jobs fetched from any source.")
        return

    # Match relevant jobs
    matched_jobs = match_jobs(jobs)

    print("\n========== MATCHING RESULTS ==========")
    print("Total fetched:", len(jobs))
    print("Relevant jobs:", len(matched_jobs))

    # Store unique jobs
    new_jobs = save_new_jobs(matched_jobs)

    print("\n========== FINAL RESULTS ==========")
    print("Total fetched:", len(jobs))
    print("Relevant jobs:", len(matched_jobs))
    print("New unique jobs:", len(new_jobs))

    print("\nAutoJobOps completed successfully!")


if __name__ == "__main__":
    main()
