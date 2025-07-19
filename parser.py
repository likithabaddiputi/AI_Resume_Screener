import streamlit as st
import pdfplumber
import re
import string 
from nltk.corpus import stopwords
import sys

stop_words = set(stopwords.words('english'))


st.title("Welcome to Resume Screener")
st.write("📄 AI-Powered Resume Screener – Extract and Analyse your resume for your desired job role")
 

    
epattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
ephone = r'(?:\+91[\-\s]?)?[6-9]\d{9}'

skillset = ["python", "java", "c++", "c", "javascript", "typescript", "kotlin", "swift", "go", "ruby", "rust", "html", "css", "javascript", "react", "node", "express", "bootstrap", "tailwind", "next.js"
, "sql", "mysql", "postgresql", "sqlite", "mongodb", "redis", "firebase", "machine learning", "deep learning", "computer vision", "nlp", "scikit-learn", "tensorflow", "keras", "pytorch"
, "pandas", "numpy", "matplotlib", "seaborn", "data analysis", "data visualization", "power bi", "excel", "git", "github", "linux", "docker", "kubernetes", "ci/cd", "bash", "terminal", "vscode"
, "flask", "django", "fastapi", "api", "rest", "graphql", "oop", "dsa", "problem solving", "debugging", "testing", "unit testing", "agile", "scrum"
]

education_keywords = ["b.tech", "m.tech", "be", "pu", "class 10", "10th", "12th", "class 12",
                      "engineering", "college", "university", "rvce", "iit", "school", "cbse", "puc"]
                      
experience_keywords = [
    "intern", "internship", "worked", "developed", "built",
    "created", "designed", "led", "managed", "contributed",
    "collaborated", "project", "experience", "volunteer", "freelance",
    "research", "engineer", "software", "trainee", "job"
]

def match(rskills, jskills):
    matched = []
    for skill in rskills:
        if skill.lower() in [j.lower() for j in jskills]:
            matched.append(skill.title())
    if len(jskills) == 0:
        return 0
        
    missed_skills = [skill for skill in jskills if skill not in matched]

    ats_score = (len(matched) / len(jskills)) * 100
    return round(ats_score, 2), missed_skills

def extract_name(text):
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        if line.lower().startswith("name:"):
            return line.split(":", 1)[1].strip()
        elif "resume of" in line.lower():
            return line.lower().split("resume of", 1)[1].strip().title()
        elif idx == 0:
            return line.strip()
    return "Unknown"

    
def extract_email(text):
    matches = re.findall(epattern, text)
    return matches
    
def extract_phone(text):
    match = re.findall(ephone , text)
    return match

def extract_skills(text):
    matched_skills = []
    text = text.lower()
    for skill in skillset:
    
        if skill in text:
            matched_skills.append(skill.title().strip())
        
    return list(set(matched_skills))
    
def extract_education(text):
    matched_education = []
    text = text.lower().splitlines()
    for line in text:
        for edu in education_keywords:
            if edu in line:
                matched_education.append(line.title().strip())
        
    return list(set(matched_education))

def extract_experience(text):
    matched_experience = []
    text = text.lower().splitlines()
    for line in text:
        for exp in experience_keywords:
            if exp in line:
                matched_experience.append(line.title().strip())
    return list(set(matched_experience))
    
def clean_text(jtext):
    jtext = jtext.lower().strip()
    
    required = []
    
    for skill in skillset:
        if skill in jtext:   # just use skill as is (already lowercase)
            required.append(skill.title())  # keep the title case for display
        
    return required

left_col, right_col = st.columns(2)

    
rtext = st.file_uploader("Upload your resume", type = ['txt','pdf'])
jtext = st.text_area("Enter Job description")                                                                                           

required_skills = clean_text(jtext)

if rtext is not None:
    if st.button("Extract"):
        if rtext.type == "application/pdf":
            with pdfplumber.open(rtext) as pdf:
                content = ''
                for page in pdf.pages:
                    content += page.extract_text() + '\n'
        else:
            content = rtext.read().decode("utf-8")
            
        resume = {
        "Name": extract_name(content),
        "Email": extract_email(content),
        "Phone" : extract_phone(content),
        "Skills" : extract_skills(content),
        "Education" : extract_education(content),
        "Experience": extract_experience(content) 
}
        with left_col:
            for key in resume:
                st.subheader(key)
                value = resume[key]
                if isinstance(value, list):
                    if value:
                        for item in value:
                            st.write(f"- {item}")
                    else:
                        st.write("Not found")
                else:
                    st.write(value or "Not found")
        
        
        with right_col:
            score, missed_skills = match(resume["Skills"], required_skills)
            st.subheader("🎯 ATS Resume Score")
            st.write(f"Your resume matches **{score}%** of the required skills.")
            
            st.subheader("Consider adding the below ones to your resume")
            for skill in missed_skills:
                st.markdown(f"- {skill}")
                
            

        
        




