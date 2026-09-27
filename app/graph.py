import json
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from .planner import planner
from .search import search
from .analyzer import analyzer
from .synthesizer import synthesizer
from .evaluator import evaluator

class ResearchState(TypedDict):
    topic: str
    questions: list[str]
    current_question_index: int
    research_results: list
    report: str
    research_sufficient:bool
    refined_query:str


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


def evaluate_research(state:ResearchState):
    # research_question() already incremented the index,
    # so the latest completed question is index - 1
    index = state["current_question_index"]-1
    question = state["questions"][index]

    latest_result = state["research_results"][-1]

    evaluation = evaluator.invoke({
        "question":question,
        "findings":json.dumps(latest_result,indent=2,default=lambda obj: obj.model_dump())
    })

    print("\n Research evaluation:")
    print(f"Sufficient: {evaluation.sufficient}")
    print(f"Reason: {evaluation.reason}")

    if not evaluation.sufficient:
        print(f"Improved query: {evaluation.improved_query}")

    return {
        "research_sufficient": evaluation.sufficient,
        "refined_query": evaluation.improved_query,
    }

def refine_research(state: ResearchState):

    query = state["refined_query"]

    index = state["current_question_index"] - 1

    question = state["questions"][index]

    print("\n    Research was insufficient.")
    print(f"    Refining search: {query}\n")

    results = search.invoke({
        "query": query
    })

    analysis = analyzer.invoke({
        "question": question,
        "results": json.dumps(
            results,
            indent=2
        )
    })

    research_results = state["research_results"].copy()

    research_results[-1] = {
        "question": question,
        "findings": analysis.findings
    }

    print(
        f"    ✓ Extracted {len(analysis.findings)} new findings"
    )

    return {
        "research_results": research_results
    }



def should_continue(state: ResearchState):

    if not state["research_sufficient"]:
        return "refine"
    if state["current_question_index"] < len(state["questions"]):
        return "research"
    return "synthesize"

builder = StateGraph(ResearchState)

builder.add_node("planner",plan_research)
builder.add_node("research",research_question)
builder.add_node("synthesize",synthesize_report)
builder.add_node("evaluate",evaluate_research)
builder.add_node("refine",refine_research)



builder.add_edge( START, "planner")
builder.add_edge("planner","research")
builder.add_edge("research","evaluate")


builder.add_conditional_edges(
    "evaluate",
    should_continue,
    {
        "research": "research",
        "refine": "refine",
        "synthesize": "synthesize",
    }
)
builder.add_edge(
    "refine",
    "evaluate"
)

builder.add_edge(
    "synthesize",
    END
)


research_graph = builder.compile()