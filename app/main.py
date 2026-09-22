import json
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
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

    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = output_dir/f"research_{timestamp}.md"

    file_path.write_text(report.content,encoding="utf-8")

    print(f"\nReport saved to: {file_path}")


if __name__ == "__main__":
    main()