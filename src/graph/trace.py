from dataclasses import dataclass

from src.graph.build import graph


@dataclass
class TrajectoryStep:
    """One step in a run: which node fired and which state keys it wrote."""

    node: str
    produced: list[str]


def run_with_trajectory(question: str) -> tuple[dict, list[TrajectoryStep]]:
    """Run the graph and record the ordered trajectory of steps.

    Returns the final state and the list of steps, so you can evaluate both
    the outcome (the brief) and the process (the path taken to produce it).
    """
    state: dict = {"question": question}
    trajectory: list[TrajectoryStep] = []
    for chunk in graph.stream({"question": question}, stream_mode="updates"):
        for node, update in chunk.items():
            produced = list(update.keys()) if update else []
            trajectory.append(TrajectoryStep(node=node, produced=produced))
            if update:
                state.update(update)
    return state, trajectory
