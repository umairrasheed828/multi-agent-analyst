from src.graph.state import AgentState
from src.llm import get_llm

WRITE_PROMPT = """You are a research writer. Using ONLY the fact-checked notes \
below, write a concise research brief (about 150 words) answering the question. \
Rely on [SUPPORTED] claims; mention [UNVERIFIED] points only with a clear caveat; \
ignore [CONTRADICTED] claims. End with a one-line 'Confidence:' note.

Question: {question}

Fact-checked notes:
{notes}

Research brief:"""


def writer_node(state: AgentState) -> dict[str, str]:
    """Specialist agent: compose the final brief from verified notes."""
    question = state["question"]
    notes = state["verified_notes"]
    llm = get_llm()
    brief = llm.invoke(WRITE_PROMPT.format(question=question, notes=notes)).content
    return {"brief": str(brief)}
