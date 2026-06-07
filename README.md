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

## Quickstart

    uv sync
    echo "OPENAI_API_KEY=sk-..." > .env
    uv run python -m src.run "What is retrieval-augmented generation?"

## Tech

Python 3.12 · LangGraph · LangChain · OpenAI gpt-4o-mini · DuckDuckGo search. Quality gates: ruff, mypy, pytest, GitHub Actions CI.

## Status

Phase 1 (multi-agent graph) complete. Phase 2 (trajectory & reliability evaluation) in progress.