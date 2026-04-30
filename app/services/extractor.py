from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.models import ResumeSkills
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert resume parser. Extract technical skills from resumes.

For each technical skill (programming languages, frameworks, tools, technologies), output an object with:
- name: the skill name (e.g. "Python", "React")
- level: "beginner", "intermediate", or "advanced"

Use these signals to assign levels:
- beginner: mentioned briefly, used in coursework, no project context
- intermediate: used in personal/academic projects with clear application
- advanced: used in professional work, multiple projects, or as a primary specialization

Ignore soft skills like communication or teamwork."""),
    ("human", "Parse this resume and extract the skills:\n\n{resume_text}")
])

def extract_skills(text: str) -> ResumeSkills:    
    chain = prompt | model.with_structured_output(ResumeSkills, method="function_calling")
    result = chain.invoke({"resume_text": text})
    return result