from pydantic import BaseModel, Field
from typing import List, Dict

class SkillItem(BaseModel):
    name: str = Field(..., description='Name of the skill')
    level: str = Field(..., description='Proficiency level: beginner, intermediate, or advanced')

class ResumeSkills(BaseModel):
    skills: List[SkillItem] = Field(
        default_factory=list,
        description='List of skills extracted from the resume, each with a name and proficiency level'
    )

class MatchScoreInput(BaseModel):
    user_skills: List[str] = Field(..., description='List of user skills')
    user_skill_levels: Dict[str, str] = Field(...,description='Dictionary mapping each skill to its proficiency level')
    event_topics: List[str] = Field(..., description='List of event topics')

class MatchScoreOutput(BaseModel):
    match_topics: List[str] = Field(..., description='List of event topics that match the user skills')
    missing_topics: List[str] = Field(..., description='List of event topics that do not match the user skills')
    match_score: float = Field(..., description='Match score between user skills and event topics, on a scale of 0 to 100') # Please confirm data type we'll be using (int ot float)

class ResourceItem(BaseModel):
    title: str = Field(..., description='Title of the resource')
    description: str = Field(..., description='Brief description of the resource')
    resource_topic: str = Field(..., description='Topic that the resource covers')
    resource_level: str = Field(..., description='Proficiency level the resource is suitable for: beginner, intermediate, advanced')
    url: str = Field(..., description='URL of the resource')
    
class RecommendationInput(BaseModel):
    event_title: str = Field(..., description='Title of the event')
    event_level: str = Field(..., description='Proficiency level required for the event: beginner, intermediate, advanced')
    missing_topics: List[str] = Field(..., description='List of event topics that do not match the user skills')

class RecommendationOutput(BaseModel):
    briefing: str = Field(..., description='Briefing on the event topics')
    resources: List[ResourceItem] = Field(..., description='List of recommended resources to improve skills on the missing topics')  