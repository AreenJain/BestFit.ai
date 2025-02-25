from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from dotenv import load_dotenv
load_dotenv()


model=ChatGoogleGenerativeAI(model='gemini-2.0-flash-thinking-exp-01-21')

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

                      