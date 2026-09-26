from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from .graph import research_graph


def main():

    topic = input("Research topic: ")

    print("\nStarting research...\n")

    result = research_graph.invoke({
        "topic": topic,
        "questions": [],
        "current_question_index": 0,
        "research_results": [],
        "report": "",
    })

    report = result["report"]

    print("\n" + "=" * 80)
    print("RESEARCH REPORT")
    print("=" * 80)

    print(report)

    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = output_dir / f"research_{timestamp}.md"

    file_path.write_text(
        report,
        encoding="utf-8"
    )

    print(f"\nReport saved to: {file_path}")


if __name__ == "__main__":
    main()