import requests
import streamlit as st

api_key = st.secrets["RAPIDAPI_KEY"]

def fetch_jobs(skills,location,remote_only,employment_type):
    """
    Fetches jobs based on extracted skills and user-specified location.
    """
    if not skills:
        return ["NO SKILLS FOUND!!"]
    


    query = skills  
    location = location 

    url = "https://jobs-search-api.p.rapidapi.com/getjobs"  # API endpoint
    headers = {
        "x-rapidapi-key": api_key,
	    "x-rapidapi-host": "jobs-search-api.p.rapidapi.com",
	    "Content-Type": "application/json"
    }
    params = {
        "search_term": query,
	    "location": location,
	    "results_wanted": 10,
	    "site_name": ["indeed", "linkedin", "zip_recruiter", "glassdoor"],
	    "job_type": employment_type,
	    "is_remote": remote_only,
	    "hours_old": 168
    }

    response = requests.post(url, json=params, headers=headers)

    # Debugging: Print details for troubleshooting
    print(f"Status Code: {response.status_code}")
    print(f"Params: {params}")

    if response.status_code == 200:
        jobs = response.json().get("jobs", []) 
        return [
            {
                "site": job.get("site", "N/A"),
                "title": job.get("title", "N/A"),
                "company": job.get("company", "N/A"),
                "location": job.get("location") or "Remote",
                "url": job.get("job_url", "#"),
                "date_posted": job.get("date_posted") or "N/A"
            }
            for job in jobs
        ]

    return []
