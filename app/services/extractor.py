from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.models import ResumeSkills
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert resume parser.
     Extract only technical skills — programming languages, 
     frameworks, tools, and technologies.
     Ignore soft skills like communication or teamwork.
     Assess each skill's level as: beginner, intermediate, or advanced."""),
    ("human", "Parse this resume and extract the skills:\n\n{resume_text}")
])

def extract_skills(text: str) -> ResumeSkills:    
    chain = prompt | model.with_structured_output(ResumeSkills)
    result = chain.invoke({"resume_text": text})
    return result

