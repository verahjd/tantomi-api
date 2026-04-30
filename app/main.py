from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.services.parser import extract_text_from_pdf
from app.services.extractor import extract_skills
from app.models import MatchScoreInput, RecommendationInput
from app.services.scorer import calculate_match_score as compute_match_score
from app.services.recommender import recommend_resources
from app.services.knowledge_base import build_knowledge_base
from app.auth import verify_api_key
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    build_knowledge_base()
    yield

app = FastAPI(lifespan=lifespan)  

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],  
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["Content-Type", "X-API-Key"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/parse-resume", dependencies=[Depends(verify_api_key)])
async def parse_resume(file: UploadFile):
    contents = await file.read()
    text = extract_text_from_pdf(contents)
    skills = extract_skills(text)
    return skills

@app.post("/calculate-match-score", dependencies=[Depends(verify_api_key)])
async def calculate_match_score(data: MatchScoreInput):
    result = compute_match_score(data)
    return result

@app.post("/recommendations", dependencies=[Depends(verify_api_key)])
async def recommendations(data: RecommendationInput):
    result = recommend_resources(
        missing_topics=data.missing_topics,
        event_title=data.event_title,
        event_level=data.event_level
    )
    return result