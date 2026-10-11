# Rodin Sub-Agents and the Gemini Model Lineup — Daily Planet Research Brief

> **Architect's rulings after this brief (2026-10-09, later the same evening):**
> 1. **Gemini 3.5, 3.6 and 3.7 Flash are removed from Integra entirely.** They are all deprecated or retiring within months; none of them may be used, proposed or kept as a fallback. The "3.5 Flash-Lite fallback" in §3 T3, §5 item 4 and the option table below is withdrawn.
> 2. **The Antigravity agent is Rodin's agent model.** It is the most immediately identified agent for the Rodin function: the orchestrator and its sub-agents run as the Antigravity agent (`antigravity-preview-09-2026`, built on `gemini-3.8-flash`, same harness as the Antigravity IDE). Its `agent_config.model` stays `gemini-3.8-flash`, the only remaining allowed value once 3.5 and 3.6 are removed. Sub-agents still carry no model of their own (they inherit the Antigravity base agent).
> 3. **Gemini 3.1 Pro Preview is superseded** (its knowledge ends in 2025) by **Gemini 3.8 Flash at `thinking_level: high`** as a placeholder, until **Gemini 4 Argon** is available. See the master blueprint, R-11.

**Research window:** 2026-10-09, about 20:20–21:00 CDT (Google pages carry "last updated" stamps of 2026-10-09 or 2026-10-10 UTC unless noted).
**Method:** Daily Planet Protocol stages, carried out by hand with the Firecrawl search and scrape tools: (1) ingestion, (2) provenance audit, (3) dialectic, (4) binding to Integra, (5) synthesis. Stage 6 (Hoard injection) was not run; see the end of this brief.
**Question from the Architect:** Rodin Route Retrieval's orchestrator core runs on "Gemini 3.8, without Flash". Rodin's sub-agents should carry **no Gemini model**: they can be the local environment's base agent for now, and later either "3.7" or no model at all (secondary extensions of Rodin). What does Google's own documentation say, and what is the best outcome, given upcoming deprecations?

---

## 1. Ingestion — sources read

Primary sources (Google). "Read in full" means every line was read.

| # | Source | Page date | Read |
|:--|:--|:--|:--|
| S1 | Gemini API — Models (ai.google.dev/gemini-api/docs/models) | 2026-10-09 | in full |
| S2 | Gemini API — Gemini deprecations (…/docs/deprecations) | 2026-10-09 | in full |
| S3 | Gemini API — Release notes (…/docs/changelog), 1,564 lines | 2026-10-09 | in full |
| S4 | Gemini API — Gemini 3.8 Flash model page | 2026-09-02 | in full |
| S5 | Gemini API — What's new in Gemini 3.8 Flash (…/docs/latest-model) | 2026-10-09 | in full |
| S6 | Gemini API — Gemini Embedding 2 model page | 2026-04-28 | in full |
| S7 | Agent Platform — Model versions and lifecycle (docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions) | 2026-10-10 | in full |
| S8 | Agent Platform — Gemini 3.1 Pro model page | n/a | targeted extract |
| S9 | Agent Platform — Release notes (July 9, 2026 entry) | n/a | targeted extract |
| S10 | Gemini API — Antigravity agent guide (…/docs/antigravity-agent) | 2026-10-09 | prose, model selection, environments, pricing, limits |
| S11 | Gemini API — Building managed agents (…/docs/custom-agents) | 2026-10-09 | prose, definition reference, limits |
| S12 | Gemini API — Agent environments (…/docs/agent-environment) | 2026-10-07 | overview, pricing, limits |
| S13 | Antigravity docs — Custom subagents (antigravity.google/docs/subagents) | n/a | in full |
| S14 | Gemini API — Pricing (…/docs/pricing) | n/a | direct-quote extract (some table headings lost; only unambiguous rows used) |
| S15 | Local copy — Gemini CLI subagents reference (`docs/gemini_cli_subagent_reference.md`) | 2026-10-09 file | in full (earlier) |

