import requests
import config  # Store API key in config.py


def fetch_jobs(skills,location,remote_only,employment_type,experience):
    """
    Fetches jobs based on extracted skills and user-specified location.
    """
    if not skills:
        return ["NO SKILLS FOUND!!"]

    query = skills  # Ensure the query format is correct
    location = location # Format location

    url = "https://jobs-api14.p.rapidapi.com/v2/list"  # Correct API endpoint
    headers = {
        "X-RapidAPI-Key": config.RAPIDAPI_KEY,  # Ensure correct capitalization
        "X-RapidAPI-Host": "jobs-api14.p.rapidapi.com"
    }
    params = {
        "query": f"{query} with {experience} experience",
        "location": location,
        "autoTranslateLocation": "true",
        "remoteOnly": remote_only,
        "employmentTypes": employment_type
    }

    response = requests.get(url, headers=headers, params=params)

    # Debugging: Print details for troubleshooting
    print(f"Status Code: {response.status_code}")
    print(f"Params: {params}")

    if response.status_code == 200:
        jobs = response.json().get("jobs", [])  # Adjust based on API response structure
        return [
            {
                "title": job.get("title", "N/A"),
                "company": job.get("company", "N/A"),
                "location": job.get("location", "N/A"),
                "url": job["jobProviders"][0]["url"] if job.get("jobProviders") else "#",
                "description": job.get("description", "N/A"),
                "logo": job.get("image", "https://via.placeholder.com/150")
            }
            for job in jobs
        ]

    return []
