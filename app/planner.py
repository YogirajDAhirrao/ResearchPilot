from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from .models import ResearchPlan

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)

structured_llm = llm.with_structured_output(ResearchPlan)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an expert research planner.

            Given a research topic, create a comprehensive
            research plan.

            Break the topic into 4-6 specific questions.

            Cover:
            - fundamentals
            - technical details
            - practical applications
            - important tradeoffs

            Each question should be independently researchable.
            """,
        ),
        (
            "human",
            "Research topic: {topic}",
        ),
    ]
)


planner = prompt | structured_llm