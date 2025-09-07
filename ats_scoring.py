from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
import streamlit as st
load_dotenv()
# Load API key from Streamlit secrets
api_key = st.secrets["GOOGLE_API_KEY"]

model = ChatGoogleGenerativeAI(model='gemini-2.5-pro',google_api_key=api_key, temperature=0)

# to get ATS score and suggestions to improve resume
def scoring(resume, job_description):
    template = PromptTemplate(
        template="""
        You are an ATS Score expert with 10+ years of experience in this field.
        I will provide you with my resume and job description, and you will:

        **Evaluate my ATS score based on the job description.**  
        **Provide suggestions to improve it under these categories:**  
           - ### **Keywords and Skills**  
           - ### **Experience and Projects** 
           -### **Formatting errors** 
           - ### **Other Improvements**  
           - ### **Important Note ** 

        Response Format:
        ---

        ### **ATS Score must be displayed in bold and large font** (e.g., ATS Score: 45/100).
        - **Suggestions should be concise and to the point.**  
        - Use **emojis** to make output more attractive.
        - If the provided content **is not a resume**, return this message:  
          **"IT'S NOT A RESUME"** in **bold and big letters** (Detect this by checking for sections like "Skills," "Experience," and "Education").  
        - Write a section titled '### Important Note' in markdown format. If the job requires X years of experience and the user has
        less than X years, state that requirement clearly. If the user meets or exceeds the required experience, provide an important 
        insight under this section, such as a key achievement, relevant project, or a strong skill that makes them a great fit.

        
        Resume Content: {resume}  

        Job Description:{job_description}  
        """,
        input_variables=['resume', 'job_description']
    )

    prompt = template.invoke({'resume': resume, 'job_description': job_description})
    result = model.invoke(prompt)
    return result.content

# to get best 3 job profiles based on resume
def job_profiles(resume):
    template = PromptTemplate(
        template="""You are an expert with 10+ years of experience in selecting job profiles based 
        on resumes.

        I will provide you with a resume, and you will analyze it to determine the best 3 
        job profiles that match the person's skills and experience.

        ### Response Format:
        Provide only a **comma-separated list** of 3 job profiles in this format:
        Job Profile 1, Job Profile 2, Job Profile 3
        
        Do not include any explanations—only the list.

        Now, here is the resume:
        resume_content: {resume}
        """,
        input_variables=['resume']
    )

    prompt = template.invoke({'resume':resume})
    result = model.invoke(prompt)
    return result.content


# to get total experience from resume
def extract_experience(resume):
    template = PromptTemplate(
        template="""You are an expert with over 10 years of experience in extracting total 
        working experience from resumes.  

        I will provide you with a resume, and your task is to extract the candidate's 
        **total years of full-time and internship working experience** 
        (excluding project-based experience).  

        ### Response Format:  
        - Provide only a **single numeric value** followed by **"years"** or **"months"** 
        if the experience is less than one year (e.g., '10 years' or '3 months').  
        - If the experience cannot be determined, return **'0 years'**.  

        Now, here is the resume:  
        resume_content: {resume}""",
        input_variables=['resume']
    )

    prompt = template.invoke({'resume':resume})
    result = model.invoke(prompt)
    return result.content.strip()


