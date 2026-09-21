from pydantic import BaseModel, Field

class ResearchQuestion(BaseModel):
    question: str = Field(
        description="A specific question that should be researched"
    )

class ResearchPlan(BaseModel):
    questions: list[ResearchQuestion]
    
