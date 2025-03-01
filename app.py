import streamlit as st
from resume_parser import parse_resume
from job_fetcher import fetch_jobs
from ats_scoring import scoring, job_profiles,extract_experience, tailored_resume,linkedin_optimization
import pdfkit
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

st.set_page_config(page_title="BestFit.AI", page_icon="🚀", layout="wide")

# Page Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🚀 BestFit.AI</h1>", unsafe_allow_html=True)

# Introduction
st.markdown(
    """
    <div style="text-align: center; font-size: 20px;">
        <b> Your AI-Powered Job Assistant! 🎯</b><br>
        Optimize your resume, match with top job listings, and generate tailored resumes effortlessly.
    </div>
    """, unsafe_allow_html=True
)

# Features Section
st.markdown("""
### 🔥 Key Features  
🔍 **Find the Best Jobs** – AI matches your resume with top job listings & provides direct apply links.  
📊 **ATS Score & Resume Optimization** – Get an ATS score & AI-powered improvement suggestions.  
📝 **Tailored Resume Generator** – Upload job descriptions & generate an optimized resume instantly.  
🔗 **LinkedIn Profile Optimizer** – Enhance your LinkedIn profile with AI-driven suggestions for better visibility.  
""", unsafe_allow_html=True)

# How It Works
st.markdown("""
### 📌 How It Works  
1️⃣ **Find Jobs** – Upload resume & get matched job listings with apply links.  
2️⃣ **Optimize Resume** – Upload job descriptions & improve ATS compatibility.  
3️⃣ **Generate Tailored Resume** – AI rewrites & optimizes your resume for the job.  
4️⃣ **Optimize LinkedIn Profile** – Get AI-powered insights to enhance your LinkedIn profile.  
""", unsafe_allow_html=True)

    
# User Selection Box
select = st.selectbox(
    "What would you like to do?",
    ["Select an option", "🔍 Find a Job", "📊 ATS Insights","🤖AI-Optimized Resume","🚀LinkedIn Profile Optimizer"]
)

#for finding jobs based on resume
if select == "🔍 Find a Job":
    st.title("🔍 Find a Job")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf", "docx"])
    remote_only=st.selectbox("Remote Only",options=["False","True"])
    employment_type=st.selectbox("Employment Type",options=["fulltime","parttime","contract","internship"])
    job_location=st.text_input("Enter Job Location")
    go=st.button("Find Jobs")
    if not uploaded_file and go:
        st.warning("Please upload your resume to find jobs.")
    if not job_location and go:
        st.warning("Please enter the job location to find jobs.")

    
    if go and uploaded_file and job_location and remote_only and employment_type:
        resume_text = parse_resume(uploaded_file)
        job_profile = job_profiles(resume_text['text'])
        experience_years = extract_experience(resume_text['text'])

        st.write(f"### Best Job Profiles for you: {job_profile}")
        st.write(f"### Total Experience: {experience_years}")
        job_to_search = [job.strip() for job in job_profile.split(",")]


        # Fetch jobs using extracted skills
        jobs_set1 = fetch_jobs(job_to_search[0],job_location,remote_only,employment_type) 
        jobs_set2 = fetch_jobs(job_to_search[1],job_location,remote_only,employment_type)
        jobs_set3 = fetch_jobs(job_to_search[2],job_location,remote_only,employment_type)
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
                            <p class="job-title">{job['title'] } - {job['company']}</p>
                            <p class="job-details">
                                Date Posted : {job['date_posted']} on {job['site']}
                            </p>
                            <p class="job-details">📍 {job['location']}</p>
                            <a class="apply-button" href="{job['url']}" target="_blank">🔗 Link to Apply</a>
                        </div>
                    """, unsafe_allow_html=True)

        else:
            st.write("No matching jobs found.")


# for ATS score
if select == "📊 ATS Insights":
    st.title("📊 ATS Insights")
    resume=st.file_uploader("Upload Your Resume in PDF or in DOCX",type=['pdf','docx'])
    job_description=st.text_area("Paste Job Description")
    go=st.button("Get Insights")

    if not resume and go:
        st.warning("Please upload your resume to get insights.")
    if not job_description and go:
        st.warning("Please paste the job description to get insights.")

    if go and resume and job_description:
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

     


if select == "🤖AI-Powered Resume Customization":
    st.title("🤖AI-Optimized Resume")
    resume=st.file_uploader("Upload Your Resume in PDF or in DOCX",type=['pdf','docx'])
    job_description=st.text_area("Paste Job Description")
    go=st.button("Generate Tailored Resume")

    if not resume and go:
        st.warning("Please upload your resume to generate a tailored resume.")
    if not job_description and go:
        st.warning("Please paste the job description to generate a tailored resume.")

    if go and resume and job_description:
        resume_text = parse_resume(resume)
        new_tailored_resume=tailored_resume(resume_text,job_description)
        import pdfcrowd
        import sys
        API = st.secrets["API"]

        try:
             # Create an API client instance.
             client = pdfcrowd.HtmlToPdfClient('areen_jain_', API)

             # Specify the mapping of HTML content width to the PDF page width.
             # To fine-tune the layout, you can specify an exact viewport width, such as '960px'.
             client.setContentViewportWidth('balanced')
             pdf_path = "Tailored.pdf"

             # Run the conversion and save the result to a file.
             client.convertStringToFile(new_tailored_resume, pdf_path)
    
        except pdfcrowd.Error as why:
            sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))
            raise
       

        # Provide download option
        with open(pdf_path, "rb") as f:
            st.download_button(label="📥 Download Tailored Resume",
                               data=f,
                               file_name="Tailored_Resume.pdf",
                               mime="application/pdf")


#optimizing linkedin profile
if select == "🚀LinkedIn Profile Optimizer":
    st.title("🚀 LinkedIn Profile Optimizer")
    st.write("Upload your LinkedIn Profile PDF (Go to **your profile → More → Save to PDF**) and get a detailed **review & improvement suggestions**.")

    profile=st.file_uploader("Upload Your Resume in PDF or in DOCX",type=['pdf'])
    go=st.button("Optimize LinkedIn Profile")

    if not profile and go:
        st.warning("Please upload your LinkedIn profile to optimize it.")
    
    if go and profile:
        resume_text = parse_resume(profile)
        suggestions= linkedin_optimization(resume_text)
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
                    {suggestions}
                </div>
                """, unsafe_allow_html=True)
