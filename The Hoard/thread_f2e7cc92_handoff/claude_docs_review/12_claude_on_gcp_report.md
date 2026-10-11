# Report 12 — Claude on Google Cloud (Agent Platform / Vertex AI)

## 0 Read receipt
- File: `docsplit/12_Claude_on_Google_Cloud_493913f35e33.md`. Read all 1002 lines (35,693 bytes) in two view_file calls (1–800, 800–1002).
- First heading: `title: Claude on Google Cloud` / `## Install an SDK for accessing Agent Platform`. Last heading: `## Additional resources`.
- Source URL: platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai.
- Note: written to the subagent's own artifact dir because the tool blocked writes to the parent's scratch dir.

## 1 DOC SAYS
- **Request format differences (L8–11):** `model` goes in the endpoint URL, not the body. `anthropic_version` goes in the body, and its value must be `"vertex-2023-10-16"`. The SDKs handle both of these automatically.
- **SDK install:** Python `pip install -U "anthropic[vertex]"`; TS `@anthropic-ai/vertex-sdk`; C# `Anthropic.Vertex`; Go `anthropic-sdk-go/vertex`; Java `anthropic-java-vertex:2.69.0`. The doc gives no minimum Python SDK version. "The ant CLI does not support Agent Platform."
- **Python client:** `from anthropic import AnthropicVertex; AnthropicVertex(project_id=..., region="global")`, then the usual `client.messages.create(model="claude-opus-5-5", ...)`.
- **Auth:** "Before running requests you might need to run `gcloud auth application-default login`." Every example uses Google credentials: cURL sends `Authorization: Bearer $(gcloud auth print-access-token)`, Go uses `vertex.WithGoogleAuth`, Java uses `GoogleCredentials.getApplicationDefault()`, TS uses the "standard `google-auth-library` flow". **No example uses an API key, and the doc never mentions Express mode.**
- **Endpoints (L378–414):**
  - Global: `https://aiplatform.googleapis.com/v1/projects/{P}/locations/global/publishers/anthropic/models/{M}:rawPredict`. This is the recommended option, has no price premium, and is pay-as-you-go only.
  - Multi-region: `us` or `eu`, via `aiplatform.{us|eu}.rep.googleapis.com`. Adds a 10% premium; PAYG only.
  - Regional (e.g. `us-east5`, `europe-west1`, via `{LOC}-aiplatform.googleapis.com`): adds a 10% premium and is required for provisioned throughput. **"Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints."**
  - The 10% premium applies to Sonnet 4.5 and later models. Older models keep their existing pricing.
- **Model ID format:** 5.x and 4.6+ models have no `@date` suffix: `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`, `claude-opus-5`, `claude-sonnet-5`, `claude-fable-5-1`, `claude-mythos-5-1` (limited availability). Older models keep the suffix, e.g. `claude-opus-4-5@20251101`, `claude-haiku-4-5@20251001`. Google sets lifecycle dates on this platform, and they can differ from the Claude API schedule.
- **Supported:** Messages API, prompt caching, thinking, tool use (Bash, browser use, computer use, memory, text editor), web search tool, citations, structured outputs.
- **NOT supported (L363–370):**
  - URL image/document sources and the Files API
  - Code execution, web fetch, advisor
  - Agent Skills, MCP connector, programmatic tool calling
  - **Message Batches, Models, Admin, Compliance, Usage and Cost APIs**
  - Claude Managed Agents
  - **Server-side `fallbacks`** (use client-side fallback instead)
- **Limits:** Opus 5.5, Sonnet 5.5, Haiku 5.5 and the other listed models have a 1M-token context window; deprecated Sonnet 4.5 and 4 have 200k. Request payloads are capped at **30 MB**.
- **Quotas:** the doc gives no numbers and points to Google docs. Model availability varies by region (check Model Garden).
- **Pricing:** the doc gives no per-token prices. It links to the Google Generative AI pricing page and Anthropic's "cloud platform pricing" page. The only pricing fact in the doc is the 10% regional/multi-region premium.
- **Data / logging:** data retention is governed by Google Cloud. Request-response logging is available, and Anthropic recommends keeping at least a 30-day rolling log.

