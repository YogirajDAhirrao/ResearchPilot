from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an expert technical research writer.

            Write a comprehensive research report based ONLY
            on the provided research findings.

            Requirements:

            - Use Markdown.
            - Create a logical structure with headings.
            - Explain technical concepts clearly.
            - Combine related findings instead of repeating them.
            - Preserve important technical details.
            - Mention conflicting information when present.
            - Do not invent information.
            - Include a Sources section.
            - Every important factual claim should be traceable
              to one of the provided sources.
            """,
        ),
        (
            "human",
            """
            Research topic:
            {topic}

            Research findings:
            {findings}

            Write the final research report.
            """,
        ),
    ]
)


synthesizer = prompt | llm