from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st
load_dotenv()
# Load API key from Streamlit secrets
api_key = st.secrets["GOOGLE_API_KEY"]["api_key"]

model=ChatGoogleGenerativeAI(model='gemini-2.0-flash-thinking-exp-01-21',google_api_key=api_key)

#to get ATS score and suggestions to improve resume
def scoring(resume,job_description):
    score=model.invoke(f""" 
                       You are an ATS Score expert with 10+ years of experience in this field.
                       I will provide you with my resume and job description, and you will:

                       Evaluate my ATS score based on the job description.
                       Give me suggestions to improve it under these categories:
                       Keywords and Skills
                       Experience and Projects
                       Other Improvements
                       Response Format:
                       Display my ATS score in bold and large font (e.g., ATS Score is 45/100)
                       (compalsary to keep in bold and big font).
                       don't keep the suggestions too long.
                       If the provided content is not a resume, simply return this message in bold and big letters:
                       "IT'S NOT A RESUME". and if its a resume you do not need to say that its a resume.
                        (Detect this by checking for key sections like "Skills," "Experience," and "Education.")
                       Now, here is my resume and job description:
                       resume_content:{resume}, 
                       job_description:{job_description}.""")
    return score.content


#to get best 3 job profiles based on resume
def job_profiles(resume):
    jobs=model.invoke(f"""You are an expert with 10+ years of experience in selecting job profiles based 
                      on resumes.
                      
                      I will provide you with a resume, and you will analyze it to determine the best 3 
                      job profiles that match the person's skills and experience.

                      Response Format:
                      Provide only a list of 3 job profiles in this format:
                      Job Profile 1, Job Profile 2, Job Profile 3
                      Do not include any explanations—only the list.
                      the output should be in list format.
                      Now, here is the resume:
                      resume_content:{resume}.""" )
    return jobs.content



#to get total experience from resume
def experience(resume):
    experience=model.invoke(f"""You are an expert with over 10 years of experience in extracting total 
                            working experience from resumes.  
                            
                            I will provide you with a resume, and your task is to extract the candidate's 
                            **total years of full-time and internship working experience** 
                            (excluding project-based experience).  
                            
                            ### Response Format:  
                            - Provide only a **single numeric value** followed by **"years"** or **"months"** 
                            if the experience is less than one year (e.g., '10 years' or '3 months').  
                            - If the experience cannot be determined, return **'1 year'**.  
                            
                            Now, here is the resume:  
                            resume_content: {resume}""")
    return experience.content

                      
def tailored_resume(resume,job_description):
    tailored_resume=model.invoke(f"""  You are an expert with over 10 years of experience in tailoring resumes to job descriptions.

I will provide you with a resume and a job description. Your task is to tailor the resume to the job description by modifying, adding, or removing content as necessary. Ensure that the tailored resume is structured professionally and formatted in HTML.

Instructions:
Maintain the following sections in the resume:

Contact Information
Professional Summary (Only if the candidate has more than 2 years of experience)
Skills
Experience
Projects (Include only if the resume contains project details)
Education
Certifications (Include only if available in the provided resume)
Customizations Based on Job Description:

Align skills, experience, and projects with the job description.
Use keywords and responsibilities from the job description where applicable.
Remove irrelevant details that do not match the job description.
Formatting Requirements:

The response must be in HTML code (but in string format) following the structure below.
Use <hr> to separate sections for a clean format.
Keep the design simple and professional.
Rules for Exclusions:

Do not include a Professional Summary if the candidate has less than 2 years of experience.
Do not include a Projects or Certifications section if the original resume does not have relevant information.
Now, here is the resume and job description:

Resume:
{resume}

Job Description:
{job_description}

Your Response Format:
Provide the tailored resume as an HTML code block following this structure:

html
Copy
Edit
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>(Candidate Name) - Resume</title>
    <style>
        body (font-family: Arial, sans-serif; margin: 40px; )
        h1, h2 ( color: #333; )
        .section ( margin-bottom: 20px; )
        hr (border: 1px solid #333; margin: 20px 0; )
        ul () padding-left: 20px; )
    </style>
</head>
<body>
    <h1>(Candidate Name)</h1>
    <p>Email: (Email) | Phone: (Phone) | LinkedIn: id</p>
    <hr>

    (Professional Summary (if applicable))

    <div class="section">
        <h2>Skills</h2>
        <ul>
            <li><strong>Languages:</strong> (Languages)</li>
            <li><strong>Libraries:</strong> (Libraries)</li>
            <li><strong>Tools:</strong> (Tools)</li>
            <li><strong>Domains:</strong> (Domains)</li>
        </ul>
    </div>
    <hr>

    <div class="section">
        <h2>Experience</h2>
        Experience Details
    </div>
    <hr>

    Projects Section (if applicable)

    <div class="section">
        <h2>Education</h2>
        Education Details
    </div>
    <hr>

    (Certifications Section (if applicable))

</body>
</html>
Do not include any explanations or additional comments. Your response should only contain the tailored resume in the given HTML format.



""")
    return tailored_resume.content
