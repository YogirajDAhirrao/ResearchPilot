from .models import Finding, Analysis
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)

structured_llm = llm.with_structured_output(Analysis)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research analyst.

            Analyze the provided search results and extract
            the most important factual findings relevant to
            the research question.

            Rules:
            - Only use information present in the search results.
            - Do not invent facts.
            - Prefer authoritative sources.
            - Each finding must have a supporting source URL.
            - Extract 2-5 important findings.
            """,
        ),
        (
            "human",
            """
            Research question:
            {question}

            Search results:
            {results}
            """,
        ),
    ]
)


analyzer = prompt | structured_llm