from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.graph.checks import check_trajectory
from src.graph.trace import run_with_trajectory

app = FastAPI(title="Multi-Agent Analyst")


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    brief: str
    path: list[str]
    checks: dict[str, bool]
    context: str = ""  # NEW: the verified_notes the writer used (faithfulness source)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="question must not be empty")
    state, trajectory = run_with_trajectory(question)
    return AskResponse(
        brief=str(state.get("brief", "")),
        path=[s.node for s in trajectory],
        checks=check_trajectory(state, trajectory),
        context=str(state.get("verified_notes", "")),  # NEW
    )
