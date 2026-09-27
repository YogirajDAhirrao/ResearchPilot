from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from .models import ResearchEvaluation

llm = ChatGroq(model="openai/gpt-oss-120b",temperature=0)
structured_llm = llm.with_structured_output(ResearchEvaluation)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a research quality evaluator.

Evaluate whether the provided research findings sufficiently answer
the research question.

If the findings are sufficient:
- Set sufficient=true.
- Explain why.
- improved_query can be an empty string.

If the findings are insufficient:
- Set sufficient=false.
- Explain what information is missing.
- Generate a better search query that could find the missing information.
"""
    ),
    (
        "human",
        """
Research Question:
{question}

Current Findings:
{findings}
"""
    )
])

evaluator = prompt | structured_llm







