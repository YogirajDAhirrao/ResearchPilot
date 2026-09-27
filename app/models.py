from pydantic import BaseModel, Field

class ResearchQuestion(BaseModel):
    question: str = Field(
        description="A specific question that should be researched"
    )

class ResearchPlan(BaseModel):
    questions: list[ResearchQuestion]

class Finding(BaseModel):
    claim:str = Field(
          description="An important factual finding relevant to the research question."
    ) 
    source_url: str = Field(
        description="URL of the source supporting the finding."
    )

class Analysis(BaseModel):
    findings:list[Finding]

class ResearchEvaluation(BaseModel):

    sufficient: bool = Field(
        description="Whether the current research sufficiently answers the question"
    )

    reason: str = Field(
        description="Explain why the research is or is not sufficient"
    )

    improved_query: str = Field(
        description="A better search query if the research is insufficient"
    )



