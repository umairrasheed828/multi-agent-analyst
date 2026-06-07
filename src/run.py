import sys

from src.graph.build import graph


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        print('Usage: uv run python -m src.run "your question here"')
        sys.exit(1)
    print(graph.invoke({"question": question})["brief"])


if __name__ == "__main__":
    main()
