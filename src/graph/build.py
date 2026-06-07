from langgraph.graph import END, START, StateGraph

from src.agents.researcher import researcher_node
from src.agents.supervisor import supervisor_node
from src.agents.verifier import verifier_node
from src.agents.writer import writer_node
from src.graph.state import AgentState


def route(state: AgentState) -> str:
    """Send control to the worker the supervisor chose."""
    return state.get("next", "researcher")


def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("researcher", researcher_node)
    builder.add_node("verifier", verifier_node)
    builder.add_node("writer", writer_node)

    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        "supervisor",
        route,
        {
            "researcher": "researcher",
            "verifier": "verifier",
            "writer": "writer",
            "FINISH": END,
        },
    )
    builder.add_edge("researcher", "supervisor")
    builder.add_edge("verifier", "supervisor")
    builder.add_edge("writer", "supervisor")

    return builder.compile()


graph = build_graph()