## 2 MY INFERENCE FOR INTEGRA
- **Nexus/Shiva through the existing GCP project: feasible.** Both IDs in use (`claude-opus-5-5`, `claude-sonnet-5-5`) appear in the table exactly as written, so `models.yml` IDs would not change. Claude spend would be billed to the same GCP billing account as Gemini, and Claude quotas become per-project GCP quotas. You must enable the Claude models in Model Garden first (the doc assumes this setup is done). Use `region="global"`: the regional endpoints don't serve 5.x models.
- **The Vertex Express API key will almost certainly NOT work for Claude.** The doc only shows OAuth bearer / ADC flows. My understanding is that Express mode covers Google's first-party Gemini models, not partner models, but this is unverified. Test it with one cURL call using `?key=` before relying on that. Plan for ADC (user `gcloud auth application-default login`) or a service account with the Vertex AI User role.
- **Impact on the 401 key-rotation problem:**
  - Moving Claude to ADC removes the Anthropic API key from the system entirely, so there is nothing to rotate. The Google auth libraries refresh short-lived tokens automatically.
  - New failure modes:
    - The ADC file is per-user (`%APPDATA%\gcloud\application_default_credentials.json`). The Task Scheduler account must be the same user, or you need to set `GOOGLE_APPLICATION_CREDENTIALS`.
    - User refresh tokens can be revoked or need reauth under org policy.
    - A service account key is a long-lived secret and becomes a new thing to rotate. A local daemon has no metadata server, so plan around that.
  - Overall, one Google identity would cover Claude and could cover Gemini too, replacing two key types. That shrinks the 401 surface.
- **Heimdall cost tracking:** the Usage and Cost API is not available on Vertex. Count tokens from each response's `usage` fields and log them to the ledger, and/or use GCP Billing export to BigQuery. Batches aren't available either, so Anthropic's batch discount can't be used for SWDS bulk jobs on this route.

## 3 Contradictions with current wiring
1. **Auth:** the brief says the Gemini key is a Vertex Express key. Reusing it for Claude contradicts the doc's auth model (bearer/ADC only).
2. **Client class:** the current code presumably uses `anthropic.Anthropic(api_key=...)`. Vertex needs `AnthropicVertex` plus the `[vertex]` extra (google-auth). The pinned `anthropic==1.5.0` was installed without that extra, as far as the brief says. Check whether `AnthropicVertex` imports.
3. **Effort / adaptive thinking:** the doc lists "Thinking" as supported but never mentions `output_config.effort` or `thinking.type:"adaptive"` on Vertex. Treat parity for those as **unverified** until probed.
4. **Unsupported features:** any planned use of the `fallbacks` param, Message Batches, the Usage/Cost Admin API, Files API, MCP connector, or Agent Skills on the Claude path would fail on Vertex.
5. **Region:** if any config defaults Claude to `us-central1`/`us-east5`, 5.x models fail there. It must be `global` (or `us`/`eu` at +10%).
6. **Response parsing:** the doc's own PHP and Ruby regional examples use `content[0].text` / `content.first.text`. That is the same hazard Integra already avoids, so keep the join-text-blocks logic.

## 4 Concrete recommended actions (ranked)
1. **(S)** Probe cost and auth. Make one 100-token `rawPredict` call to `claude-sonnet-5-5` at `locations/global` with an ADC bearer token, and one attempt with the Express key, to settle Express support empirically. Record the HTTP codes in the ledger.
2. **(S)** Check `python -c "from anthropic import AnthropicVertex"` in the kernel venv. If it fails, run `pip install "anthropic[vertex]==1.5.0"` (keeping the pin) and confirm the version.
3. **(M)** Add a `provider: vertex|anthropic` switch per model in `models.yml`, and have `api_clients.py` build `AnthropicVertex(project_id, region="global")`. Keep the direct Anthropic API as a client-side fallback, since server-side `fallbacks` isn't supported.
4. **(S)** Probe parity: send `thinking:{type:"adaptive"}` plus `output_config.effort` to Opus 5.5 on Vertex and log whether the request succeeds or errors.
5. **(M)** Pick the identity: a dedicated service account with least-privilege Vertex AI User, with `GOOGLE_APPLICATION_CREDENTIALS` set in the scheduled task environment. Heimdall should check token-mint health, not key validity.
6. **(M)** Point Heimdall cost tracking at per-response `usage` plus GCP Billing export to BigQuery, and enable request-response logging with 30-day retention.
7. **(L)** Optionally move Gemini off the Express key onto the same ADC identity, which fully unifies auth, quotas and billing.
