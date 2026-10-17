# 07 — `NovelSeekUpdateInternAgent.pdf`: InternAgent Team (Shanghai AI Lab), *InternAgent: When Agent Becomes the Scientist — Building Closed-Loop System from Hypothesis to Verification* (arXiv:2505.16938v3, July 2025; earlier name NovelSeek)

**Read:** 2026-10-16, all 34 pages (pdftotext, 17,532 words): body (lines 1–1,148) and appendices A–D (lines 1,213–1,472) in full; the reference list (lines 1,149–1,212) checked, not studied.

## What it says (isolated read)
- **A closed loop for autonomous research:** (1) self-evolving idea generation with human feedback, (2) idea-to-methodology construction, (3) evolutionary experiment planning and execution. Twelve tasks (reaction yield, molecular dynamics, power flow, time series, transcription response, enhancer activity, sentiment, 2-D/3-D classification, segmentation, driving detection, VLM fine-tuning).
- **Agents:** Survey (two modes: broad literature review by keyword combinations scored for relevance in [0,1]; deep research that reads full texts and generates new keywords); Code Review (static analysis with Python `ast`, summaries, repo- and file-level); Idea Innovation (high-temperature generation G:(T,B,L)→I and evolution G:(I,C,L)→I′ using critique and literature); Assessment (0–10 scores on coherence, credibility, verifiability, novelty, alignment; weighted sum; **keeps the top set diverse** so near-duplicates don't crowd it); Orchestration (workflow, memory, and *when* to ask the human — after high-scoring ideas).
- **Idea → method:** initialization T:(I,T,B,L)→M, then refinement R:(M,C,L)→M′ with critiques and literature; a method is detailed enough to code.
- **Execution:** exception-guided debugging (run → capture traceback → understand context → plan fix → apply; max 4 attempts); Aider for single files, OpenHands for repositories. **Adaptive evolution:** implement step by step, measure after each step, keep a record of decisions and their effects, and re-plan. Example path on 3-D classification: +0.5 → +1.2 → +1.6 → **−0.8 (rolled back, simplified)** → +2.1 points.
- **Settings:** 50 papers surveyed; 15 ideas, each evolved into 3, top 5 kept, up to 4 rounds; GPT-4o for ideas, Claude 3.7 Sonnet for code; ~$0.6 per idea and ~$0.4–1.2 per coding run.
- **Results, reported with denominators:** e.g. enhancer activity 0.65 → 0.79 (8 improved / 8 ran / 10 tested); reaction yield 27.6 → 35.4 R² (4/6/10); segmentation 78.8 → 81.0 mIoU (9/9/10). Few-shot yield is reported over 5 repeats with spread (baseline 24.2 ± 4.2 vs 34.8 ± 1.1). Adaptive evolution doubled the share of improving ideas on yield (40 % vs 20 %). Human review: 5 qualified reviewers × 20 ideas per task, ≥ 10 minutes per idea, with explicit soundness/contribution/overall/confidence rubrics.
- **Stated future work:** papers as structured triples in a graph for meta-analysis; evaluate an idea's *value*, not just novelty; check that code matches the stated method.

## Observations
- The headline numbers mix settings: the abstract quotes yield 27.6 → 35.4, the introduction 24.2 ± 4.2 → 34.8 ± 1.1 (a few-shot variant). Both are true for their settings; the reader needs the setting to compare.

## Links to the earlier documents (compounding)
- **The decisive signal is the experiment, not the judge.** The Assessment agent is an LLM grader (06 says LLM self-assessment is weakly calibrated); InternAgent's gains are proven by runs and human reviewers. This is the cure for document 04's self-confirming Amaterasu loop: new knowledge counts only after an independent test.
- **Phoenix/Rogue X done with discipline:** mutate → measure → keep or roll back, with a decision log. The −0.8 rollback is the behaviour the Kintsugi/Rogue X story (03) describes but never measures.
- **Honest reporting = Tufte's integrity (01):** improved/ran/tested triples and repeat spreads are "compared to what?" in practice. Integra experiments (T5, T8) should report the same triple.
- **Diversity in the top set** answers a measured Integra problem (the legacy Chroma had 2,974 exact duplicates in 5,526 rows): retrieval and promotion should penalise near-duplicates.
- **When to ask the human** (after high-scoring candidates) is the same shape as the Phoenix Force two-key rule (T6): autonomy for low-stakes steps, the Architect's key for consequential ones.
- **Survey modes** map onto Alexandria's tiers: breadth first, then depth driven by the terms the ideas actually use.
