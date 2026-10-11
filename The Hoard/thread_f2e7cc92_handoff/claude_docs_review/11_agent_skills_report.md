# 11 — Using Agent Skills with the API: Report

## 0 Read receipt
- File: `docsplit/11_Using_Agent_Skills_with_the_API_388264d5e1a1.md`. Read in full: lines 1–4802 of 4802 (154,842 bytes), in 7 view passes.
- First heading: "Using Agent Skills with the API" (frontmatter title) / "## Quick links". Last heading: "## Next steps" (preceded by "## Data retention" and "## Audit logging"). Source marker: `Claudecode5Untitled-3.md lines 7491-12290`.
- Roughly 85% of the section is the same examples repeated across 9 languages (cURL, CLI, Python, TS, C#, Go, Java, PHP, Ruby). All prose was read.

## 1 DOC SAYS
**Skill structure**
- A bundle is a directory with a top-level `SKILL.md` that has `name` and `description` YAML frontmatter, plus any scripts or resources.
- `SKILL.md` must sit at the upload root (or at the top of a single enclosing folder).
- `name`: ≤64 chars, lowercase letters/numbers/hyphens only, no XML tags, must not contain the reserved words "anthropic" or "claude".
- `description`: ≤1024 chars, non-empty, no XML tags.
- `display_name` is optional, ≤255 chars, not unique. If omitted it comes from `name`.

**Endpoints**
- `POST /v1/skills` (multipart `files[]`, zip or individual files; Python `files_from_dir`; CLI `ant apply <dir>`).
- `GET /v1/skills` (`?source=custom`; `limit` 1–1000, default 20; response `{data, next_page}`).
- `GET /v1/skills/{id}`. `DELETE /v1/skills/{id}` deletes ALL versions.
- `POST /v1/skills/{id}/versions`. `GET /v1/skills/{id}/versions/latest`.
- The SDK uses `client.skills.*` and `client.skills.versions.create`.

**Versioning**
- Custom skills get IDs like `skill_01…`. Versions are `skver_01…` or `"latest"`.
- Anthropic skills use date versions such as `20251013`, or `latest`.
- A new version is a full snapshot, not a delta. Omitted files are dropped, and `name` must match.
- Production: pin a version ID. With `latest`, anyone in the workspace who uploads a new version changes production behaviour immediately. Quote version IDs as strings.
- Deleting the only remaining version returns a 400.

**Container and code-exec dependency**
- Skills only run through the code execution tool: `tools:[{"type":"code_execution_20250825","name":"code_execution"}]`.
- Request shape: `container:{skills:[{type:"anthropic"|"custom", skill_id, version}]}`.
- Max **20 skills per request**. Max upload **30 MB uncompressed**.
- To reuse a container, pass `container.id` (the response has `container.id` and `expires_at`).
- `pause_turn` stop reason: send the content back as an assistant turn in the same container. The examples loop up to 10 times.
- Generated files come back as a `file_id` inside `bash_code_execution_tool_result` → `bash_code_execution_result` blocks. Download them with the Files API.
- Inputs go in through Files API plus container upload blocks.

**Environment**
- **No network access.** No runtime package installation.
- A fresh container is created unless an ID is passed.

**Beta headers**
- The Skills API is **out of beta and needs no beta header**. The examples send only `anthropic-version: 2023-06-01`.
- `skills-2025-10-02` is still accepted but returns the old shapes: `display_title`, epoch-µs `latest_version`, string `source`, oldest-first version lists, and delete returns 400 while any version exists.
- From Python SDK **1.2.0** (TS 0.122.0, Go 1.68.0), `client.beta.skills` no longer sends the header.

**Prebuilt skills**
- `pptx`, `xlsx`, `docx`, `pdf` (type `anthropic`). The catalog source value is `anthropic_example`.

**Progressive disclosure**
- Name and description go into the system prompt.
- Files are copied to `/skills/{skill-name}/` (the directory uses the `name`, not the ID).
- The full instructions load only when relevant.

**Other**
- Custom skills are **workspace-scoped**: any key for the workspace can read, invoke or delete them. The Default Workspace is reachable by all service accounts and API-enabled users. Up to 100 workspaces per org.
- Changing the skills list or its order breaks the prompt cache. `latest` can also invalidate it when the description changes.
- Skill errors are 400 `BadRequestError` with "skill" in the message.
- **Not covered by ZDR.** Audit logging only works if the Compliance API is enabled first; nothing done before that can be recovered.

## 2 MY INFERENCE FOR INTEGRA
- **Porting `integra-protocol` SKILL.md** (`~/.gemini/config/skills/integra-protocol/`):
  - The name `integra-protocol` passes the rules.
  - The description must be confirmed ≤1024 chars with no XML tags. I did not measure it.
  - The body ("When this skill is activated, you ARE Integra…") is persona text. It works as a skill, but only loads on relevance, so it is not always-on. That is a poor fit for an "always-on identity": the identity core belongs in the `system` prompt or a cached prefix. Skills suit procedural playbooks, e.g. Proof-of-Sleep ledger rendering, Rodin node schema, Hoard JSON format, report templates.
- **Identity matrix**:
  - Skills are Claude-only. Only `nexus_right` (opus-5-5) and `shiva_orchestrator` (sonnet-5-5) could use them.
  - The Gemini clients (y789, jean_grey, rodin, cheshire_*) cannot. Shared protocol text must stay model-agnostic files on disk; the API skill would be a thin mirror.
  - Keep one skill list in a fixed order per role so the cache holds.
- **Cheshire Daemon**: the "local only, no internet" rule happens to match the container (no network). But the container also cannot see The Hoard, Rodin or SQLite unless files are uploaded through the Files API, and it is a remote Anthropic sandbox. So it is not local and not ZDR. Using skills for Cheshire would break its "local only" constraint, so do not use API skills for Cheshire. The brief also proposes Gemini 3.1 Pro for Cheshire, which cannot use them anyway.
- **Cost and latency**: every skill request adds the code execution tool and container work. `pause_turn` loops add more calls. Heimdall token/$ tracking must count every continuation call.
- **Anti-fabrication**: container outputs are real execution artefacts (`file_id`s). The Proof-of-Sleep ledger could log `container.id`, `file_id` and `skver_` per step.

## 3 Contradictions with current wiring
1. **SDK version**: the brief pins `anthropic==1.5.0`, and the doc says Python SDK ≥1.2.0 stops sending the beta header from `client.beta.skills`. So 1.5.0 should support the non-beta `client.skills` (unverified — needs a probe). Any older code or docs using `skills-2025-10-02`, `display_title` or `latest_version` will get beta shapes.
2. **Response parsing**: `integra-homebase/core/api_clients.py` (lines 121–122) already avoids `content[0].text` for thinking blocks. With code execution, content also holds `server_tool_use` and `bash_code_execution_tool_result` blocks, and `stop_reason` can be `pause_turn`. Grep found no `pause_turn`, `container` or `code_execution` handling in the file. Turning skills on without these changes would truncate turns.
3. Model IDs in the doc (`claude-opus-5-5`) match `models.yml`. No conflict.
4. **"Local only" / privacy**: skills run remotely, and ZDR does not cover them. This conflicts with the Cheshire and Hoard locality rules.
5. **Cache**: the doc says changing the skills list or order breaks the prompt cache. If the ModelRouter builds skill lists per request, it would break caching and work against the token-overuse goal.

## 4 Concrete recommended actions (ranked)
1. **(S)** Probe `anthropic==1.5.0`: `client.skills.list()` with no beta header. Log the result to the ledger, and record the real response rather than assuming it works.
2. **(S)** Keep the identity and constitution in the `system` prompt or cached prefix, not in API skills. Skills only load on relevance.
3. **(M)** If skills are adopted for Claude roles: add `pause_turn` continuation (bounded, e.g. 10), handling for every block type, and Heimdall cost accounting for each continuation call in `NexusClient`/`ShivaClient`.
4. **(M)** Make 1–3 procedural custom skills (e.g. `swds-ledger-report`, `hoard-node-schema`) with names ≤64 chars and descriptions ≤1024. Upload with `files_from_dir`, **pin `skver_` IDs** in `models.yml`, and use a dedicated workspace, not Default.
5. **(S)** Exclude Cheshire Daemon and any Hoard-private data from API skills (no ZDR, remote sandbox).
6. **(L)** Optional: use the container as a verifiable compute sandbox for SWDS report rendering. Log `container.id`, `file_id`s and hashes per step. Turn on the Compliance API first if an audit trail is wanted.
