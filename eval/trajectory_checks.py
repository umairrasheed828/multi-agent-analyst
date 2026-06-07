from src.graph.trace import TrajectoryStep

FAILURE_MARKERS = ("[search failed", "[no results found]")


def first_index(trajectory: list[TrajectoryStep], node: str) -> int:
    """Index of the first time `node` ran, or -1 if it never ran."""
    for i, step in enumerate(trajectory):
        if step.node == node:
            return i
    return -1


def check_trajectory(state: dict, trajectory: list[TrajectoryStep]) -> dict[str, bool]:
    """Deterministic reliability checks on a single run (no LLM needed)."""
    r = first_index(trajectory, "researcher")
    v = first_index(trajectory, "verifier")
    w = first_index(trajectory, "writer")

    return {
        "researcher_ran": r != -1,
        "verifier_ran": v != -1,
        "writer_ran": w != -1,
        "researched_before_verified": r != -1 and v != -1 and r < v,
        "verified_before_wrote": v != -1 and w != -1 and v < w,
        "brief_present": bool(state.get("brief")),
        "brief_has_confidence": "confidence" in str(state.get("brief", "")).lower(),
        "research_succeeded": not any(
            m in str(state.get("research_notes", "")) for m in FAILURE_MARKERS
        ),
    }
