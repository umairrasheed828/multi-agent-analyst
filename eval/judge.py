from typing import cast

from pydantic import BaseModel, Field

from src.llm import get_llm


class Judgment(BaseModel):
    """LLM-as-judge scores for a research brief (1-5 scale)."""

    faithfulness: int = Field(
        ge=1, le=5, description="Is every claim supported by the notes?"
    )
    relevance: int = Field(
        ge=1, le=5, description="Does the brief answer the question?"
    )
    rationale: str = Field(description="One or two sentences explaining the scores.")


JUDGE_PROMPT = """You are a strict evaluator of research briefs. Score 1 (poor) to 5 \
(excellent) on two axes:

- faithfulness: EVERY claim in the brief is supported by the FACT-CHECKED NOTES below. \
Penalise any claim not grounded in the notes.
- relevance: the brief directly and completely answers the QUESTION.

Be critical; reserve 5 for briefs with no flaws on that axis.

QUESTION:
{question}

FACT-CHECKED NOTES (the only allowed source of truth):
{notes}

BRIEF TO JUDGE:
{brief}"""


def judge_brief(question: str, notes: str, brief: str) -> Judgment:
    llm = get_llm().with_structured_output(Judgment)
    return cast(
        Judgment,
        llm.invoke(JUDGE_PROMPT.format(question=question, notes=notes, brief=brief)),
    )