Third-party sources, used only to cross-check: laozhang.ai blog on the 3.7 → 3.8 migration; promptfoo's Vertex provider page (3.8 Flash pricing); thecloudcollective.es (September 2026 model summary); omidsaffari.com (Antigravity `local_environment` migration); a Medium post on the Gemini 2.5 retirement on Vertex.

## 2. Provenance audit

- **Two Google platforms, two lifecycles.** Google now runs the same models under two names with different schedules: the **Gemini Developer API** (ai.google.dev, AI Studio keys) and the **Gemini Enterprise Agent Platform** (the new name for Vertex AI, docs.cloud.google.com). The Genesis Kernel reaches Gemini through Vertex express mode (`core/api_clients.py:112`, `genai.Client(vertexai=True, …)`), so **the Agent Platform schedule (S7) governs the kernel**, and the Developer API schedule (S2) governs AI Studio keys and Gemini API managed agents.
- **Embedding 2 model code.** S1's endpoint table lists `gemini-embedding-2-preview`, while S2, S3 (April 22, 2026: "Released `gemini-embedding-2` as generally available") and S6 (stable: `gemini-embedding-2`) agree on **`gemini-embedding-2`**. Verdict: S1's cell is stale. Use `gemini-embedding-2`.
- **Rejected third-party claim.** thecloudcollective.es says Gemini 3.1 Pro Preview is "scheduled for discontinuation starting May 7, 2027 (replacement: 3.5 Flash-Lite)". S2 lists `gemini-3.1-pro-preview` with **no shutdown date**, and S8 lists it as **public preview with no retirement date**. The quoted date and replacement match `gemini-3.1-flash-lite` exactly (S2: shutdown May 7, 2027 → `gemini-3.5-flash-lite`), so the blog has almost certainly conflated the two. Not used.
- **Ambiguous release-note snippet resolved.** A search excerpt of S9 read "Retirement for preview models for 2.5 Flash, 2.5 Flash-Lite, and 3.1". The full entry (July 9, 2026) names `gemini-3.1-flash-lite-preview`, not 3.1 Pro.
- **Pricing.** Only rows confirmed by two primary sources, or clearly headed in S14, are used: 3.8 Flash (S5 + S14), 3.5 Flash-Lite (S14), Embedding 2 (S14).

## 3. Dialectic — the tensions and how they resolve

### T1. "Base 3.8, without Flash" against what Google offers

Google publishes **no non-Flash Gemini 3.8 text model.** The complete 3.8 family is: `gemini-3.8-flash` (text, stable GA September 2, 2026), `gemini-3.8-live` and `gemini-3.8-live-extended-thinking` (voice), `gemini-3.8-flash-tts` and `gemini-3.8-flash-lite-tts` (speech), plus `gemini-3.8-flash-cyber` on the Agent Platform (S1, S2, S7). In the 3.x generation "Flash" is Google's main workhorse line; the light tier is "Flash-Lite", and the only 3.x Pro model is `gemini-3.1-pro-preview`.
**Resolution:** Integra can call Rodin's core "Gemini 3.8" in its own vocabulary, but the model string must be **`gemini-3.8-flash`**. That is also the default model of Google's Antigravity agent ("built with Gemini 3.8 Flash and uses the same harness as the Antigravity IDE", S10) and the default for managed agents (S11).

### T2. "3.7" as the future sub-agent designation

- S3, **October 8, 2026**: "`gemini-3.7-flash` is deprecated and has been replaced by `gemini-3.8-flash`. All requests to `gemini-3.7-flash` are automatically routed to `gemini-3.8-flash`."
- S7: on the Agent Platform, `gemini-3.7-flash` **retires January 28, 2027** (replacement `gemini-3.8-flash`).
- S13: an Antigravity sub-agent's `model` field accepts only **tiers**, `inherit` (default), `flash` or `pro`, not version strings, so "3.7" cannot be selected there at all.
- S10 and S11: Gemini API managed agents accept only `gemini-3.8-flash`, `gemini-3.6-flash` and `gemini-3.5-flash-lite`.

