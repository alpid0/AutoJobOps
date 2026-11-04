import requests
from job_matcher import match_jobs
from job_store import save_new_jobs

API_URL = "https://jobicy.com/api/jobs"


def fetch_jobs():

    print("Connecting to Jobicy API...")

    params = {
        "count": 50,
        "geo": "anywhere",
        "industry": "engineering"
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        jobs = data.get("jobs", [])

        print(f"\nTotal jobs fetched: {len(jobs)}\n")

        if not jobs:
            print("No jobs found.")
            return []

        for job in jobs:

            print("--------------------------------")
            print("Company:", job.get("companyName"))
            print("Position:", job.get("jobTitle"))
            print("Location:", job.get("jobGeo"))
            print("Salary:", job.get("annualSalaryMin"))
            print("Job URL:", job.get("url"))

        # Match relevant jobs
        matched_jobs = match_jobs(jobs)

        # Remove duplicate jobs and save new jobs
        new_jobs = save_new_jobs(matched_jobs)

        print("\n========== FINAL RESULTS ==========")
        print("Total jobs fetched:", len(jobs))
        print("Relevant jobs:", len(matched_jobs))
        print("New unique jobs:", len(new_jobs))

        return new_jobs

    except requests.exceptions.RequestException as error:

        print("API request failed:", error)
        raise

    except (ValueError, AttributeError) as error:

        print("Invalid API response:", error)
        raise


if __name__ == "__main__":
    fetch_jobs()
