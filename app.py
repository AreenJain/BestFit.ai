import streamlit as st
from resume_parser import parse_resume
from job_fetcher import fetch_jobs
from ats_scoring import scoring, job_profiles, experience
import os
# Path to the locally extracted wkhtmltopdf binary
WKHTMLTOPDF_PATH = os.path.join(os.getcwd(), "bin", "wkhtmltopdf")
# Configure pdfkit to use the local binary
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"


# Page Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🚀 BestFit.AI</h1>", unsafe_allow_html=True)

# Introduction
st.markdown(
    """
    <div style="text-align: center; font-size: 18px;">
        <b>Find the Best Jobs & Optimize Your Resume for Success! 🎯</b><br>
        Our AI-driven platform helps you land your dream job by matching your resume with top job listings and optimizing it for ATS systems.
    </div>
    """,
    unsafe_allow_html=True
)

# Features Section
st.markdown("""
    ### 🔥 What We Offer?
    🛠 **Find the Best Jobs** – Upload your resume, and we’ll match you with top job listings based on your skills.<br>
    📊 **ATS Score & Optimization** – See how well your resume matches a job description and get suggestions to improve it.<br>
    🚀 **Direct Apply Links** – No more searching! Instantly access job application links.<br>
    📈 **Resume Enhancement Tips** – Boost your chances of getting shortlisted with AI-powered insights.<br>
    """, unsafe_allow_html=True)

# How It Works
st.markdown("""
    ### 📌 How It Works?
    1️⃣ **Find the Best Jobs**  
       - Upload your resume 📄  
       - AI extracts key skills & experience 🔍  
       - Matches jobs from **LinkedIn, Indeed, etc.** 📢  
       - Provides ATS score & **direct apply links** 🚀  
    
    2️⃣ **Optimize Your Resume for ATS**  
       - Upload your resume & job description 📝  
       - Get an ATS compatibility score 📊  
       - Receive **custom AI-powered improvement tips** to boost your resume 💡  
    """, unsafe_allow_html=True)
    
# User Selection Box
select = st.selectbox(
    "What would you like to do?",
    ["Select an option", "🔍 Find a Job", "📊 Get ATS Score"]
)

#for finding jobs based on resume
if select == "🔍 Find a Job":
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf", "docx"])
    remote_only=st.selectbox("Remote Only",options=["False","True"])
    employment_type=st.selectbox("Employment Type",options=["Full-time","Part-time","Contract","Internship"])
    job_location=st.text_input("Enter Job Location")
    
    if uploaded_file and job_location and remote_only and employment_type:
        resume_text = parse_resume(uploaded_file)
        job_profile = job_profiles(resume_text['text'])
        experience_years = experience(resume_text['text'])

        st.write(f"### Best Job Profiles for you: {job_profile}")
        st.write(f"### Total Experience: {experience_years}")
        job_to_search = [job.strip() for job in job_profile.split(",")]


        # Fetch jobs using extracted skills
        jobs_set1 = fetch_jobs(job_to_search[0],job_location,remote_only,employment_type,experience_years) 
        jobs_set2 = fetch_jobs(job_to_search[1],job_location,remote_only,employment_type,experience_years)
        jobs_set3 = fetch_jobs(job_to_search[2],job_location,remote_only,employment_type,experience_years)
        all_jobs = jobs_set1 + jobs_set2 + jobs_set3


        # Styling for the job cards

        st.markdown(
            """
            <style>
                .job-card {
                    background-color: #000000;
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                    margin-bottom: 15px;
                }
                .job-title {
                    font-size: 18px;
                    font-weight: bold;
                    color: #f8f8ff;
                }
                .job-details {
                    font-size: 14px;
                    color: #f8f8ff;
                }
                .company-logo {
                    width: 20px;  /* Small Logo Size */
                    height: 20px;
                    margin-right: 10px;
                    vertical-align: middle;
                }
                .apply-button {
                    display: inline-block;
                    background-color: #151414;
                    color: white;
                    padding: 8px 15px;
                    border-radius: 5px;
                    text-align: center;
                    text-decoration: none;
                    font-size: 14px;
                    font-weight: bold;
                }
                .apply-button:hover {
                    font-weight: bold;
                    font-size: 16px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
    
        if all_jobs:
            st.write("### Matching Jobs")
    
            # Display job listings
            for job in all_jobs:
                with st.container():  # Creates a box around each job listing
                    st.markdown(f"""
                        <div class="job-card">
                            <p class="job-title">{job['title']}</p>
                            <p class="job-details">
                                <img class="company-logo" src="{job['logo']}" alt="Company Logo"> {job['company']}
                            </p>
                            <p class="job-details">📍 {job['location']}</p>
                            <a class="apply-button" href="{job['url']}" target="_blank">🔗 Link to Apply</a>
                        </div>
                    """, unsafe_allow_html=True)

        else:
            st.write("No matching jobs found.")


# for ATS score
if select == "📊 Get ATS Score":
    resume=st.file_uploader("Upload Your Resume in PDF or in DOCX",type=['pdf','docx'])
    job_description=st.text_area("Paste Job Description")


    if resume and job_description:
        resume_text = parse_resume(resume)
        ats= scoring(resume_text,job_description)

        # Custom Styling for a Single Box
        st.markdown(
                """
                <style>
                    .ats-container {
                        background-color: #000000;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                        margin-bottom: 20px;
                        text-align: left;
                        font-size: 16px;
                        line-height: 1.6;
                    }
                    .ats-score {
                        font-size: 22px;
                        font-weight: bold;
                        color: #007BFF;
                   }
                    .highlight {
                        color: #28A745;
                        font-weight: bold;
                    }
                </style>
                """,
                unsafe_allow_html=True
            )
        
        # Display ATS Score and Suggestions Inside a Single Styled Box
        st.markdown(f"""
                <div class="ats-container">
                    {ats}
                </div>
                """, unsafe_allow_html=True)

        

