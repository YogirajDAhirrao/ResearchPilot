import json
from dotenv import load_dotenv
load_dotenv()

from .planner import planner
from .search import search
from .analyzer import analyzer
from .synthesizer import synthesizer




def main():
    topic = input("Research topic: ")

    print("\nPlanning research...\n")

    plan = planner.invoke({
        "topic": topic
    })

    research_results = []

    for i, question in enumerate(plan.questions, 1):

        print(f"[{i}/{len(plan.questions)}] Searching:")
        print(f"    {question.question}\n")
        # Search
        results = search.invoke({
            "query": question.question
        })
        # Analyze
        analysis = analyzer.invoke({
            "question": question.question,
            "results":json.dumps(
                results,
                indent=2
            )

        })

        research_results.append({
            "question":question.question,
            "findings":analysis.findings
        })

        print(
            f"    ✓ Extracted {len(analysis.findings)} findings\n"
        )

        

    print("\nResearch completed.")
    print("=" * 60)

    report = synthesizer.invoke({
        "topic":topic,
        "findings":json.dumps(
            research_results,
            indent=2,
            default=lambda obj:obj.model_dump()
        )
    })

    print("\n" + "=" * 80)
    print("RESEARCH REPORT")
    print("=" * 80)

    print(report.content)


if __name__ == "__main__":
    main()