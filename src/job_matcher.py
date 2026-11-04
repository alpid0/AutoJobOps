# AutoJobOps - Job Matching Engine

import json

# Your job preferences
preferences = {
    "skills": [
        "linux",
        "aws",
        "docker",
        "kubernetes",
        "terraform",
        "python",
        "jenkins",
        "github actions"
    ],
    "minimum_experience": 2,
    "target_role": "DevOps Engineer"
}

# Sample job listings
jobs = [
    {
        "company": "ABC Technologies",
        "role": "DevOps Engineer",
        "experience": 3,
        "skills": ["Linux", "AWS", "Docker", "Jenkins"]
    },
    {
        "company": "XYZ Solutions",
        "role": "Java Developer",
        "experience": 4,
        "skills": ["Java", "Spring Boot"]
    },
    {
        "company": "Cloud Systems",
        "role": "Cloud Engineer",
        "experience": 3,
        "skills": ["AWS", "Linux", "Terraform", "Python"]
    }
]

def match_jobs():

    print("\nStarting AutoJobOps Job Matcher\n")

    for job in jobs:

        matching_skills = set(
            skill.lower() for skill in job["skills"]
        ) & set(preferences["skills"])

        match_percentage = (
            len(matching_skills) /
            len(preferences["skills"])
        ) * 100

        if job["experience"] >= preferences["minimum_experience"]:

            print("--------------------------------")
            print("Company:", job["company"])
            print("Role:", job["role"])
            print("Experience:", job["experience"])
            print("Matching Skills:", matching_skills)
            print("Match Score:", round(match_percentage, 2), "%")

    print("\nJob matching completed!")

if __name__ == "__main__":
    match_jobs()
