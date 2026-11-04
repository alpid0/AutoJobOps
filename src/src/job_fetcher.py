import requests

API_URL = "https://jobicy.com/api/jobs"

def fetch_jobs():

    print("Connecting to Jobicy API...")

    params = {
        "count": 50,
        "geo": "anywhere",
        "industry": "engineering"
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    jobs = data.get("jobs", [])

    print(f"\nTotal jobs fetched: {len(jobs)}\n")

    for job in jobs:

        print("--------------------------------")

        print("Company:", job.get("companyName"))
        print("Position:", job.get("jobTitle"))
        print("Location:", job.get("jobGeo"))
        print("Salary:", job.get("annualSalaryMin"))
        print("Job URL:", job.get("url"))

    return jobs


if __name__ == "__main__":
    fetch_jobs()
