import json
from pathlib import Path

from eval.judge import judge_brief

CALIB_FILE = Path("eval/calibration_set.jsonl")


def load_cases() -> list[dict]:
    lines = CALIB_FILE.read_text().splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def main() -> None:
    cases = load_cases()
    n = len(cases)
    abs_err = {"faithfulness": 0.0, "relevance": 0.0}
    exact = {"faithfulness": 0, "relevance": 0}
    disagreements = []

    for c in cases:
        j = judge_brief(c["question"], c["notes"], c["brief"])
        for axis, judged in (
            ("faithfulness", j.faithfulness),
            ("relevance", j.relevance),
        ):
            human = c[f"human_{axis}"]
            err = abs(judged - human)
            abs_err[axis] += err
            if err == 0:
                exact[axis] += 1
            if err >= 2:
                disagreements.append(
                    f"  {c['id']} {axis}: judge={judged} human={human}  ({c['question']})"
                )

    print(f"Calibration over {n} labeled cases:")
    for axis in ("faithfulness", "relevance"):
        print(
            f"  {axis}: MAE={abs_err[axis] / n:.2f}  "
            f"exact={exact[axis]}/{n} ({100 * exact[axis] / n:.0f}%)"
        )
    print("\nBiggest disagreements (|judge - human| >= 2):")
    print("\n".join(disagreements) if disagreements else "  none")


if __name__ == "__main__":
    main()
