from src.graph.state import AgentState
from src.llm import get_llm
from src.tools.search import web_search

RESEARCH_PROMPT = """You are a research assistant. Using ONLY the web search \
results below, extract the key facts relevant to the question as concise bullet \
points. If the results are insufficient to answer, say so explicitly.

Question: {question}

Search results:
{results}

Key facts (bullet points):"""


def researcher_node(state: AgentState) -> dict[str, str]:
    """Specialist agent: gather facts from the web for the question."""
    question = state["question"]
    results = web_search(question, max_results=5)
    llm = get_llm()
    notes = llm.invoke(
        RESEARCH_PROMPT.format(question=question, results=results)
    ).content
    return {"research_notes": str(notes)}
