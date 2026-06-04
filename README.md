# AI Noise Reducer Agent (Anti AI Slop)

<p align="center">
  <b>Convert 10 minutes of reading into 60 seconds of verified understanding.</b><br/>
  Evidence-first. Retrieval-first. Trust-scored. Open and extensible.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.11%2B-blue.svg">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-API-green.svg">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-black.svg">
  <img alt="Status" src="https://img.shields.io/badge/status-open%20source-brightgreen.svg">
</p>

---

## Why this project exists

The modern web is increasingly saturated with:

- AI-generated SEO filler
- rewritten content farms
- affiliate spam
- repetitive low-information posts

This project is built to extract **signal from noise**.

Given a URL (or raw text), AI Noise Reducer Agent produces:

1. **AI Slop Score**
2. **Information Density Score**
3. **Trust Score**
4. **Hard Facts**
5. **Evidence Table**
6. **Contradictions**
7. **Missing Information**
8. **60-second Executive Brief**

Every generated insight is designed to be traceable back to source evidence.

---

## Core principles

1. **Retrieval before generation**
2. **Evidence before summary**
3. **Classification before LLM**
4. **Human-verifiable outputs**
5. **Continuous benchmark evaluation**
6. **Prefer strong open models before custom training**

---

## What is implemented

This repository includes full code scaffolding for all roadmap phases:

- ✅ **Phase 0** — Benchmarking + evaluation framework
- ✅ **Phase 1** — MVP API + extraction + slop scoring + hard-fact summary
- ✅ **Phase 2** — Information density + evidence + entity extraction
- ✅ **Phase 3** — Citation analysis + source credibility + trust scoring
- ✅ **Phase 4** — Knowledge brain adapters (Qdrant + Neo4j) + versioning
- ✅ **Phase 5** — Research learning engine (arXiv / ACL / Semantic Scholar connectors)
- ✅ **Phase 6** — Feedback learning (ingest / replay / error analysis)
- ✅ **Phase 7** — Custom training scaffolds + benchmark gate
- ✅ **Phase 8** — Scale hooks (observability / analytics / i18n)

---

## Architecture overview

```text
Input (URL / raw text)
        │
        ▼
[Extraction Pipeline]
  - URL fetch + content extraction
        │
        ▼
[Analysis Pipeline]
  - AI Slop Detection
  - Information Density
  - Evidence Extraction
  - Entity Extraction
  - Hard Fact Engine
  - Citation Analysis
  - Source Credibility
  - Trust Aggregation
        │
        ▼
[Orchestrator]
  - Produces final analysis response
  - Emits analytics + metrics
  - Persists benchmark/feedback
        │
        ├──► PostgreSQL (benchmark + feedback records)
        ├──► Qdrant (vector knowledge memory)
        └──► Neo4j (knowledge graph memory)
```

---

## Project structure

```text
src/ai_noise_reducer/
├── __init__.py
├── api.py
├── orchestration.py
├── config.py
├── logging.py
├── domain_models.py
├── pipeline/
│   ├── extraction.py
│   ├── slop_detection.py
│   ├── information_density.py
│   ├── evidence_extraction.py
│   ├── entity_extraction.py
│   ├── hard_fact_engine.py
│   ├── citation_analysis.py
│   ├── source_credibility.py
│   └── trust_engine.py
├── storage/
│   ├── postgres_repo.py
│   ├── qdrant_repo.py
│   └── neo4j_repo.py
├── knowledge/
│   └── versioning.py
├── research/
│   ├── connectors.py
│   └── learning_engine.py
├── feedback/
│   └── learning.py
├── benchmark/
│   ├── evaluation.py
│   └── competitor_analysis.py
├── training/
│   └── scaffolds.py
└── scale/
    ├── observability.py
    ├── analytics.py
    └── i18n.py
```

---

## Quick start

### 1) Requirements

- Python **3.11+**
- Optional for full runtime integrations:
  - PostgreSQL
  - Qdrant
  - Neo4j

### 2) Install

```bash
pip install -e .
```

### 3) Run API

```bash
uvicorn ai_noise_reducer.api:app --reload
```

API docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## API endpoints

### Health & status

- `GET /health` — service health
- `GET /status` — runtime metrics + analytics snapshot

### Analysis

- `POST /analyze` — core analysis workflow (URL/raw text → scores + facts + evidence)

### Benchmarking

- `POST /benchmark/record` — persist benchmark record
- `POST /benchmark/evaluate` — evaluate precision/recall/hallucination/latency
- `GET /competitor/template` — competitor analysis template

### Feedback learning

- `POST /feedback` — ingest user correction feedback

### Research learning

- `POST /research/update` — discover + ingest research items + version update

### Training (conditional phase scaffolding)

- `GET /training/scaffolds` — dataset contract specs
- `GET /training/gate?baseline=<x>&candidate=<y>` — train/no-train decision gate

---

## Example request

### Analyze content

```bash
curl -X POST "http://127.0.0.1:8000/analyze?language=en" \
  -H "Content-Type: application/json" \
  -d '{
    "source_name": "Example Source",
    "url": "https://example.com"
  }'
```

---

## Configuration

Configuration is centralized in:

- `src/ai_noise_reducer/config.py`

Typical categories include:

- application environment
- timeouts
- PostgreSQL connection
- Qdrant connection
- Neo4j connection

Use environment variables to customize runtime values in production.

---

## Storage and memory model

### PostgreSQL

Used for:

- benchmark records
- feedback records

### Qdrant

Used for:

- vector memory of knowledge items

### Neo4j

Used for:

- graph memory relationships and long-term knowledge structure

### Knowledge versioning

`knowledge/versioning.py` provides version IDs to track each research update cycle for auditability and reproducibility.

---

## Evaluation philosophy

The project prioritizes measurable quality via:

- precision
- recall
- hallucination rate
- latency

Target directions (from roadmap vision):

- high fact precision/recall
- low hallucination
- high trust-human agreement
- significant user reading-time reduction

---

## Roadmap alignment

This codebase follows the documented development roadmap and strategic docs:

- `CLAUDE.md`
- `PROJECT-detail.md`
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md`
- `SECOND-KNOWLEDGE-BRAIN.md`

---

## Open-source notes

This repository is designed to be:

- modular
- composable
- benchmark-driven
- evidence-first

Contributions are welcome in:

- extraction quality improvements
- model-backed scoring upgrades
- connector reliability
- benchmark datasets
- eval harness hardening
- production deployment templates

---

## Known current scope

This release is a complete coding implementation of the multi-phase architecture.
Production hardening tasks (deployment infra, secrets management, comprehensive runtime testing, CI pipelines, model quality tuning with real datasets) can be layered on top directly.

---

## License

MIT (recommended for open source).  
If you use a different license, update this section accordingly.

---

## Citation

If this project helps your work, cite the repository and link to your deployment/use case.  
Evidence-first knowledge tooling improves faster when results are shared openly.
