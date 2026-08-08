# F1 AI Engineering Portfolio – Project Plan

(with open-source embedding integration)

## How to use this document

This document contains everything you need to build three production-grade AI engineering projects for your GitHub portfolio. It is written so you can copy each project's section into a fresh chat with another Claude instance and use it as the project kickoff brief.

All three projects share the Formula 1 domain. This is deliberate — a thematically coherent portfolio is more memorable than three random projects, and the elevator pitch becomes simple: "end-to-end AI engineering applied to F1 data". The three projects deliberately tackle three different categories of AI work, so the coherent domain doesn't mean repeating the same skills.

There are four sections:

- Section 1 — Universal standards: things every project must do, regardless of which one you're working on. Read this once.
- Section 2 — Project 1 brief: F1 Regulations RAG with Evaluation Harness.
- Section 3 — Project 2 brief: F1 Race Strategy Multi-Agent System.
- Section 4 — Project 3 brief: F1 Telemetry Anomaly Detection Service.

**Recommended workflow:** Start a new chat for each project. At the top, paste the relevant section plus the universal standards. Tell the assistant: *"I'm building this project. Help me scaffold the repo, then we'll work through it section by section."* Treat each project chat as a long-running pair-programming session.

### Suggested timing

| Project | Timing | Hours |
|---|---|---|
| Project 1 (RAG) | weeks 1–2 | ~25–30 hours total |
| Project 2 (Multi-Agent) | weeks 3–4 | ~25–30 hours total |
| Project 3 (Telemetry service) | weeks 5–6 | ~20–25 hours total |

Realistic expectation: with a job search running in parallel, expect 8–10 weeks for the first project and 6–7 weeks each for the next two. That is fine. Start anyway.

If life happens and you're tight on time: drop Project 2 first, then Project 3. One genuinely finished project always beats three half-built ones, and Project 1 (RAG) is the single most-asked-for skill on AI Engineer job descriptions.

### What 'done' looks like for each project

A project is not finished when the code runs. It is finished when all of the following are true:

- Public GitHub repo with clean commit history (no 'fix typo' chains, no 'wip' commits to main).
- README that an interviewer can read in under 5 minutes and understand: what it does, why you built it, the architecture, the evaluation results, the limitations.
- Architecture diagram in the README (use Mermaid or excalidraw, included as PNG).
- Dockerfile that actually works (test it on a fresh machine).
- GitHub Actions CI that runs lint + tests on every push.
- At least 60% test coverage on the core logic (not the API endpoints — the actual logic).
- A 'Limitations and what I'd do differently' section in the README. This is non-negotiable; it is the single highest-signal part of any portfolio project.
- Either a deployed live demo (HF Spaces / Railway) or a 60-second screen recording embedded in the README.

---

# Section 1 — Universal standards

These rules apply to all three projects. Paste this section into the top of any new project chat alongside the project-specific brief.

## 1.1 Repository structure

Every project follows the same skeleton. This is the standard 'Python application' layout — recruiters and engineers recognise it instantly.

```text
project-name/
├── .github/
│   └── workflows/
│       └── ci.yml              # lint + test on push
├── src/
│   └── project_name/           # your package
│       ├── __init__.py
│       ├── core/               # main logic
│       ├── api/                # FastAPI routes
│       ├── models/             # Pydantic schemas
│       └── config.py           # settings via pydantic-settings
├── tests/
│   ├── unit/
│   └── integration/
├── data/                       # gitignored (raw inputs)
├── notebooks/                  # exploration only, NOT the project
├── docs/
│   ├── architecture.png
│   └── evaluation_results.md
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml          # if you need redis/postgres
├── pyproject.toml              # use this, NOT requirements.txt
├── README.md
└── LICENSE                     # MIT
```

## 1.2 Tooling — non-negotiable

- Python 3.12 — newer than 3.10 because employers want to see modern type hints.
- `uv` for dependency management. It's faster than pip, recruiters notice, and it makes your CI faster.
- `ruff` for linting and formatting (replaces black + flake8 + isort).
- `pytest` for tests, with `pytest-cov` for coverage reporting.
- `pydantic` v2 for all data validation. Always. No exceptions.
- `pydantic-settings` for config — never read `os.environ` directly in your code.
- `loguru` for logging. Cleaner than the stdlib logger, and it shows you've thought about logs.

## 1.3 README structure

Every project README follows this exact structure. Recruiters skim — make it scannable.

```text
# Project Name
One-line description that says what the project does and the headline result.
[![CI](badge)](link) [![Python 3.12](badge)](link) [![License](badge)](link)

## Demo
Live demo link OR embedded GIF (15-30 seconds, shows the happy path)

## What this is
2-3 paragraphs. Lead with the problem, then the approach.

## Architecture
Diagram (PNG/SVG). Then 3-5 sentences explaining the data flow.

## Key technical decisions
3-5 bullets, each one a non-obvious choice with the reasoning.
This is the section interviewers actually read.

## Evaluation results
Table with numbers. Without this, the project doesn't count.

## Running locally
```bash
git clone ...
cp .env.example .env  # add your OpenAI key
docker compose up
```

## Project structure
Tree view of the repo, briefly annotated.

## Limitations and what I'd do differently
This is the most important section. Be honest. Examples:

- The eval set is small (50 questions); I'd expand to 500 with a labelling effort.
- Hybrid retrieval works but reranking adds 200ms p95; for production I'd cache.
- Single-language only.

## License
MIT.
```

