# Tantomi API

The backend service for Tantomi — a skill progress tracking app for the 
Baguio tech community. Built with FastAPI and powered by AI.

## Overview

This API provides the core intelligence layer for Tantomi:

* **Resume Parsing:** Accepts PDF resume uploads and extracts technical 
  skills and proficiency levels using LangChain and GPT-4o-mini.
* **Event Match Scoring:** Compares a user's skill profile against event 
  topics and returns a weighted match percentage, matched topics, and 
  missing topics.
* **Learning Recommendations:** Retrieves curated learning resources from 
  a ChromaDB vector knowledge base, falling back to Tavily web search for 
  niche topics, then generates a personalized pre-event briefing using GPT.

## Technical Stack

* **Language:** Python 3.12
* **Framework:** FastAPI
* **AI / LLM:** LangChain, OpenAI GPT-4o-mini
* **Vector Database:** ChromaDB with OpenAI text-embedding-3-small
* **Web Search Fallback:** Tavily Search API
* **PDF Parsing:** PyMuPDF (fitz)
* **Data Validation:** Pydantic v2
* **Environment:** Uvicorn, python-dotenv

## Project Structure

| File | Responsibility |
|------|---------------|
| `app/main.py` | FastAPI routes and server startup |
| `app/models.py` | Pydantic schemas |
| `app/services/parser.py` | PDF text extraction |
| `app/services/extractor.py` | LangChain skill extraction |
| `app/services/scorer.py` | Match score calculation |
| `app/services/knowledge_base.py` | ChromaDB vector store |
| `app/services/recommender.py` | Hybrid retrieval + GPT briefing |
| `app/data/resources.json` | Curated learning resource knowledge base |

## API Endpoints

* **POST /parse-resume** — Accepts a PDF file upload and returns extracted 
  skills and proficiency levels as structured JSON.
* **POST /calculate-match-score** — Accepts a user skill profile and event 
  topics, returns a match percentage, matched topics, and missing topics.
* **POST /recommendations** — Accepts missing topics and event details, 
  returns a GPT-generated pre-event briefing and 2-3 curated learning resources.

## Execution Instructions

1. Clone the repository and navigate to the project folder.
2. Create and activate a virtual environment: `python -m venv venv` then `.\venv\Scripts\Activate.ps1`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your API keys:
   OPENAI_API_KEY=your_openai_key_here
   TAVILY_API_KEY=your_tavily_key_here
5. Start the server: `uvicorn app.main:app --reload`
6. Visit `http://localhost:8000/docs` to access the interactive API documentation.

---

**Author:** Verah Dulay  
**Date:** April 2026
