import json
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from .planner import planner
from .search import search
from .analyzer import analyzer
from .synthesizer import synthesizer

class ResearchState(TypedDict):
    topic: str
    questions: list[str]
    current_question_index: int
    research_results: list
    report: str


def plan_research(state:ResearchState):
    plan = planner.invoke({
        "topic":state["topic"]
    })

    questions = [question.question for question in plan.questions]

    return {
        "questions": questions,
        "current_question_index": 0,
        "research_results": [],
    }


def research_question(state:ResearchState):

    index = state["current_question_index"]
    question = state["questions"][index]

    print(f"\n[{index + 1}/{len(state['questions'])}] Researching:")
    print(f"    {question}\n")

    results = search.invoke({
        "query": question
    })

    analysis = analyzer.invoke({
        "question": question,
        "results": json.dumps(
            results,
            indent=2
        )
    })

    research_results = state["research_results"].copy()
    research_results.append({
        "question":question,
        "findings":analysis.findings
    })

    print(
        f"    ✓ Extracted {len(analysis.findings)} findings"
    )

    return {
        "research_results": research_results,
        "current_question_index":index+1
    }

def should_continue(state: ResearchState):

    if state["current_question_index"] < len(state["questions"]):
        return "research"

    return "synthesize"

def synthesize_report(state:ResearchState):

    findings = json.dumps(
        state["research_results"],
        indent=2,
        default=lambda obj: obj.model_dump()
    )

    report = synthesizer.invoke({
        "topic": state["topic"],
        "findings": findings,
    })

    return {
        "report": report.content
    }

builder = StateGraph(ResearchState)

builder.add_node(
    "planner",
    plan_research
)

builder.add_node(
    "research",
    research_question
)

builder.add_node(
    "synthesize",
    synthesize_report
)


builder.add_edge(
    START,
    "planner"
)

builder.add_edge(
    "planner",
    "research"
)

builder.add_conditional_edges("research",should_continue,{"research": "research","synthesize": "synthesize",})


builder.add_edge(
    "synthesize",
    END
)


research_graph = builder.compile()