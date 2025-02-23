import streamlit as st
from resume_parser import parse_resume
from job_fetcher import fetch_jobs
from ats_scoring import scoring, job_tittle
import os
import ast
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
    job_location=st.text_input("Enter Job Location")
    
    if uploaded_file and job_location:
        resume_text = parse_resume(uploaded_file)
        job_to_search=job_tittle(resume_text['text'])
        st.write(f"### Best Job Profiles for you: {job_to_search}")
        job_to_search = [job.strip() for job in job_to_search.split(",")]


        # Fetch jobs using extracted skills
        jobs_set1 = fetch_jobs(job_to_search[0],job_location) 
        jobs_set2 = fetch_jobs(job_to_search[1],job_location)
        jobs_set3 = fetch_jobs(job_to_search[2],job_location)
        all_jobs = jobs_set1 + jobs_set2 + jobs_set3
    
        if all_jobs:
            st.write("### Matching Jobs")
    
            for job in all_jobs:

                # Display job details with ATS Score
                st.markdown(f"**[{job['title']} - {job['company']} - {job['location']}]({job['url']})**")

        else:
            st.write("No matching jobs found.")


# for ATS score
if select == "📊 Get ATS Score":
    resume=st.file_uploader("Upload Your Resume in PDF or in DOCX",type=['pdf','docx'])
    job_description=st.text_area("Paste Job Description")


    if resume and job_description:
        resume_text = parse_resume(resume)
        ats= scoring(resume_text,job_description)

        st.write(ats)

        

