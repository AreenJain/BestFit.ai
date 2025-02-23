import docx
import re
import fitz 


#extract text from pdf
def extract_text_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text

#extract text from docs
def extract_text_doc(docx_file):
    doc = docx.Document(docx_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

#preprocess text
def preproces(text):
    text=re.sub(r'\s+', ' ', text)
    return text.lower().strip()




def parse_resume(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type=='pdf':
        text=extract_text_pdf(uploaded_file)

    elif file_type=='docx':
        text=extract_text_doc(uploaded_file)

    else:
        return"error"
    
    text=preproces(text)

    return {
        "text": text
    }

    
