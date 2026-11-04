```python
# AutoJobOps - Intelligent Job Matcher

KEYWORDS = [
    "devops",
    "cloud engineer",
    "linux",
    "aws",
    "docker",
    "kubernetes",
    "terraform",
    "jenkins",
    "github actions",
    "ci/cd",
    "sre",
    "cloud operations"
]

def match_jobs(jobs):

    matched_jobs = []

    print("\nStarting Intelligent Job Matching...\n")

    for job in jobs:

        title = job.get("jobTitle", "")
        description = job.get("jobDescription", "")

        searchable_text = (
            title + " " + description
        ).lower()

        matching_keywords = [
            keyword for keyword in KEYWORDS
            if keyword in searchable_text
        ]

        score = len(matching_keywords)

        if score >= 2:

            matched_jobs.append(job)

            print("--------------------------------")
            print("Company:", job.get("companyName"))
            print("Role:", title)
            print("Location:", job.get("jobGeo"))
            print("Matching Skills:", matching_keywords)
            print("Match Score:", score, "/", len(KEYWORDS))
            print("Job URL:", job.get("url"))

    print("\nTotal jobs received:", len(jobs))
    print("Relevant jobs found:", len(matched_jobs))

    return matched_jobs
```