**Critical:** The 'Limitations and what I'd do differently' section is the highest-signal part of your README. Engineers who can honestly assess their own work get hired; engineers who oversell get filtered out in interviews. Be specific and technical, not vague.

## 1.4 Commit hygiene

- Use conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`.
- Push small, focused commits. A reviewer should understand each one in 30 seconds.
- No commits called 'wip', 'fix', 'updates', 'changes'. These signal a junior developer.
- Squash messy branches before merging to main.
- First commit should be the project skeleton, not a half-built feature.

## 1.5 Secrets and API keys

- Never commit API keys. Ever. Even once.
- Use `.env` for local development; commit `.env.example` with placeholder values.
- Add `.env` to `.gitignore` before your first commit. Do this immediately.
- If you accidentally commit a key, rotate it immediately and use `git-filter-repo` to clean history. Don't just delete in a follow-up commit — the key is still in history.

## 1.6 Cost discipline

OpenAI / Anthropic API calls are cheap per call but easy to burn through during development. Set a hard budget.

- Set a usage limit in your OpenAI account dashboard (£20-30 max for development).
- Cache aggressively. For RAG eval, you should never re-embed documents you've already embedded.
- Use `gpt-4o-mini` or `gpt-4.1-mini` for development; only use larger models when you need them. They are 10-30x cheaper and good enough for most tasks.
- Use `text-embedding-3-small` for embeddings. It's the cheapest OpenAI embedding model and performs well.

## 1.7 Evaluation philosophy

The single most important thing separating you from other candidates is that you **measure what you build**.

For every project, before you write feature code, write the evaluation harness. Even a primitive one. This forces you to define 'good' before you optimise toward something undefined.

- Hand-curate 30-50 test cases. Don't auto-generate them with an LLM at first — you need to know what 'right' looks like.
- Run evaluation on every meaningful change. Commit results.
- Track results over time. A simple `docs/evaluation_results.md` with a dated table is enough.
- Be honest about regression. If a change made things worse on some metric, write that in the README.

## 1.8 What to NOT do

- Don't build in Jupyter notebooks. Notebooks are for exploration only. The deliverable is a Python package.
- Don't skip tests because 'it's just a portfolio project'. Recruiters check for tests. The absence is louder than presence.
- Don't use LangChain for everything by default. Use it where the orchestration is genuinely complex; use raw SDK calls where it's simple. Interviewers will ask why you chose what you chose.
- Don't deploy without thinking about cost. Hugging Face Spaces free tier is fine for demos but it sleeps; mention this in the README.
- Don't claim functionality that isn't there. If the agent self-critique 'works in 70% of cases', say that — don't claim it 'works'.
- Don't forget the LICENSE file. MIT is fine. Repos without licenses look unfinished.

## 1.9 Observability is a first-class deliverable

Every project must have LLM observability wired in from the start, not bolted on at the end. This is something the market increasingly asks for and almost no candidate portfolio shows.

- Projects 1 and 2 use **Langfuse** (free tier, hosted). Wrap every LLM call. Screenshots of traces go in the README.
- Project 3 uses **Prometheus + Grafana** for service-level metrics. Screenshot of the dashboard goes in the README.
- Track at minimum: token usage per request, p50/p95/p99 latency, error rates, cost per request.
- If you can't show observability screenshots in your README, you have not finished the project.

---

# Section 2 — Project 1: F1 Regulations RAG

## 2.1 The pitch

A retrieval-augmented Q&A system over the FIA Formula 1 Sporting Regulations, Technical Regulations, and a corpus of stewards' decisions. Built with hybrid retrieval, three chunking strategies compared, and a reproducible evaluation harness using RAGAS.

**Why this project, and why this domain**

Every AI Engineer job posting mentions RAG. Most candidate RAG projects fail because they have no evaluation. This project leads with evaluation.

The FIA F1 regulations are an unusually good corpus for RAG: they are dense, hierarchically structured, full of cross-references, contain tables, and use specific article numbers that users genuinely query ("Article 33.4"). This means the corpus naturally tests every interesting RAG problem. A generic 'RAG over a Wikipedia article' project tests none of them.

## 2.2 Stack

- **Language:** Python 3.12
- **Orchestration:** LangChain (LCEL) for the chain composition
- **Embeddings:** Pluggable embedding provider supporting **OpenAI `text-embedding-3-small`** and **local `BAAI/bge-small-en-v1.5`** (via `sentence-transformers`). See Phase B for details.
- **Vector store:** pgvector (PostgreSQL extension) — runs in Docker
- **Sparse retrieval:** BM25 via `rank-bm25`
- **Reranker:** `cohere-rerank` or `BAAI/bge-reranker-base` if you want to keep it free
- **LLM:** `gpt-4o-mini` for answer generation (cost discipline)
- **Evaluation:** RAGAS
- **Observability:** Langfuse (free tier)
- **API:** FastAPI
- **Container:** Docker Compose (app + postgres+pgvector)

## 2.3 Data sources — exact URLs

Use these. They are public, official, and free.

- FIA F1 Sporting Regulations: fia.com → Documents → Sporting Regulations → 2025/2026 (PDF)
- FIA F1 Technical Regulations: same path → Technical Regulations
- FIA F1 Financial Regulations: same path → Financial Regulations
- Stewards' decisions: fia.com/documents — filter by F1, year. Download 30-50 decisions across recent seasons. They are short PDFs (1-3 pages) — perfect for testing edge cases.

**Tip:** Build a small Python script that downloads and stores the PDFs once, locally, into `data/raw/`. Don't re-fetch on every ingestion run. Document the exact versions you used in the README — the FIA updates these regulations annually.

## 2.4 Build sequence

Build in this order. Do not skip ahead. Each step depends on the previous one being solid.

### Phase A — Skeleton (day 1, 2-3 hours)

- Create the GitHub repo. Public. MIT license. README with the title and one-paragraph description.
- Set up `pyproject.toml` with `uv`. Pin Python 3.12.
- Add `ruff` config, pre-commit hooks, `.env.example`, `.gitignore`.
- Add the GitHub Actions CI workflow (lint + test). It will run on an empty test, that's fine for now.
- Add `docker-compose.yml` with postgres+pgvector service. Verify it starts.
- Commit. Push. Confirm CI passes.

### Phase B — Ingestion (days 2-3, ~5 hours)

- Write `src/f1_rag/ingestion/loaders.py` — load PDFs using `pypdf` or `pdfplumber` (pdfplumber handles tables better; this matters for technical regs).
- Write `src/f1_rag/ingestion/chunkers.py` with three strategies:
  - `FixedSizeChunker` (e.g. 500 tokens, 50 overlap)
  - `SemanticChunker` (use LangChain's SemanticChunker)
  - `HierarchicalChunker` — custom, splits on regulation article boundaries ("Article 1.2", "Article 33.4"). This will be your best-performing one and the story you tell in interviews.
- Write `src/f1_rag/ingestion/embedder.py` — **pluggable embedding provider**:
  - Define a `BaseEmbeddingProvider` interface with a single `embed(texts: list[str]) -> list[list[float]]` method.
  - Implement `OpenAIEmbeddingProvider` (wraps `text-embedding-3-small`).
  - Implement `LocalBGEProvider` (loads `BAAI/bge-small-en-v1.5` via `sentence-transformers`, no API key needed).
  - Add disk caching to both providers so you never re-embed the same document.
  - The provider is selected via an environment variable (`EMBEDDING_PROVIDER=openai` or `local`).
- Write `src/f1_rag/ingestion/store.py` — pgvector insertion, with metadata fields: `source_doc`, `article_number`, `page_number`, `chunking_strategy`.
- Write the ingest CLI command: `python -m f1_rag.cli ingest --strategy hierarchical --embedding-provider local`.

**Why local embeddings?** This addition directly addresses a common UK job spec requirement: experience with open-source models. It lets you discuss model trade-offs (cost, latency, privacy), run the evaluation harness with both providers, and prove you're not dependent on a single API.

### Phase C — Retrieval (days 4-5, ~5 hours)

- Write `src/f1_rag/retrieval/dense.py` — pgvector similarity search.
- Write `src/f1_rag/retrieval/sparse.py` — BM25 over the same chunks.
- Write `src/f1_rag/retrieval/hybrid.py` — combines dense + sparse with reciprocal rank fusion (RRF). RRF is simpler and more robust than weighted score fusion; use it.
- Add a reranker stage that takes the top 20 hybrid results and reranks to top 5.
- Write `src/f1_rag/retrieval/router.py` — picks retrieval strategy. If the query contains a regex match for an article number (e.g. "Article 33.4"), prefer BM25; otherwise hybrid.

*Why this matters: The article-number routing is the single best interview story this project gives you. "Why hybrid?" → "Because users query specific article numbers like '33.4' and pure embeddings handle those poorly. I added a router that detects article references and prefers BM25 for those cases." That's a senior-thinking answer.*

### Phase D — Generation chain (day 6, ~3 hours)

- Write the LangChain LCEL chain: retrieve → format_context → prompt → llm → parse.
- Use a careful system prompt: instruct the LLM to cite article numbers, refuse to answer if context is insufficient, never speculate.
- Pydantic output schema: `answer`, `citations` (list of article numbers), `confidence` (low/medium/high), `insufficient_context` (bool).
- Wire Langfuse tracing.

### Phase E — Evaluation harness (days 7-8, ~6 hours — the most important phase)

This is what makes the project hireable rather than ordinary. Take it seriously.

- Hand-curate 40-50 test questions. Mix of types:
  - Simple lookups: "What is the maximum fuel flow rate?"
  - Article-specific: "What does Article 33.4 say about overtaking?"
  - Multi-hop: "Compare the 2024 and 2025 wing dimension regs" (will fail; that's interesting to discuss)
  - Edge cases: "What's the penalty for a yellow flag infringement?" (depends on stewards' discretion — answer should reflect uncertainty)
  - Off-topic: "What's the weather in Monaco?" (must refuse)
- For each, write the expected answer and the expected source article(s).
- Store as `evals/test_set.yaml`.
- Wire RAGAS metrics: faithfulness, answer_relevancy, context_precision, context_recall.
- **Run the harness against all three chunking strategies. Additionally, run the best chunking strategy with both the OpenAI and the local embedding provider.** Save results to `docs/evaluation_results.md` as a dated table.
- Run a small ablation: hybrid vs dense-only vs sparse-only retrieval. Document.
- The resulting table should show the impact of embedding choice, giving you another data-driven story for interviews.

### Phase F — API and packaging (day 9, ~3 hours)

- FastAPI app with `/query` endpoint and `/health`.
- Pydantic request/response models.
- Rate limiting via `slowapi`.
- Dockerfile (multi-stage, slim final image).
- Docker Compose with API + postgres+pgvector + a one-shot ingestion service.
- Test the full path on a fresh machine: `git clone → docker compose up → curl /query`.

### Phase G — Polish (day 10, ~3 hours)

- Architecture diagram (excalidraw or Mermaid). Save as PNG in `docs/`.
- Write the README using the standard structure. Include the eval results table (with embedding provider comparison).
- Record a 60-second demo: terminal showing curl request, API response with citations, dashboard showing Langfuse trace.
- Deploy on Hugging Face Spaces or Railway free tier (mention sleep behaviour in README).

## 2.5 Things to remember during the build

- PDF parsing is harder than it looks. Tables and multi-column layouts break naive parsers. Test `pdfplumber` on a hard page early.
- FIA regulation PDFs use page headers and footers — strip them before chunking or they pollute every chunk.
- Article cross-references break flat retrieval. If chunk A says 'see Article 33.4' and the user query needs both, you have a multi-hop retrieval problem. Document this as a limitation; don't try to solve it.
- Don't chase eval numbers obsessively. Get to a defensible baseline (faithfulness > 0.85, context precision > 0.7), then stop.
- The hierarchical chunker is what makes this project distinctive. Spend extra time on it. Use the regulation's natural structure ("Article X.Y.Z") as the splitting boundary.
- **Local embedding model**: The `bge-small-en-v1.5` model is ~130MB, runs entirely locally, and produces 384-dim vectors. It's about 10× cheaper than API calls but slightly lower quality — your evaluation will quantify the exact gap. Discuss this trade-off in your README's "Key technical decisions" section.

## 2.6 Interview answers this project unlocks

- "Walk me through your RAG architecture." — concrete answer with diagram
- "How did you choose chunk size?" — "I evaluated three strategies on 45 hand-curated questions; hierarchical chunking gave 14% higher context precision."
- "How do you evaluate RAG?" — RAGAS metrics with numbers
- "What were the failure modes?" — multi-hop queries, regulation cross-references, ambiguous stewards' decisions
- "Why hybrid retrieval?" — article-number routing story
- "Have you used a vector DB?" — pgvector, with operational experience
- **"Have you used open-source embeddings? How do they compare to OpenAI?"** — now you have real numbers from the eval harness. "BGE-small achieved 0.79 context precision vs 0.83 for OpenAI, but costs nothing and runs without network dependency. For a regulated environment or an offline document store, it's a strong candidate."

## 2.7 README headline (write this last but plan for it)

> **F1 Regulations RAG** — A retrieval-augmented Q&A system over the FIA F1 Sporting and Technical Regulations. Built with hybrid retrieval (dense + BM25 + reranking), three chunking strategies benchmarked, and a 45-question evaluation harness using RAGAS. Hierarchical chunking achieved 0.91 faithfulness and 0.83 context precision on the eval set. Pluggable embeddings compared OpenAI `text-embedding-3-small` and local `BAAI/bge-small-en-v1.5`.

---

# Section 3 — Project 2: F1 Race Strategy Multi-Agent System

## 3.1 The pitch

A LangGraph multi-agent system where four specialised agents — Tyre Strategist, Weather Analyst, Gap Analyst, and Pit Window Calculator — collaborate via shared state to produce structured race strategy recommendations. The system takes a snapshot of mid-race state (lap N, tyre ages per driver, gaps to leader, weather forecast, current track conditions) and produces a strategy report with recommended actions, confidence levels, supporting reasoning, and a self-critique pass that can trigger one revision cycle.

**Why this project, and why this domain**

Agentic AI is the highest-paying and fastest-growing segment of the AI Engineer market in 2026. LangGraph specifically appears in roughly a quarter of agentic AI listings, and most candidate "agent" projects are single-agent ReAct loops dressed up as something more sophisticated. A genuine multi-agent system with explicit state management, structured collaboration, and self-critique is rare in the candidate pool.

The F1 race strategy domain works because race strategy is genuinely a multi-agent problem in real Formula 1. Different specialists actually do focus on different sub-problems and feed information to a strategy lead. You're not forcing the multi-agent pattern onto a domain that doesn't need it; you're modelling something that works that way in real life. That authenticity shows up in how thoughtful the agent decomposition is, and it gives you a genuine story in interviews: "In a real F1 team, this is how strategists actually work — I modelled it directly."

This project also shares its data source (FastF1) with Project 3, which means the F1 portfolio thread is reinforced and your data-loading code can be shared between the two projects.

## 3.2 Stack

- **Language:** Python 3.12
- **Agent framework:** LangGraph — not LangChain agents. LangGraph's graph state model is what you want.
- **LLM:** `gpt-4o` for the synthesiser and critic; `gpt-4o-mini` for individual specialist agents (cost optimisation).
- **Structured output:** Pydantic v2 + OpenAI's JSON mode at every node
- **Data:** `fastf1` library for historical race state (free, official-derived). Same library as Project 3 — reuse the loader code if useful.
- **Observability:** Langfuse
- **UI:** Streamlit (interviewers like clickable demos for agents, and Streamlit's status components are visually impressive when nodes execute live)
- **Evaluation:** LLM-as-judge with a hand-written rubric, plus human spot-checking
- **Container:** Docker

## 3.3 Data sources

- **FastF1:** docs.fastf1.dev — free Python library that gives you lap timing, telemetry, weather, tyre stints, gaps, and position changes from real F1 sessions.

You are not running this in real time. You take a snapshot of mid-race state at, say, lap 25 of Monaco 2024, and run your agent system on that snapshot. This sidesteps all the hard real-time problems and lets you focus on the agent design — which is what the project is actually about.

**Tip:** Cache FastF1 sessions to disk explicitly via env var. Build a small loader that converts a `(year, event, session, lap_number)` tuple into a clean `RaceState` Pydantic object. This loader is the single most reusable piece of code across Projects 2 and 3.

## 3.4 Agent architecture

LangGraph state machine. Define this on paper before writing any code.

```text
STATE GRAPH