**Resolution:** "3.7" is no longer a real choice. On the Developer API it silently becomes 3.8 Flash; on the platform the kernel uses it ends on January 28, 2027; and neither agent system lets you pick it. **Do not designate 3.7.**

### T3. Google's own sub-agent recommendation against the Architect's "no Flash"

S3, July 21, 2026, describes **Gemini 3.5 Flash-Lite** as "a low-latency, highly cost-effective subagent option designed for high-volume automation". It has the longest guaranteed availability of the current Flash-family models on the Agent Platform ("July 21, 2027 or later", S7) and costs $0.30 / $2.50 per million input / output tokens (S14).
**Resolution:** the Architect's parameter wins. Record 3.5 Flash-Lite as the documented fallback if Rodin's sub-agents ever need a model of their own, not as the plan.

### T4. Developer API against Agent Platform dates

| Model | Developer API (S2) | Agent Platform (S7) — governs the kernel |
|:--|:--|:--|
| `gemini-3.8-flash` | No shutdown announced | No retirement announced (short-term class: at least 45 days' notice when scheduled) |
| `gemini-3.7-flash` | Deprecated 10/08/2026; routed to 3.8 Flash | **Retires 2027-01-28** |
| `gemini-3.6-flash` | No shutdown announced | **Retires 2026-11-19** |
| `gemini-3.5-flash` | Deprecated; routed to 3.6 Flash | Available until 2027-05-19 or later |
| `gemini-3.5-flash-lite` | No shutdown announced | Available until 2027-07-21 or later |
| `gemini-3.1-pro-preview` | Preview; no shutdown announced (previews can be deprecated with ≥ 2 weeks' notice, S1) | Public preview, global region only; no date listed (S8) |
| `gemini-2.5-pro` / `-flash` / `-flash-lite` | Access limited to existing users (S3, 9/18/2026) | **Retire 2026-10-20** |
| `text-embedding-004` | **Shut down 2026-01-14** | **Served until 2027-04-01** |
| `gemini-embedding-2` | GA 2026-04-22; no shutdown | Released 2026-04-22; no retirement listed |
| `gemini-embedding-001` | Shutdown 2028-05-14 | No sooner than 2028-05-20 |

**Resolution:** read the right column for anything the kernel calls. One consequence settles an open question from the blueprint (N3, ADR-005): Rodin's default embedding model, `text-embedding-004`, is dead on the Developer API but **still served on the Agent Platform until April 1, 2027**. That explains why the 10/07 self-test returned 768-dimension embeddings through Vertex express mode. It is a hard deadline, not a reprieve.

### T5. "No model at all" against "local environment base agent"

These turn out to be the same instruction, seen from two places:
- **In Antigravity**, a sub-agent declared with `model: inherit` has no model of its own: it runs on whatever its parent runs (S13). For Google's Antigravity agent the parent's default is `gemini-3.8-flash` (S10). So "the local environment base agent" and "no model at all" both mean `model: inherit`.
- **In the Genesis Kernel**, Rodin's swarm is already model-free: `RodinSupervisor.agent_registry` is a dictionary of four role labels (ANALYST, RESEARCH, DBA, DEVOPS) with no model attached (`orchestration/rodin_supervisor.py:50-55`). Today that dispatch is simulated: it routes on a fixed mock vector `[0.1] * 768` with an empty candidate list and always picks ANALYST (`:80-107`). See Section 4.

## 4. Binding to Integra

| Integra element | Today (verified) | Designation after this brief |
|:--|:--|:--|
| Rodin Route Retrieval **orchestrator core** | `models.yml` `rodin_retrieval: gemini-3.8-flash` (live router, 19:26 probe) | **Gemini 3.8 → `gemini-3.8-flash`.** Already correct; no change to `models.yml`. |
| Rodin **sub-agents (swarm)** | Model-free labels in `rodin_supervisor.py`; dispatch is simulated | **No Gemini model.** Secondary extensions of Rodin. |
| SKILL.md §15 registry | Lists `rodin_retrieval` as `gemini-3.6-flash` | Stale. 3.6 Flash retires on the Agent Platform **2026-11-19**. Correct to 3.8 (part of the pending 10/07 learning proposal, item 6). |
| SKILL.md §8.5.1 SWDS table | "Rodin (Flash)" in Phase 2 | Relabel "Rodin core (3.8)". Sub-agents carry no model label. |
| Rodin embeddings | Default `text-embedding-004`; `RODIN_EMBED_MODEL` unset | Served on the platform until **2027-04-01**. Move to `gemini-embedding-2` at 768 dimensions (Google's recommended size, S6; $0.20 per million text tokens, S14) and re-embed before then (ADR-005). |
| Rodin core thinking settings | Router: `thinking_budget: model_default` | For 3.8 Flash use **`thinking_level`** (`low` for routing, `medium` default); `minimal` returns an error (S4). Never send `temperature`, `top_p` or `top_k`: deprecated since July 21, 2026, and rejected outright by the Antigravity agent (S3, S5, S10). The kernel currently sends none of them (checked `core/api_clients.py`). |

### How to realise "no model" sub-agents in each environment

1. **Genesis Kernel (recommended now).** Implement each sub-agent as a deterministic retrieval function owned by Rodin, with no model call: fetch Hoard node(s) by ID, expand KNN neighbours, run full-text search, look up ledger rows, check staleness. Rodin's 3.8 core is the only model in the loop. This costs no tokens, has no deprecation exposure, and fits ADR-002 (every fetch becomes a ledger row). It also fixes the simulated dispatch by replacing the mock vector with the real query embedding.
2. **Antigravity IDE (when needed).** Define each sub-agent as `.agents/agents/rodin-<role>.md` in the workspace, with this front matter:
   ```yaml
   name: rodin-research
   description: Rodin swarm extension. Fetches and returns the Hoard nodes Rodin names; never synthesises.
   subagent: true
   mainAgent: false
   model: inherit
   tools: [view_file, grep_search, find_by_name]
   commandExecutionPolicy: sandbox
   ```
   Label sub-agents by role, never by model. If they are ever created as Gemini API managed agents, IDs **must not start** with `gemini-`, `google-` or `antigravity-` (S11 reserves them).
3. **Gemini CLI.** Omit `model` (it defaults to `inherit`, S15) and give an explicit `tools` list (otherwise it inherits all tools).

### Nesting is one level deep everywhere

Gemini CLI sub-agents cannot call sub-agents (S15). Gemini API managed agents state "No subagent nesting: subagent delegation is not yet supported" (S11). Antigravity 2.0 lets agents message each other and runs its own three-tier `/boost` orchestrator, but custom sub-agents are invoked by a parent (S13). The design that works on all three is the one the Architect described: **Rodin is the commander; the swarm sits one level below it.** The orchestrator must be the main agent, or the kernel itself, never a sub-agent.

## 5. Synthesis — recommendation

1. **Rodin orchestrator core = Gemini 3.8, model string `gemini-3.8-flash`.** It is the only 3.8 text model, stable since September 2, 2026, with no shutdown announced on either platform. Use `thinking_level` `low` for routing and `medium` for synthesis.
2. **Rodin sub-agents = no model.** They are secondary extensions of Rodin: deterministic functions in the kernel now, `model: inherit` sub-agents in Antigravity when needed. Write them in documents as "no model (inherits Rodin core)".
3. **Retire "3.7" as an option.** It was deprecated October 8, 2026, is routed to 3.8 Flash on the Developer API, retires January 28, 2027 on the Agent Platform, and cannot be selected in Antigravity or managed agents.
4. ~~If a sub-agent ever needs its own model, the documented choice is `gemini-3.5-flash-lite`.~~ **Withdrawn by the Architect's ruling:** 3.5, 3.6 and 3.7 models are removed. Rodin's agent identity is the Antigravity agent on `gemini-3.8-flash`; sub-agents inherit it.
5. **Correct the stale labels** in SKILL.md §15 and §8.5.1 through the pending learning proposal. Nothing in `models.yml` needs to change for Rodin.

### Option scoring (CRA = W_y / C_c; values are judgement, not measurement)

| Option for Rodin sub-agents | W_y | C_c | CRA | Note |
|:--|:--|:--|:--|:--|
| No model: deterministic extensions (kernel) | 0.80 | 0.15 | 5.3 | No tokens, no deprecation risk, provable through the ledger |
| `model: inherit` (Antigravity) | 0.75 | 0.30 | 2.5 | Uses the base agent's model; no separate label to maintain |
| ~~`gemini-3.5-flash-lite` (own model)~~ | — | — | — | Removed (Architect ruling: no 3.5 / 3.6 / 3.7 models) |
| `gemini-3.7-flash` | 0.10 | 0.60 | 0.2 | Deprecated alias; retires 2027-01-28 on the platform |

## 6. Deprecation watch list for Integra (dates from S2 and S7)

| Date | Event | Integra exposure |
|:--|:--|:--|
| 2026-10-20 | Gemini 2.5 Pro, Flash and Flash-Lite retire on the Agent Platform | None (not used) |
| 2026-10-23 | `deep-research-pro-preview-12-2025` shuts down | None (Deep Research was rejected for the Cheshire Daemon) |
| 2026-11-19 | `gemini-3.6-flash` retires on the Agent Platform | Only the stale SKILL.md §15 label; the kernel runs 3.8 |
| 2027-01-01 | 3.8 Flash introductory price ends: $0.75 → $1.50 input, $3.75 → $7.50 output per million tokens (S5, S14) | Cost of Rodin core, Cheshire Kernel and Cheshire Protocol doubles |
| 2027-01-28 | `gemini-3.7-flash` retires on the Agent Platform | None once "3.7" is dropped |
| **2027-04-01** | **`text-embedding-004` retires on the Agent Platform** | **Rodin embeddings: migrate and re-embed before this date** |
| 2027-05-07 | `gemini-3.1-flash-lite` shuts down (Developer API) | None |
| Open | `gemini-3.1-pro-preview` is a preview with no date; previews can be deprecated with ≥ 2 weeks' notice | Y789 and Jean Grey: watch the release notes |
| 2028-05-14/20 | `gemini-embedding-001` | None if Rodin moves straight to `gemini-embedding-2` |

## 7. New code finding from this research

`POST /rodin/query` runs `RodinSupervisor.dispatch`, which evaluates Gate III on a fixed mock vector `[0.1] * 768` with an empty candidate list and always dispatches ANALYST (`orchestration/rodin_supervisor.py:78-107`). The "swarm conductor" route is therefore simulated end to end. It belongs on the blueprint's false-positive list and in ADR-005 / ADR-006 work.

## 8. Not done

- **Stage 6 (Hoard injection)** was not run. The kernel's own Daily Planet code can fabricate sources when a fetch fails (blueprint §5.10), and the Hoard's layout is still pending the cleanup decision. This brief lives in `docs/` instead. It can be added to the Hoard once ADR-013 is fixed.
- No live model or embedding call was made. The Agent Platform's April 1, 2027 date for `text-embedding-004` is documentary evidence; a single paid probe would confirm the model still answers today.
- No Integra file other than this brief, the master blueprint and the working plan was changed. SKILL.md and `models.yml` are untouched pending the Architect's approval.
