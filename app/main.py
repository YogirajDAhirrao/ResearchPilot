from dotenv import load_dotenv
load_dotenv()

from .planner import planner
from .search import search




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

        results = search.invoke({
            "query": question.question
        })

        research_results.append({
            "question": question.question,
            "results": results,
        })

    print("\nResearch Plan")
    print("=" * 50)

    for i, question in enumerate(plan.questions, 1):
        print(f"{i}. {question.question}")


if __name__ == "__main__":
    main()