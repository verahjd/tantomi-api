from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.models import ChatInput, ChatOutput
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an assistant that helps users reflect on what they learned at tech events.

You will be given:
- The event title and topics covered
- The user's raw reflection or answers to guided questions

Your job is to produce TWO things:

1. A summary of what the user learned, written in second person ("You explored...", "You learned that..."). Make it personal and specific to what they actually wrote, not generic. Reference concrete things they mentioned.

2. A list of skills they demonstrated learning, each with a proficiency level.

For the skills list:
- Only include skills the user explicitly described engaging with or learning about. Don't invent skills they didn't mention.
- Skills should be concrete (e.g., "React Hooks", "Docker", "SQL") not vague (e.g., "Programming", "Technology").
- Assign levels based on how the user describes their understanding:
  * beginner: they describe learning what something IS, basic concepts, first exposure ("I learned what hooks are")
  * intermediate: they describe USING or APPLYING the concept, building something, connecting ideas ("I built a small app using hooks")
  * advanced: they describe optimizing, comparing approaches, deep technical insight, or extending existing expertise ("I refactored our hook patterns to reduce re-renders")

If the user's reflection is very brief or vague, default to beginner.
If the user mentions a skill from the event topics list explicitly, include it.
If they mention skills NOT in the event topics, still include those — they may have made connections beyond the event scope."""),
    ("human", """Event: {event_title}
Topics covered: {event_topics}

User's reflection:
{user_input}

Generate the summary and skills extracted.""")
])

def generate_chat_response(data: ChatInput) -> ChatOutput:
    chain = prompt | model.with_structured_output(ChatOutput, method="function_calling")
    result = chain.invoke({
        "event_title": data.event_title,
        "event_topics": ", ".join(data.event_topics),
        "user_input": data.user_input,
    })
    return result