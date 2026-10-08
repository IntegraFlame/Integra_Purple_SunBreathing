# External Storage: Tier 1 Research and Daily Planet Findings

**2026-10-08 00:17 CDT | 2026-10-08T05:17Z**. Research was done by the External Storage Researcher subagent; I verified the local items myself.
Method: multiple sources, official docs preferred, every source dated, **UNVERIFIED** marked where it applies, and each option scored by CRA ($W_y / C_c$, judgement-based).

> [!CAUTION]
> **P0 finding: the embedding model may be dead.**
> - Google's Gemini API deprecation page lists `text-embedding-004` as **shut down 2026-01-14**. The replacement is `gemini-embedding-2`, which supports 768 dimensions.
> - **Verified locally:** `core/api_clients.py` L680 defaults to `text-embedding-004`, and `RODIN_EMBED_MODEL` is **not set** in `integra-homebase\.env`. Rodin is therefore using 004.
> - **Conflict to settle:** yesterday's self-test reported embeddings working. That call goes through Vertex AI Express (`main.py` L483), and Vertex's own schedule for 004 was not checked. A single direct embed probe will decide it.
> - **If 004 is dead or retiring, every vector must be re-embedded.** Vectors from different models cannot be mixed.

## Verdict (best fit for one developer, local-first, low budget)
1. **Live memory:** one SQLite database (`memory.db`) in a non-synced folder such as `C:\IntegraData\`. It holds:
   - nodes
   - edges (the graph map)
   - vectors, via `sqlite-vec` at 768 dimensions with the model name stored per vector
   - FTS5 keyword search
   - an append-only, hash-chained **ledger** (this is the Proof-of-Sleep substrate)
2. **Cold archive** for superseded files: a GCS bucket with versioning and soft delete, using a lifecycle rule of Standard → Coldline at 30 days → Archive at 180 days. Upload files as **bundles**, because Autoclass never moves objects under 128 KiB.
3. **Cross-thread memory:** the Genesis Kernel hosts an **MCP memory server** with these tools:
   - `search_memory`
   - `get_node`
   - `neighbors`
   - `write_node`
   - `write_handoff`
   - `get_kernel_card`

   It serves Antigravity and Claude Desktop locally. A Claude Project carries a small **kernel card** of 2–3k tokens.
4. **Optional later:**
   - a Neo4j Desktop graph viewer, rebuilt from `memory.db` (never the source of truth)
   - BigQuery analytics within the free tier
   - Cloud SQL, only if an always-on remote store is needed
5. **Estimated cost:** about $0–5/month for steps 1–3.

## Claude app memory (late 2026; Anthropic help center, 2026-09-30)
- **Memory:** saved as individual topics during chat, and **scoped per Project**. Nothing crosses between projects. Reset deletes all of it.
- **Chat search:** paid plans only. Scope is either all non-project chats or one project's chats; it does not search across both.
- **Project knowledge:** loaded **in full until near the context limit, then switches automatically to RAG**, where only retrieved chunks reach the model. This is a plausible mechanical cause of the "skimmed handoff" problem. Keep core docs small enough to always load in full.
- **Custom connectors (remote MCP):** these connect **from Anthropic's cloud**, so the server must be internet-reachable. Local MCP in `claude_desktop_config.json` is Desktop-only.
- **Local-connector secrets:** Claude docs say connector environment variables are stored unencrypted.
- **What persists across threads:** memory topics, project knowledge, searchable past chats (paid plans), and anything exposed through MCP. The full conversation context does **not** carry over, so **owning the memory store and exposing it through MCP is the reliable path.**

## CRA ranking

| Option | Best role | CRA | Key fact |
|:--|:--|:--|:--|
| GCS bucket | Cold archive | **8.0** | Archive class is $0.0012/GB-month with a 365-day minimum |
| OneDrive | Human docs and snapshots only | 7.0 | Unsafe for live databases |
| SQLite + sqlite-vec + FTS5 | Live nodes, vectors, graph, ledger | **5.67** | Free and private; sqlite-vec is pre-v1, so pin the version |
| Claude Project + MCP memory | Cross-thread memory | **3.6** | Local MCP keeps it private |
| Neo4j Aura Free | Graph | 2.0 | Deleted after 30 days of inactivity; data is cloud-hosted |
| Postgres + pgvector (Docker) | Upgrade path | 1.9 | pgvector 0.8.6 (2026-07-29) |
| Docker | Host for local services | 1.83 | **CLI 29.8.0 installed** (verified). Daemon status not checked |
| Neo4j Desktop | Graph viewer | 1.75 | Best visual explorer |
| LangGraph store | Agent memory | 1.57 | Only worthwhile if we build LangGraph agents |
| BigQuery | Analytics | 1.5 | 10 GB storage and 1 TiB queries free per month |
| Cloud SQL + pgvector | Remote always-on store | 1.33 | About $8–10/month for micro (estimate) |
| Sharding | — | 0.83 | 305 shards is tiny; consolidate instead |
| Redis 8 | Cache | 0.75 | AGPLv3 licence; not needed |
| LangChain | Glue | 0.75 | Heavy abstraction; direct SDK calls are simpler |
| GraphRAG | Graph | 0.58 | Repo is **in maintenance mode** |
| Pub/Sub | Event bus | 0.57 | **31-day maximum retention**, so it is not a ledger |
| AlloyDB | Vector database | 0.47 | About $227/month minimum |
| Node.js | — | 0.33 | Not needed; Python MCP works |

## OneDrive and SQLite: unsafe for live databases
- SQLite's documentation warns that copy or backup tools and synced filesystems can corrupt a database mid-transaction.
- In WAL mode, the `.db`, `-wal` and `-shm` files must stay consistent with each other, but OneDrive uploads them independently.
- **Fix:** keep live databases on an unsynced path, snapshot them with `VACUUM INTO`, and sync only the snapshots.
- The same applies to `.venv`, `.pytest_cache` and the kernel log, which is already locked and has mixed encoding.

## Phased adoption (proposal; each phase needs your approval)
| Phase | Work |
|:--|:--|
| P0 | Probe the embed model and fix it. Full backup. Move live `.db` files out of OneDrive. Run `PRAGMA integrity_check`. Move keys out of synced `.env` files (Credential Manager or Secret Manager). |
| P1 | Create the `memory.db` schema. **Dry-run** ingestion: hash every file, deduplicate `The Hoard` against `The_Hoard`, write a manifest, move nothing. |
| P2 | Re-embed with `gemini-embedding-2` at 768 dimensions (about $4 one-off, estimate). Build edges. |
| P3 | GCS archive bucket. Move superseded files as hash-verified bundles; keep a 30-day local quarantine. |
| P4 | MCP memory server, Claude Project kernel card, start- and end-of-thread handoff routine. |
| P5 | Optional: Neo4j viewer, BigQuery. |

**This is the "external storage" step that the environment-ingestion plan was missing.** P1 plus P3 give that plan a safe destination.

## UNVERIFIED
- Whether 004 still works through Vertex Express.
- Whether the Docker daemon is running.
- The list of `.db` files under OneDrive.
- The Claude Projects per-file limit, and which plans get Desktop extensions.
- Cloud SQL dedicated-instance pricing.

The researcher's full report and complete source list (with dates) are recorded in this thread. Key sources: support.claude.com articles 11817273, 11473015 and 11175166; the Gemini API deprecations page; sqlite.org/howtocorrupt.html; GCS storage-classes and Autoclass docs; the pgvector changelog; the microsoft/graphrag README; Pub/Sub quotas.
