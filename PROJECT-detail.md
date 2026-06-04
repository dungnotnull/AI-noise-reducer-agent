
# PROJECT DETAIL

# Executive Assessment

The original concept is strong but should not be implemented as a pure prompt-engineering project.

The highest-value version is an AI Content Intelligence Platform.

## Core Problem

Internet content is increasingly polluted by:

- AI-generated SEO articles
- Affiliate spam
- Rewritten content farms
- Low-information blog posts
- Redundant AI summaries

Users need:
- Facts
- Evidence
- Numbers
- Insights

not 3000 words of filler.

---

# Final Product Vision

Input:
Any webpage.

Output:

1. AI Slop Score
2. Information Density Score
3. Trust Score
4. Hard Facts
5. Evidence Table
6. Contradictions
7. Missing Information
8. 60-second Executive Brief

---

# System Architecture

## Layer 1 — Content Acquisition

Responsibilities:
- Browser Extension
- Reader Mode Extraction
- Boilerplate Removal
- Ad Removal

Tools:
- Readability.js
- Trafilatura

---

## Layer 2 — AI Slop Detection

Features:

### Linguistic Features
- Repetition Ratio
- Entropy Score
- Lexical Diversity
- Burstiness

### Content Features
- Citation Density
- Fact Density
- Claim Density
- Numerical Evidence Ratio

### AI-Slop Patterns
- Generic transitions
- Empty introductions
- Circular explanations
- Excessive adjectives

Models:
- ModernBERT
- DeBERTa-v3

Output:
AI Slop Score (0–100)

---

## Layer 3 — Information Density Engine

Metrics:

Information Density =
Unique Facts / Total Words

Additional Metrics:
- Entities per 100 words
- Numerical Facts
- Evidence Count
- Unique Claims

Output:
Information Density Score

---

## Layer 4 — Evidence Extraction

Extract:
- Statistics
- Research Findings
- Citations
- Dates
- Numbers
- Quotes

Build evidence graph.

---

## Layer 5 — Hard Fact Engine

Convert article into:

- Facts
- Metrics
- Entities
- Evidence

Remove:
- Marketing language
- AI filler
- Redundant paragraphs

Technique:
Chain of Density + Retrieval Validation

---

## Layer 6 — Trust Score Engine

Trust Score =
0.35 Evidence Quality
+0.25 Citation Quality
+0.20 Information Density
+0.10 Source Authority
+0.10 Freshness

This becomes the main user-facing metric.

---

## Layer 7 — Research Learning Engine

Sources:

- arXiv
- Semantic Scholar
- ACL Anthology
- Papers With Code
- OpenAI Research
- Anthropic Research
- Google DeepMind
- Hugging Face Papers

Process:

Discover → Extract → Validate → Embed → Store → Benchmark

---

## Layer 8 — Knowledge Brain

Files:
- SECOND-KNOWLEDGE-BRAIN.md

Storage:
- Qdrant
- Neo4j

Capabilities:
- Long-term memory
- Research evolution tracking
- Retrieval augmentation

---

# Competitive Moat

The moat is NOT summarization.

The moat is:

- Knowledge accumulation
- Research ingestion
- Benchmarking
- Trust scoring
- Proprietary fact graph

---

# ML Training Strategy

DO NOT train models initially.

Phase 1:
Use HuggingFace models.

Phase 2:
Collect labeled data.

Phase 3:
Train only if:
- >10% improvement
- Significant ROI

Potential future models:

- AI Slop Classifier
- Fact Density Predictor
- Trust Score Predictor

---

# Success Metrics

- Fact Precision > 90%
- Fact Recall > 85%
- Hallucination Rate < 2%
- User Reading Time Saved > 80%
- Trust Score Correlation with Human Experts > 0.8
