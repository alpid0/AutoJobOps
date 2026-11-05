import requests


API_URL = "https://himalayas.app/jobs/api/search"

SEARCH_TERMS = [
    "DevOps",
    "AWS",
    "Cloud Engineer",
    "Site Reliability",
    "Linux",
    "Platform Engineer",
    "SysOps"
]


def fetch_himalayas_jobs():
    all_jobs = []
    seen_urls = set()

    for term in SEARCH_TERMS:
        try:
            response = requests.get(
                API_URL,
                params={
                    "q": term,
                    "country": "IN",
                    "worldwide": "true",
                    "sort": "recent",
                    "page": 1
                },
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            jobs = data.get("jobs", [])

            for job in jobs:
                url = (
                    job.get("applicationLink")
                    or job.get("guid")
                )

                if not url or url in seen_urls:
                    continue

                seen_urls.add(url)

                restrictions = job.get(
                    "locationRestrictions", []
                )

                location = (
                    "Remote India"
                    if restrictions
                    else "Remote Worldwide"
                )

                all_jobs.append({
                    "title": job.get("title", ""),
                    "company": job.get("companyName", ""),
                    "location": location,
                    "description": job.get("description", ""),
                    "url": url,
                    "source": "Himalayas",
                    "salary_min": job.get("minSalary"),
                    "salary_max": job.get("maxSalary")
                })

        except requests.RequestException as error:
            print(f"Himalayas error for {term}: {error}")

    print(f"Himalayas jobs fetched: {len(all_jobs)}")

    return all_jobs
