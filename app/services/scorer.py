from app.models import MatchScoreInput, MatchScoreOutput

def calculate_match_score(data: MatchScoreInput) -> MatchScoreOutput:
    # Define weights for each skill level
    level_weights = {
        "beginner": 0.5,
        "intermediate": 1.0,
        "advanced": 1.5
    }

    # Normalize skills and topics to lowercase for case-insensitive matching
    user_skills_lower = [skills.lower() for skills in data.user_skills]
    user_topics_lower = [topics.lower() for topics in data.event_topics]
    user_skill_levels_lower = {
        k.lower(): v.lower() 
        for k, v in data.user_skill_levels.items()
    }

    # Identify matched and missing topics
    match_topics = [topic for topic in user_topics_lower if topic in user_skills_lower]
    missing_topics = [topic for topic in user_topics_lower if topic not in user_skills_lower]
    
    # Calculate weighted match score based on skill levels
    weighted_match_score = 0
    for topic in match_topics:

        skill_level = user_skill_levels_lower.get(topic, "beginner")
        weight = level_weights.get(skill_level)
        weighted_match_score += weight
      
    # Calculate the maximum possible score based on the number of event topics and the highest skill level weight
    max_possible_score = len(data.event_topics) * max(level_weights.values())

    if max_possible_score > 0:
        final_match_score = int((weighted_match_score / max_possible_score) * 100)
    else:
        final_match_score = 0

    return MatchScoreOutput(
        match_score=final_match_score,
        match_topics=match_topics,
        missing_topics=missing_topics
    )






