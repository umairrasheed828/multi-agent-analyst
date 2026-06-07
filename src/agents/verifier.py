from src.graph.state import AgentState
from src.llm import get_llm
from src.tools.search import web_search

VERIFY_PROMPT = """You are a fact-checker. You are given research notes and \
independent evidence from a fresh web search. For each claim in the notes, decide \
whether the evidence supports it. Rewrite the notes so each bullet is prefixed with:
[SUPPORTED]    - corroborated by the evidence
[UNVERIFIED]   - plausible but not confirmed by the evidence
[CONTRADICTED] - the evidence disagrees
Drop any claim that appears fabricated or off-topic.

Question: {question}

Research notes:
{notes}

Independent evidence:
{evidence}

Fact-checked notes:"""


def verifier_node(state: AgentState) -> dict[str, str]:
    """Specialist agent: cross-check research notes against fresh evidence."""
    question = state["question"]
    notes = state["research_notes"]
    evidence = web_search(question, max_results=5)
    llm = get_llm()
    checked = llm.invoke(
        VERIFY_PROMPT.format(question=question, notes=notes, evidence=evidence)
    ).content
    return {"verified_notes": str(checked)}
