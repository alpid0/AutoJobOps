
import requests
from job_matcher import match_jobs

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

        matched_jobs = match_jobs(jobs)

        print("\nJob fetching completed successfully.")

        return matched_jobs

    except requests.exceptions.RequestException as error:
        print("API request failed:", error)
        raise

    except (ValueError, AttributeError) as error:
        print("Invalid API response:", error)
        raise


if __name__ == "__main__":
    fetch_jobs()