def tailored_resume(resume, job_description):
    template = PromptTemplate(
        template="""You are an expert with over 10 years of experience in tailoring resumes to job descriptions.

        I will provide you with a resume and a job description. Your task is to tailor the resume to the job description by modifying, adding, or removing content as necessary. Ensure that the tailored resume is structured professionally and formatted in HTML.

        Instructions:
        - Maintain the following sections in the resume:
            - Contact Information
            - Professional Summary (Only if the candidate has more than 2 years of experience,extract the candidate's 
                **total years of full-time and internship working experience** 
                (excluding project-based experience).)
            - Skills
            - Experience
            - Projects (Include only if the resume contains project details)
            - Education
            - Certifications (Include only if available in the provided resume and add certificate which are releted to job)

        Customizations Based on Job Description:
        - Align skills, experience, and projects with the job description.
        - Use keywords and responsibilities from the job description where applicable.
        - Remove irrelevant details that do not match the job description.

        Formatting Requirements:
        - The response must be in HTML code (but in string format) following the structure below.
        - Use <hr> to separate sections for a clean format.
        - Keep the design simple and professional.

        Now, here is the resume and job description:

        Resume:
        {resume}

        Job Description:
        {job_description}

        Your Response Format:
        Provide the tailored resume as an HTML code block following this structure:

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>(Candidate Name) - Resume</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1, h2 {{ color: #333; }}
                .section {{ margin-bottom: 20px; }}
                hr {{ border: 1px solid #333; margin: 20px 0; }}
                ul {{ padding-left: 20px; }}
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
        """,
        input_variables=['resume', 'job_description']
    )

    prompt = template.invoke({'resume':resume, 'job_description':job_description})    
    result = model.invoke(prompt)
    return result.content



#linked in profile otimization

def linkedin_optimization(profile):
    if not profile:
        return "❌ Error: No profile data provided. Please upload a valid LinkedIn profile PDF."

    # Correct usage of PromptTemplate
    template = PromptTemplate(
        template="""You are an expert in LinkedIn profile optimization, specializing in enhancing professional 
        visibility and engagement. When I provide a LinkedIn profile as a PDF, your task is to analyze 
        the content and offer structured, actionable feedback.

        Your response should follow this format and do not add anything else:

        ---
        ### **Rating & Review of Your LinkedIn Profile**

        ---
        ### **Overall Rating: X/10 🚀** 
        (A general assessment of the profile’s strength and what makes it stand out.)

        ---
        ### **Strengths 💪**
        ✅ Highlight the strongest aspects of the profile (skills, achievements, certifications, internships, etc.).

        ---
        ### **Areas to Improve 🔧**
        1️⃣ **Expand Your Experience Section**  
        - Suggest how the user can make their experience more impactful (adding **quantifiable metrics, problem-solving approaches, real-world impact**).  

        2️⃣ **Add More Projects**  
        - Recommend adding **NLP, AI, or domain-specific projects** that align with their skills.  

        3️⃣ **Showcase More Soft Skills**  
        - Explain how they can include **communication, teamwork, or leadership skills effectively**.  

        4️⃣ **Add More Keywords for Better Visibility**  
        - Provide **ATS-friendly keywords** relevant to their expertise (e.g., "Data Science, LLMs, Hugging Face, TensorFlow").  

        5️⃣ **Customize Your LinkedIn URL**  
        - Suggest making the profile URL more professional (e.g., `linkedin.com/in/firstnamelastname`).  

        ---
        ### **Final Suggestions 📌**
        1. Summarize key actions they should take.  
        2. Encourage **engagement on LinkedIn** (posting insights, commenting, networking).  
        3. Suggest **ways to improve personal branding**.  

        **Output should be concise, actionable, and easy to follow.** Focus on practical steps that can 
        immediately enhance their LinkedIn profile visibility and impact.  

        **Here is the LinkedIn profile data:**  
        ```  
        {profile}  
        ```
        """,
        input_variables=["profile"] 
    )

    prompt = template.format(profile=profile)
    result = model.invoke(prompt)
    return result.content


def prepare_for_job_interview(user_input, chat_history):
    template = ChatPromptTemplate.from_template( """
                 You are an advanced AI mock interview coach. Ask the user to enter either a job title or full job description. 
                  Based on the input, generate role-specific technical and behavioral interview questions.

Evaluate answers with:
- Strengths and weaknesses
- Clear improvement suggestions
- Confidence rating (1-10)
- Follow-up tips

**Chat History (for context):** {chat_history}  

---
### **User Input:**  
{user_input} 

Keep the interaction professional and supportive. Prepare them thoroughly for real interviews.
""")

    # Format the prompt with chat history & user input
    formatted_prompt = template.format(
        user_input=user_input, 
        chat_history="\n".join(chat_history) if chat_history else "No previous messages"
    )

    response = model.invoke(formatted_prompt)
    return response.content

