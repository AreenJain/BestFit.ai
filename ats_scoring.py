from langchain_google_genai import ChatGoogleGenerativeAI
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
                       Display my ATS score in bold and large font (e.g., 45/100)(compalsary to keep in bold and big font).
                       don't keep the suggestions too long.
                       If the provided content is not a resume, simply return this message in bold and big letters:
                       "THIS IS NOT A RESUME. and is its a resume you do not need to say that its a resume"
                        (Detect this by checking for key sections like "Skills," "Experience," and "Education.")
                       Now, here is my resume and job description:
                       resume_content:{resume}, 
                       job_description:{job_description}.""")
    return score.content


#to get best 3 job profiles based on resume
def job_tittle(resume):
    jobs=model.invoke(f"""You are an expert with 10+ years of experience in selecting job profiles based on resumes.

                    I will provide you with a resume, and you will analyze it to determine the best 3 job profiles that match the person's skills and experience.

                    Response Format:
                    Provide only a list of 3 job profiles in this format:
                    Job Profile 1, Job Profile 2, Job Profile 3
                    Do not include any explanations—only the list.
                      the output should be in list format.
                    Now, here is the resume:
                    resume_content:{resume}.""")
    return jobs.content

                      