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


# JUDGE_PROMPT = """You are a strict evaluator of research briefs. Score 1 (poor) to 5 \
# (excellent) on two axes:

# - faithfulness: EVERY claim in the brief is supported by the FACT-CHECKED NOTES below. \
# Penalise any claim not grounded in the notes.
# - relevance: the brief directly and completely answers the QUESTION.

# Be critical; reserve 5 for briefs with no flaws on that axis.

# QUESTION:
# {question}

# FACT-CHECKED NOTES (the only allowed source of truth):
# {notes}

# BRIEF TO JUDGE:
# {brief}"""

JUDGE_PROMPT = """You are a strict evaluator of research briefs. Score the two axes \
INDEPENDENTLY, each 1-5. Do not let one axis influence the other.

faithfulness — are ALL claims in the brief supported by the FACT-CHECKED NOTES?
  5: every claim is grounded in the notes.
  3: mostly grounded, with one minor unsupported detail.
  1: contains a clearly fabricated or contradicted claim.
Judge ONLY grounding here.

relevance — does the brief ADDRESS THE QUESTION that was asked?
  5: directly and fully answers the question.
  3: partially answers it, or answers a narrower version.
  1: answers a different question or is off-topic.
Judge ONLY topical fit here. A brief can be fully relevant even if a claim is wrong — \
incorrectness is a FAITHFULNESS problem, never a relevance one.

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
