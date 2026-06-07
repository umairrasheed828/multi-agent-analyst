# Multi-Agent Analyst

A multi-agent system that produces **fact-checked research briefs** — built to be *reliable and evaluable*, not merely functional. Given a question, a team of agents researches it, **independently verifies** the findings, and writes a concise brief that states its own confidence.

## Architecture

A LangGraph supervisor coordinates three specialist agents:

    question -> SUPERVISOR -> RESEARCHER  (web search)
                   |       -> VERIFIER    (independent fact-check)
                   |       -> WRITER      (brief + confidence)
                   v
               final brief

Each worker returns control to the supervisor, which re-decides the next step until the brief is complete — so every routing decision is a discrete, auditable step.

## Why it's built this way

- **Separation of concerns** — research, verification, and writing are distinct agents, each independently evaluable.
- **Independent verification** — the verifier runs its *own* web search instead of trusting the researcher, labelling each claim `[SUPPORTED] / [UNVERIFIED] / [CONTRADICTED]`.
- **Calibrated output** — every brief ends with an explicit confidence note.

## Evaluation

The system is evaluated on both the **process** (did it behave reliably?) and the **outcome** (is the brief good?) — and the quality judge itself is **calibrated** against human labels.

**Process — deterministic reliability checks** over an 8-question set (`eval/run_eval.py`). Every run is checked, with no LLM needed:

| check | pass rate |
|---|---|
| researched before verified | 8/8 |
| verified before wrote | 8/8 |
| brief includes a confidence note | 8/8 |
| research tool succeeded | 8/8 |

**Outcome — LLM-as-judge** scores each brief on faithfulness and relevance (1–5).

**Judge calibration** (`eval/calibrate.py`) — the judge is held to human-labelled cases that include deliberately flawed briefs. The initial judge conflated faithfulness errors with relevance; separating the axes in the rubric fixed it:

| axis | MAE before | MAE after | exact agreement |
|---|---|---|---|
| relevance | 1.00 | **0.20** | 40% → 80% |
| faithfulness | 0.40 | 0.40 | 60% |

Reproduce: `uv run python -m eval.run_eval` then `uv run python -m eval.calibrate`.


## Deployment

Containerized with Docker and deployed on AWS EC2. Every push to `main` runs the test suite, then auto-deploys over SSH via GitHub Actions. The API serves at port 8000 (`/docs` for the interactive Swagger UI). A live instance is run on demand and shared on request.

## Status

Complete: multi-agent graph (Phase 1), trajectory + calibrated evaluation (Phase 2), and a Dockerized FastAPI service auto-deployed to AWS via CI/CD (Phase 3).


## Quickstart

    uv sync
    echo "OPENAI_API_KEY=sk-..." > .env
    uv run python -m src.run "What is retrieval-augmented generation?"

## Tech

Python 3.12 · LangGraph · LangChain · OpenAI gpt-4o-mini · DuckDuckGo search. Quality gates: ruff, mypy, pytest, GitHub Actions CI.
