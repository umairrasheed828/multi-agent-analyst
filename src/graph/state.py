from typing import TypedDict


class AgentState(TypedDict, total=False):
    question: str
    research_notes: str
    verified_notes: str
    brief: str
    next: str
