from src.graph.build import build_graph, route


def test_route_logic() -> None:
    assert route({"question": "q"}) == "researcher"
    assert route({"question": "q", "next": "verifier"}) == "verifier"
    assert route({"question": "q", "next": "writer"}) == "writer"
    assert route({"question": "q", "next": "FINISH"}) == "FINISH"


def test_graph_compiles() -> None:
    assert hasattr(build_graph(), "invoke")
