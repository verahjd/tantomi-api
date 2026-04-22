import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tavily import TavilyClient
from app.models import RecommendationOutput, ResourceItem
from app.services.knowledge_base import search_resources

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def recommend_resources(
        missing_topics: list[str],
        event_title: str,
        event_level: str
) -> RecommendationOutput:
    if not missing_topics:
        return RecommendationOutput(
            briefing=f"You are well prepared for the event. No additional resources are needed.",
            resources=[]
        )
    
    all_resources = []
    
    for topic in missing_topics:
        query = topic
        chroma_results = search_resources(query)

        if chroma_results and chroma_results[0]["distance"] < 0.5:
            for result in chroma_results:
                all_resources.append(ResourceItem(
                    title=result["title"],
                    url=result["url"],
                    topic=result["topic"],
                    level=result["level"],
                    description=result["description"]
                ))
        else:
            tavily_response = tavily_client.search(query=f"{topic} {event_level} learning resource", max_results=3) 

            for result in tavily_response["results"]:
                all_resources.append(ResourceItem(
                    title=result["title"],
                    url=result["url"],
                    topic=topic,
                    level=event_level,
                    description=result["content"]
                ))
    all_resources = all_resources[:3]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful learning advisor for tech events.
        Write a short, friendly 2-3 sentence briefing explaining what the user 
        needs to know before attending this event based on their missing topics.
        Keep it encouraging and simple."""),
        ("human", "Event: {event_title} ({event_level} level)\nMissing topics: {missing_topics}")
    ])

    chain = prompt | llm
    briefing = chain.invoke({
        "event_title": event_title,
        "event_level": event_level,
        "missing_topics": ", ".join(missing_topics)
    }).content
        
        
    return RecommendationOutput(
        briefing=briefing,
        resources=all_resources
    )