[RaceState input: lap, drivers, tyres, gaps, weather]
↓
initialise_state
↓
┌──────────────────┬──────────────────┬──────────────────┐
↓                  ↓                  ↓                  ↓
tyre_strategist  weather_analyst  gap_analyst  pit_window_calc
(parallel — all four run concurrently against the same input)
↓                  ↓                  ↓                  ↓
└──────────────────┴──────────────────┴──────────────────┘
↓
synthesise_strategy
↓
self_critique
↓ (if severity high, loop back to synthesise once)
↓
[final StrategyReport]

EACH NODE:
- takes State, returns updated State
- logs its inputs/outputs to Langfuse
- validates outputs with Pydantic
- has a max-iteration guard if it can loop
```

The four specialist agents run in parallel against the same input. This is one of LangGraph's strengths over a sequential ReAct loop and makes for a great interview talking point about agent topology choices.

**What each agent owns**

- **Tyre Strategist:** Given current tyre compounds, tyre ages, and recent stint pace, recommend whether each driver should pit, when, and which compound to switch to. Output: per-driver tyre recommendation with confidence.
- **Weather Analyst:** Given current weather and forecast, assess rain probability over the next 10 laps and what tyre compound would be optimal under each scenario. Output: weather-conditioned strategy adjustments.
- **Gap Analyst:** Given gaps between drivers, identify undercut and overcut opportunities and threats. Output: list of strategic gap windows with risk/reward notes.
- **Pit Window Calculator:** Given pit lane time loss, traffic, and current race position, calculate optimal pit windows for each driver. Output: per-driver pit window in lap range with expected position outcome.
- **Synthesiser:** Takes all four specialist outputs and produces a single coherent strategy report. This is the only agent that uses `gpt-4o`.
- **Critic:** Reviews the synthesised report against the original `RaceState`. Looks for contradictions, missed opportunities, factual errors. If severity is high, the graph loops back to the synthesiser once with the critique included as additional context.

## 3.5 Build sequence

### Phase A — Skeleton + Pydantic models (day 1, ~3 hours)

- Repo skeleton (universal standards).
- Define all Pydantic models BEFORE writing any agent code:
  - `RaceState` (lap, drivers, tyres, gaps, weather)
  - `DriverState` (number, name, tyre_compound, tyre_age, gap_to_leader, position)
  - `TyreRecommendation` (driver, action: pit/stay, target_compound, recommended_lap, confidence)
  - `WeatherAssessment` (rain_probability_next_10_laps, optimal_compound_per_scenario)
  - `GapOpportunity` (driver, type: undercut/overcut, target_lap_range, risk_score, reward_score)
  - `PitWindow` (driver, lap_range_start, lap_range_end, expected_position_after)
  - `StrategyReport` (summary, per_driver_recommendations, key_risks, confidence)
  - `Critique` (issues, severity: low/medium/high, suggestions)
- Write tests for the models. They cost nothing and show care.

### Phase B — Specialist agents as testable functions (days 2-3, ~6 hours)

Build each specialist as a clean function with Pydantic input and output. The functions should be testable without invoking the graph at all.

- `tyre_strategist(state: RaceState) → list[TyreRecommendation]`
- `weather_analyst(state: RaceState) → WeatherAssessment`
- `gap_analyst(state: RaceState) → list[GapOpportunity]`
- `pit_window_calculator(state: RaceState) → list[PitWindow]`
- Each function uses `gpt-4o-mini` with a tightly-scoped prompt and JSON-mode structured output.
- Each function gets unit tests that assert the schema is correct and that obvious cases produce obvious answers (e.g., tyre on lap 30 of a 70-lap race on hards, no rain, no pit window urgency → recommendation: stay).

*Why tests matter here: Most candidate agent projects have zero tests because "agents are non-deterministic". The senior answer is: each individual agent IS testable, you just have to test the schema and the obvious cases. Tests are how you show you know this.*

### Phase C — LangGraph wiring (days 4-5, ~6 hours)

- Define the State TypedDict (the shared mutable state passed between nodes).
- Write each node as a function `(state) → state_update`.
- Wire the graph: parallel fan-out to the four specialists, then fan-in to the synthesiser, then the critic with a conditional edge back to the synthesiser.
- Add max iteration guards (no infinite loops — cap at 1 self-critique cycle).
- Hook Langfuse tracing on every node — this is non-negotiable.
- End-to-end test with a single hardcoded `RaceState` (e.g., Monaco 2024 lap 25).

### Phase D — Self-critique loop (day 6, ~3 hours)

This is the part of the project that gets noticed.

- Write the critique prompt: "Given this strategy report and the original RaceState, identify issues with completeness, internal consistency, factual accuracy, and actionability. Output a Pydantic Critique."
- If critique severity is high, loop back to synthesise with the critique appended to the prompt context.
- Cap at one revision (otherwise costs balloon and infinite loops happen).
- Log both versions of the report to Langfuse for inspection.
- In the README, show a real before/after example: a critic flagged a contradiction, the revised report fixed it. This is gold for interviews.

### Phase E — Streamlit UI (day 7, ~3 hours)

- Streamlit app: dropdown to pick a historical race + lap, button to run, then live updates as nodes execute.
- Use `st.status` to show node-by-node progress (visually impressive in demos).
- Final `StrategyReport` rendered with markdown.
- Sidebar shows the Langfuse trace ID so you can click through.
- Sidebar also shows token usage and approximate cost for the run — this signals cost-awareness to interviewers.

### Phase F — Evaluation (days 8-9, ~5 hours)

- Hand-curate 12 historical race scenarios across conditions: dry race (Silverstone 2024 lap 30), wet race (Spa 2024 lap 15), Monaco 2024 lap 25 (overtaking nearly impossible — strategy-defined race), late-race undercut window (Hungary), safety-car-disrupted race, and so on.
- For each, write the expected key strategic decisions ("Driver X should pit on lap 32-35 to undercut Driver Y") based on what actually happened or what informed analysis suggests.
- Hand-write a rubric: completeness (0-3), accuracy of reasoning (0-3), F1 domain plausibility (0-3), report actionability (0-3).
- LLM-as-judge: `gpt-4o` reads the report against the rubric, outputs a Pydantic `JudgeScore`.
- Run all 12 scenarios, average the scores, save to `docs/evaluation_results.md`.
- Spot-check 3-4 manually — do you agree with the judge's scores? Document disagreements in the README. This honesty is high-signal.

**Important caveat:** LLM-as-judge has well-known biases (favours longer answers, favours its own outputs, anchors on first-presented options). Mention this as a limitation in the README. This is a standard interview topic and acknowledging it shows you know what you're doing.

### Phase G — Polish (day 10, ~3 hours)

- Architecture diagram showing the LangGraph state machine with the parallel fan-out and the critic loop.
- README with a clear example: one full `RaceState` input, the four specialist outputs, the synthesised report, the critique, the revised report.
- Demo video (90 seconds — agents take longer than RAG to demonstrate).
- Deploy to Hugging Face Spaces (Streamlit deploys nicely there).

## 3.6 Things to remember during the build

- FastF1 caches sessions to disk after first fetch. Configure cache location explicitly via env var; otherwise it dumps cache files everywhere and confuses Docker.
- Don't try to make the agents "creative". The whole point is that each specialist has a tightly-scoped job. Creativity in the wrong place produces hallucinated lap numbers and made-up strategies.
- LLM-as-judge has biases. Mention this as a limitation. Don't pretend the eval is perfect.
- Don't make the agent run for 90 seconds. If it does, profile and parallelise. The four specialists should run concurrently with asyncio, not sequentially.
- Cost discipline: a full multi-agent run is roughly 4 × specialist (gpt-4o-mini, ~£0.001) + synthesiser (gpt-4o, ~£0.02) + critic (gpt-4o, ~£0.01) = roughly £0.04 per run. Document this in the README.
- F1 strategy is genuinely contested even among real strategists. Don't pretend your agent has "the right answer". Frame it as a structured aid to a human decision.
- Avoid making strategy recommendations about the current ongoing season. Use historical races where the actual outcome is known. This makes the eval much easier and avoids the appearance of competing with real F1 teams.

## 3.7 Interview answers this project unlocks

- "Have you built agents?" — yes, here's the state graph diagram, here's the live demo, here's the trace in Langfuse
- "Why LangGraph over LangChain agents?" — "LangChain agents use ReAct, which is a single agent looping over tool calls. I needed multiple specialists with their own context and the ability to loop back for self-critique. LangGraph's explicit state model and explicit graph topology fits that better — I can see exactly what state each node receives and produces, and I can run the four specialists in parallel."
- "How do you evaluate an agent?" — LLM-as-judge with a 0-12 rubric across four dimensions, plus honest discussion of judge biases, plus manual spot-checking on 3-4 scenarios
- "How do you handle agent failures?" — bounded loops, max iteration guards, Pydantic validation at every step, fall-through paths if a specialist fails
- "How do you design agents/tools?" — Pydantic in/out, single responsibility, testable in isolation, schema-validated at every boundary
- "What about cost?" — gpt-4o-mini for the four specialists where the work is well-scoped, gpt-4o only for the synthesiser and critic where genuine reasoning is needed. Roughly £0.04 per run, which I documented in the README.
- "How do you decide when to use a multi-agent system instead of a single agent?" — "When the sub-problems are genuinely separable and benefit from specialised context. F1 strategy is multi-agent in real life. A general chat assistant is single-agent. Forcing multi-agent on a problem that doesn't decompose is a common anti-pattern."

## 3.8 README headline

> **F1 Race Strategy Multi-Agent System** — A LangGraph multi-agent system that produces structured race strategy recommendations from real F1 race state. Four specialist agents (tyre, weather, gaps, pit windows) run in parallel against the same input, a synthesiser combines their outputs into a coherent report, and a critic agent reviews the report and can trigger one revision pass. Evaluated across 12 historical race scenarios with an LLM-as-judge rubric averaging 9.4/12. Full Langfuse traces and a Streamlit live demo.

---

# Section 4 — Project 3: F1 Telemetry Anomaly Service

## 4.1 The pitch

A production FastAPI microservice that ingests F1 lap timing and telemetry data, uses statistical methods to detect anomalous laps, then uses an LLM to generate structured natural-language explanations for the flagged anomalies. Hybrid statistical + LLM architecture, Redis caching, full observability.

**Why this project, and why this domain**

This is the project that demonstrates the rarest skill in the candidate pool: knowing when NOT to use an LLM.

Most junior AI engineers want to LLM everything. Showing that you used statistical methods for the detection layer (where they're appropriate) and LLMs only for the explanation layer (where natural language matters) is genuinely senior thinking. This signals judgment that interviewers can't easily test for any other way.

The F1 telemetry domain works because the data is rich, free, and visually compelling. FastF1 gives you sector times, weather, tyre stints, lap-by-lap position changes — proper engineering data. The shared FastF1 dependency with Project 2 also strengthens the portfolio thread: "I built a full data engineering stack on F1 historical data."

## 4.2 Stack

- **Language:** Python 3.12
- **Data:** `fastf1` library (free, official-derived) — same as Project 2
- **Statistical methods:** `numpy` + `scipy` + `scikit-learn` (Isolation Forest)
- **LLM:** `gpt-4o-mini` for explanation generation. *(Optional: you can later add a local model via Ollama to further demonstrate open-source capability — see note in 4.6.)*
- **Caching:** Redis
- **API:** FastAPI
- **Observability:** Prometheus + simple Grafana dashboard
- **Container:** Docker Compose (api + redis + prometheus + grafana)
- **Deployment:** Hugging Face Spaces or Railway

## 4.3 The data

FastF1 caches data locally after the first fetch, which is great for dev cost. A typical race session gives you ~20 drivers × 50-70 laps × 20+ telemetry channels — plenty to work with.

- Lap timing: Driver, Lap number, LapTime, Sector1Time, Sector2Time, Sector3Time, Compound, TyreLife, Position
- Telemetry per lap (sampled at ~4Hz): Speed, Throttle, Brake, Gear, RPM, DRS
- Weather: AirTemp, TrackTemp, Humidity, Rainfall

## 4.4 What counts as an anomaly

Define this precisely up front — it's the spec for your detector.

- Lap time z-score > 2.5 vs that driver's recent stint
- Sector time outlier (one sector slow, others fine — suggests a localised event)
- Sudden mid-stint pace drop (>2s/lap drop sustained for 3+ laps — tyre or mechanical)
- Off-pace lap with normal sectors and DRS off (suggests yellow flag or off-track)
- Pace inconsistency relative to track conditions (slow when track is improving)

## 4.5 Build sequence

### Phase A — Skeleton + data exploration (days 1-2, ~5 hours)

- Repo skeleton.
- Notebook (kept in `notebooks/`) to explore FastF1 data — this is the only place a notebook is acceptable.
- Pick 3-5 reference sessions to develop against (e.g. Monaco 2024, Silverstone 2024, a wet race).
- Hand-identify 10-15 anomalies in those sessions yourself (e.g. "Sainz lap 32 at Silverstone — ran wide at Copse"). These become your test cases.
- If you built the FastF1 loader for Project 2, reuse it here.

### Phase B — Statistical detection (days 3-4, ~6 hours)

- Pydantic data models: `LapData`, `SessionData`, `Anomaly`, `AnomalyContext`.
- Z-score detector: per-driver, per-stint.
- Sector-imbalance detector.
- Stint pace-drop detector.
- Isolation Forest detector across full feature space — for catching things the rule-based detectors miss.
- Combine detector outputs into a single `Anomaly` object with: type, severity (low/medium/high), driver, lap, evidence (the numerical features that triggered it).
- Test against your hand-identified anomalies. Aim for >80% recall on your manual list.

### Phase C — LLM explanation layer (days 5-6, ~4 hours)

- For each `Anomaly`, build an `AnomalyContext` with: surrounding laps, weather, tyre, position changes, gap to leader.
- Prompt the LLM with the context and ask for a structured explanation: `plausible_causes` (list, ranked), `confidence`, `recommended_investigation`.
- Cache aggressively: same anomaly hash → same explanation. F1 sessions are immutable once raced.
- **Important:** do NOT let the LLM 'detect' anomalies. Its only job is to explain ones the statistical layer found. Make this division of labour explicit in the README.

### Phase D — API and caching (day 7, ~3 hours)

- FastAPI: `/analyse/{year}/{event}/{session}` endpoint.
- Redis cache for analysed sessions (key = year+event+session, value = full Anomaly list with explanations).
- First call takes ~30 seconds; cached calls return in <100ms. This is a great demo and a good interview story.
- Pydantic response schemas. OpenAPI auto-generated docs.
- Rate limiting.

### Phase E — Observability (day 8, ~3 hours)

- Prometheus metrics: requests/sec, p50/p95/p99 latency, cache hit rate, LLM token usage, anomalies detected per session.
- Grafana dashboard with those panels (just one page).
- Screenshot the dashboard for the README.
- Structured logging via `loguru`.

### Phase F — Tests + Docker (day 9, ~3 hours)

- Unit tests on each detector with synthetic data.
- Integration test using a cached FastF1 session.
- Mock the LLM in tests (don't burn money on test runs).
- Multi-stage Dockerfile.
- Docker Compose: api + redis + prometheus + grafana.

### Phase G — Polish (day 10, ~3 hours)

- Architecture diagram showing the hybrid pipeline (statistical → LLM → cache).
- README with the killer 'why this is hybrid, not all-LLM' section. Be explicit.
- Latency benchmarks table (cold call, warm call, cache hit).
- Cost-per-session calculation.
- Deploy. Live link in README.

## 4.6 Things to remember during the build

- FastF1 caches to disk. Configure cache location explicitly via env var; otherwise it dumps cache files everywhere and confuses Docker.
- Driver pace varies by tyre compound and stint phase. A z-score detector that doesn't account for stint context will flag every fresh-tyre lap as anomalously fast. Group by stint, not by session.
- Wet races break most detectors. Either filter them out for v1 or add a 'wet conditions' flag and adjust thresholds. Document the choice.
- LLM explanations can sound confident even when wrong (e.g. claiming a yellow flag occurred when it didn't). Always include a `confidence: low` option in the schema and instruct the LLM to use it freely.
- Don't try to be a real-time service. F1 sessions are post-hoc analysis. Frame it as such.
- Cost: a full session has ~50 anomalies × ~500 tokens of explanation = ~25k tokens × £0.0003/1k input = ~£0.50 per session uncached, free when cached.
- **Optional stretch:** To show open-source model serving, you could later replace `gpt-4o-mini` with a local model like `llama3.2:3b` via Ollama. This would let you discuss latency/quality trade-offs and serving your own model. Only do this if you have extra time; the core hybrid architecture already proves the critical judgement.

## 4.7 Interview answers this project unlocks

- "When wouldn't you use an LLM?" — concrete example. "Anomaly detection is a statistical problem. Using an LLM for it would be slow, expensive, and worse at the actual task. I used the LLM only for the explanation layer where natural language matters."
- "How do you put an LLM service in production?" — link, here's p95 latency, here's cost per request, here's the cache hit rate
- "How do you handle cost in production?" — caching strategy, hybrid architecture, model selection
- "How would you scale this?" — Redis is single-node; for multi-region you'd need a distributed cache. The detector layer is embarrassingly parallel; you'd shard by session.
- "Have you used Prometheus / observability?" — yes, here's the Grafana dashboard
- "How do you test code that calls an LLM?" — mock the LLM in tests; have a separate small test suite that hits the real LLM occasionally and runs in CI on a schedule, not on every push

## 4.8 README headline

> **F1 Telemetry Anomaly Service** — A production FastAPI microservice that detects anomalous F1 laps using statistical methods (z-scores, Isolation Forest, sector imbalance) and explains them using an LLM. Hybrid architecture: statistical layer for detection, `gpt-4o-mini` for natural-language explanations. Redis caching gives sub-100ms p95 on warm requests. Full Prometheus + Grafana observability. Cost: ~£0.50 per uncached session, free when cached.

---

# Closing notes

## How the three projects together cover the AI Engineer skill stack

Each project deliberately targets a different category of AI engineering work, so the coherent F1 domain doesn't mean repeating the same skills three times. Together they cover what AI Engineer job descriptions in 2026 ask for:

- **Project 1 (RAG):** Retrieval, vector databases, chunking, hybrid retrieval, reranking, RAGAS evaluation, LangChain LCEL, FastAPI, observability, **open-source vs. cloud embeddings comparison**.
- **Project 2 (Multi-Agent):** LangGraph, multi-agent orchestration, parallel agent execution, structured outputs at every node, self-critique loops, tool design, LLM-as-judge evaluation.
- **Project 3 (Hybrid Service):** Knowing when NOT to use an LLM, hybrid statistical + LLM architecture, FastAPI production patterns, Redis caching, Prometheus + Grafana, cost engineering.

Three projects, one domain, three genuinely different categories of production AI work. The portfolio elevator pitch becomes: "end-to-end AI engineering applied to Formula 1 data — retrieval, agents, and production services."

## Order of priority if time runs out

If you can only ship two of the three, ship Project 1 and Project 3. Together they cover the two most-asked things in AI Engineer interviews — RAG and production LLM services — and the F1 thematic continuity makes the portfolio coherent. Project 2 (the multi-agent system) is the most fashionable but the least essential for entry/mid-level roles.

If you can only ship one, ship Project 1. RAG with rigorous evaluation is the single highest-signal portfolio piece for an AI Engineer role in 2026.

## Updating the CV

As each project finishes, update the CV's Selected Projects section with concrete numbers. Don't update the CV with vague claims like "built a RAG system". Update with: "Built a hybrid retrieval RAG system over 600 pages of FIA F1 regulations; achieved 0.91 faithfulness and 0.83 context precision on a 45-question evaluation set; compared OpenAI and open-source (BGE) embeddings; deployed via Docker on Hugging Face Spaces."

Specificity is what separates portfolio projects that get interviews from ones that get scrolled past. Include the GitHub link in the bullet itself, not just at the end of the document. Recruiters click. Make it easy.

## When to apply for jobs

Don't wait for all three projects. Apply with the current CV starting now. As Project 1 lands, update the CV and re-apply. Each project landing is a re-application opportunity for roles that didn't respond initially.

*Realistic expectation: you should expect rejections at the rate any candidate sees in this market. Aim for 2-3 technical interviews from every 30-50 applications. The portfolio is what gets you over the line in the technical interview, not what gets you the interview itself — the interview comes from the CV plus referrals.*

## If you get stuck

Use a fresh chat with another Claude instance for each project. Paste the relevant section of this document plus Section 1 (Universal Standards) at the top. Then work through phase by phase, asking for help on specific sub-tasks rather than "build me the whole thing".

If you hit something genuinely hard — for example, hierarchical chunking on PDFs that don't have clean article boundaries, or a LangGraph node that won't pass state correctly — bring it back here. We can debug without the project chat losing focus.

---

*End of brief*
