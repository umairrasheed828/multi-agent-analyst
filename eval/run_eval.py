import json
from collections import defaultdict
from pathlib import Path

from eval.judge import judge_brief
from src.graph.checks import check_trajectory
from src.graph.trace import run_with_trajectory

QUESTIONS_FILE = Path("eval/eval_questions.jsonl")
RESULTS_FILE = Path("eval/results.jsonl")


def load_questions() -> list[dict]:
    lines = QUESTIONS_FILE.read_text().splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def main() -> None:
    questions = load_questions()
    n = len(questions)
    totals: dict[str, int] = defaultdict(int)
    score_sums = {"faithfulness": 0, "relevance": 0}

    with RESULTS_FILE.open("w") as out:
        for item in questions:
            qid, question = item["id"], item["question"]
            print(f"Running {qid}: {question}")
            state, trajectory = run_with_trajectory(question)
            checks = check_trajectory(state, trajectory)
            for name, passed in checks.items():
                totals[name] += int(passed)

            judgment = judge_brief(
                question,
                str(state.get("verified_notes", "")),
                str(state.get("brief", "")),
            )
            score_sums["faithfulness"] += judgment.faithfulness
            score_sums["relevance"] += judgment.relevance

            out.write(
                json.dumps(
                    {
                        "id": qid,
                        "question": question,
                        "path": [s.node for s in trajectory],
                        "checks": checks,
                        "faithfulness": judgment.faithfulness,
                        "relevance": judgment.relevance,
                        "rationale": judgment.rationale,
                        "brief": state.get("brief", ""),
                    }
                )
                + "\n"
            )

    print(f"\nReliability over {n} questions:")
    for name, count in totals.items():
        print(f"  {name}: {count}/{n}  ({100 * count / n:.0f}%)")
    print("\nQuality (LLM judge, 1-5):")
    print(f"  faithfulness: {score_sums['faithfulness'] / n:.2f}")
    print(f"  relevance:    {score_sums['relevance'] / n:.2f}")


if __name__ == "__main__":
    main()
