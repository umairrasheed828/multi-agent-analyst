from typing import Literal, cast

from pydantic import BaseModel, Field

from src.graph.state import AgentState
from src.llm import get_llm

Worker = Literal["researcher", "verifier", "writer", "FINISH"]


class Route(BaseModel):
    """The next worker to act, or FINISH when the brief is complete."""

    next: Worker = Field(description="Which worker acts next, or FINISH.")


SUPERVISOR_PROMPT = """You are the supervisor of a research team with three workers:
- researcher: gathers facts from the web (produces research_notes)
- verifier: fact-checks research_notes against fresh evidence (produces verified_notes)
- writer: composes the final brief from verified_notes (produces brief)

The required order is researcher -> verifier -> writer. Choose who acts next based on
what already exists. Once the brief exists, respond FINISH.

Produced so far:
- research_notes: {has_research}
- verified_notes: {has_verified}
- brief: {has_brief}"""


def supervisor_node(state: AgentState) -> dict[str, str]:
    """Router: decide which worker acts next based on current state."""
    llm = get_llm().with_structured_output(Route)
    decision = cast(
        Route,
        llm.invoke(
            SUPERVISOR_PROMPT.format(
                has_research=bool(state.get("research_notes")),
                has_verified=bool(state.get("verified_notes")),
                has_brief=bool(state.get("brief")),
            )
        ),
    )
    return {"next": decision.next}
