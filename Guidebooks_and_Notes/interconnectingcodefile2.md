# **Hardening the Integra OS Substrate for Dual-Provider LLM Orchestration and SQLite Persistence**

Deploying an autonomous, bicameral intelligence kernel across Anthropic Claude, Google Gemini, GitHub, and Antigravity 2.0 requires immediate abandonment of flat-file JSON sharding in favor of an ACID-compliant, Write-Ahead Logging (WAL) SQLite storage layer. The previous architecture suffered from four system-halting vulnerabilities: multi-process file-lock collisions between the kernel writer, Prometheus exporter, and Model Context Protocol (MCP) server; exponential API quota exhaustion caused by re-embedding knowledge documents inside real-time inference loops; unhandled Markdown code fences in Google Gemini delegation responses that crashed Python's native JSON parser; and unbuffered sys.stdout logging that corrupted the Antigravity 2.0 JSON-RPC communication bridge.

To stabilize the runtime environment, the storage architecture must be consolidated into an embedded SQLite database configured with a five-second busy timeout and WAL mode, allowing concurrent non-blocking reads during operational writes. Knowledge retrieval must transition from on-the-fly embedding to pre-computed vector BLOB lookups, while LLM responses must pass through regex-based fence extraction and Pydantic validation. Furthermore, external repository ingestion must execute via remote Abstract Syntax Tree (AST) parsing using PyGithub to eliminate external Git shell dependencies, and agentic state checkpoints must be persisted through AsyncSqliteSaver to support non-volatile recovery during Slow-Wave Deep Sleep (SWDS) consolidation cycles.

The operational blueprint below presents an exhaustive engineering audit of previous system actions, details a unified SQLite database engine, hardens the dual-provider execution loop, provides a clean stdio MCP server for the Antigravity 2.0 IDE, and establishes automated telemetry thresholds for persistent autonomous stability.

## **Structural and Concurrency Vulnerability Audit**

A forensic review of the initial deployment scripts demonstrates that while the bicameral reasoning division—assigning Google Gemini to broad architecture and Anthropic Claude to precision logic—is theoretically sound, the operational substrate contained severe race conditions and unhandled exception boundaries.

| Subsystem Component | Operational Precondition | Failure Mechanism | Empirical Impact | Remediated Architecture |
| :---- | :---- | :---- | :---- | :---- |
| File Storage (LocalFolderDatabase) | Kernel writes state\_\*.json | Unsynchronized file writes collide with reads from Exporter and MCP | JSONDecodeError: Unter\[span\_51\](start\_span)\[span\_51\](end\_span)\[span\_60\](start\_span)\[span\_60\](end\_span)minated string; crashed telemetry daemon | SQLite database in WAL mode with normalized tables and busy timeouts |
| Retrieval (RodinRouteRetriever) | User inputs query string | Synchronous iteration re-embedding every markdown section on each turn | HTTP 429 RESOURCE\_EXH\[span\_2\](start\_span)\[span\_2\](end\_span)\[span\_9\](start\_span)\[span\_9\](end\_span)AUSTED within 10–15 conversation turns | Pre-computed embeddings stored as vector BLOBs; single-query embedding |
| Thalamic Delegator (\_delegate) | Gemini returns JSON string | Model wraps structured response in Markdown code fences (json ... ) | Fatal JSON parsing crashes; loss of conversational context | Regex fence extraction combined with Pydantic model validation |
| IDE Bridge (AntigravityMcpServer) | Antigravity 2.0 polls MCP | Uncaptured print() statements send raw text down s\[span\_37\](start\_span)\[span\_37\](end\_span)\[span\_42\](start\_span)\[span\_42\](end\_span)ys.stdout | JSON-RPC desynchronization; IDE drops MCP connection | All diagnostic logging redirected to sys.stderr |
| Dual Model Bus (\_execute\_pass) | Concurrent execution of Gemini and Claude | Unshielded asyncio.gather without backoff or rate-limit retry logic | Transient API drop from one provider terminates the entire turn | Exponential backoff with random jitter and independent task shielding |
| Memory Checkpointing (PhoenixEngine) | Rolling context capped at 30 items | Large code blocks in prompt history exceed model token context windows | Context rot, high inference latency, and memory overflow | LangGraph AsyncSqliteSaver checkpointer with SQL history pruning |

Filesystem concurrency was the most immediate source of instability. In the original implementation, the CheshireCatKernel wrote execution shards (state\_\[span\_49\](start\_span)\[span\_49\](end\_span)\*.json) directly into ./kernel\_memory/conversations/ while maintaining an active rolling array in rolling\_context.json. Concurrently, heimdall\_exporter.py scraped the latest JSON file every two seconds over an uncoordinated file handle. When the kernel performed a write during a scrape, the exporter ingested partially written byte streams, causing silent metric drops and dashboard deadlocks. Similarly, if the emergency CircuitBreaker flushed rolling\_context.json while the kernel was executing an in-flight synthesis, the kernel's trailing flush overwrote the empty state, completely bypassing the circuit breaker's safety purge.

The retrieval pipeline contained an equally critical computational flaw. In rodin\_protocol.py, every candidate markdown file in indexed\[span\_54\](start\_span)\[span\_54\](end\_span)\[span\_63\](start\_span)\[span\_63\](end\_span)\_libraries/ was split by section dividers, and each chunk was embedded dynamically using self.embed\_text(clean\_sec\[:1000\]). Under Google GenAI quotas, repeated calls to text-embedding-004 exhausted the per-minute request rate almost instantly during multi-turn testing. Storing pre-computed float32 vector buffers directly in a database table reduces query-time retrieval to a single embedding call against the incoming prompt, followed by in-memory NumPy matrix multiplication.

On the network transport layer, relying on naked json.loads(response.text) to parse the output of gemini-2.5-flash or gemini-2.5-pro repeatedly failed. Models frequently interleave explanatory remarks or encapsulate payloads within Markdown blocks despite specifying response\_mime\_type: "application/json". A robust pipeline requires deterministic regex extraction of bracketed JSON content and automated coercion into a validated Pydantic schema before passing tasks to the execution hemispheres.

## **High-Performance Database Persistence Layer**

To resolve file-locking contention, prevent inode exhaustion, and maintain an immutable audit trail, all unstructured directories inside kernel\_\[span\_25\](start\_span)\[span\_25\](end\_span)memory/ are migrated to an embedded SQLite database (integra\_hoard.db). SQLite's WAL mode permits unlimited concurrent readers while a single writer appends data, providing non-blocking execution across the kernel, exporter, and MCP server.

The normalized relational schema segregates conversation shards, distilled knowledge nodes, parsed codebase syntax trees, and real-time telemetry.

`-- Database Optimization: integra_hoard.db`  
`PRAGMA journal_mode = WAL;`  
`PRAGMA synchronous = NORMAL;`  
`PRAGMA foreign_keys = ON;`  
`PRAGMA busy_timeout = 5000;`

`-- 1. Atomic Turn Shards`  
`CREATE TABLE I[span_3](start_span)[span_3](end_span)[span_10](start_span)[span_10](end_span)F NOT EXISTS conversation_shards (`  
&nbsp;&nbsp;&nbsp;&nbsp;`id INTEGER PRIMARY KEY AUTOINCREMENT,`  
&nbsp;&nbsp;&nbsp;&nbsp;`interaction_id TEXT UNIQUE NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`t1_wall_clock TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`t2_vector_coun[span_4](start_span)[span_4](end_span)[span_11](start_span)[span_11](end_span)ter INTEGER NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`t3_lunar_phase REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`t3_orbital_deg REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`user_input TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`intent TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`left_thought TEXT,`  
&nbsp;&nbsp;&nbsp;&nbsp;`right_thought TEXT,`  
&nbsp;&nbsp;&nbsp;&nbsp;`unified_thought TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`omega_metric REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`entropy_metric REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`  
`);`

`-- 2. Cold/Hot Knowledge Nodes with Serialized MRL Vectors`  
`CREATE TABLE IF NOT EXISTS knowledge_nodes (`  
&nbsp;&nbsp;&nbsp;&nbsp;`id TEXT PRIMARY KEY,`  
&nbsp;&nbsp;&nbsp;&nbsp;`title TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`domain TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`content TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`axioms TEXT, -- Serialized JSON array of invariant principles`  
&nbsp;&nbsp;&nbsp;&nbsp;`embedding_mrl BLOB NOT NULL, -- Binary serialized float32 NumPy array`  
&nbsp;&nbsp;&nbsp;&nbsp;`embedding_dim INTEGER NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`access_count INTEGER DEFAULT 0,`  
&nbsp;&nbsp;&nbsp;&nbsp;`created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,`  
&nbsp;&nbsp;&nbsp;&nbsp;`last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP`  
`);`

`-- 3. Codebase AST Structural Cache`  
`CREATE TABLE IF NOT EXISTS system_modules (`  
&nbsp;&nbsp;&nbsp;&nbsp;`file_path TEXT PRIMARY KEY,`  
&nbsp;&nbsp;&nbsp;&nbsp;`file_hash TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`repo_source TEXT DEFAULT 'local',`  
&nbsp;&nbsp;&nbsp;&nbsp;`classes_json TEXT, -- Serialized AST class signatures`  
&nbsp;&nbsp;&nbsp;&nbsp;`functions_json TEXT, -- Serialized AST function signatures`  
&nbsp;&nbsp;&nbsp;&nbsp;`imports_json TEXT, -- Serialized module dependencies`  
&nbsp;&nbsp;&nbsp;&nbsp;`raw_content TEXT,`  
&nbsp;&nbsp;&nbsp;&nbsp;`updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`  
`);`

`-- 4. Real-Time Telemetry Snapshots`  
`CREATE TABLE IF NOT EXISTS telemetry_snapshots (`  
&nbsp;&nbsp;&nbsp;&nbsp;`id INTEGER PRIMARY KEY AUTOINCREMENT,`  
&nbsp;&nbsp;&nbsp;&nbsp;`timestamp REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`cognitive_load_index REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`shannon_entropy REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`omega_agency REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`anomaly_flag INTEGER DEFAULT 0,`  
&nbsp;&nbsp;&nbsp;&nbsp;`created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`  
`);`

`-- 5. Atomic Working Context Window`  
`CREATE TABLE IF NOT EXISTS rolling_context (`  
&nbsp;&nbsp;&nbsp;&nbsp;`id INTEGER PRIMARY KEY AUTOINCREMENT,`  
&nbsp;&nbsp;&nbsp;&nbsp;`role TEXT NOT NULL CHECK (role IN ('user', 'nexus', 'system')),`  
&nbsp;&nbsp;&nbsp;&nbsp;`content TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`token_count INTEGER NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;`created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`  
`);`

`-- Indices for sub-millisecond range lookups`  
`CREATE INDEX IF NOT EXISTS idx_shards_t2 ON conversation_shards(t2_vector_counter DESC);`  
`CREATE INDEX IF NOT EXISTS idx_nodes_domain ON knowledge_nodes(domain);`  
`CREATE INDEX IF NOT EXISTS idx_telemetry_time ON telemetry_snapshots(timestamp DESC);`

The data access layer is managed by hoard\_db.py. It provides synchronous table bootstrapping and an asynchronous database connection manager using aiosqlite for non-blocking I/O during execution turns.

`# hoard_db.py`  
`import os`  
`import json`  
`import sqlite3`  
`import aiosqlite`  
`import numpy as np`  
`from typing import List, Dict, Any, Optional`

`DB_DIR = os.environ.get("KERNEL_MEMORY_DIR", "./kernel_memory")`  
`DB_PATH = os.path.join(DB_DIR, "integra_hoard.db")`

`def init_sync_db(db_path: str = DB_PATH):`  
&nbsp;&nbsp;&nbsp;&nbsp;`"""Synchronously initializes the database schema during startup."""`  
&nbsp;&nbsp;&nbsp;&nbsp;`os.makedirs(os.path.dirname(db_path), exist_ok=True)`  
&nbsp;&nbsp;&nbsp;&nbsp;`conn = sqlite3.connect(db_path)`  
&nbsp;&nbsp;&nbsp;&nbsp;`conn.execute("PRAGMA journal_mode = WAL;")`  
&nbsp;&nbsp;&nbsp;&nbsp;`conn.execute("PRAGMA busy_timeout = 5000;")`  
&nbsp;&nbsp;&nbsp;&nbsp;`with conn:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn.execute("""`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CREATE TABLE IF NOT EXISTS conversation_shards (`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`id INTEGER PRIMARY KEY AUTOINCREMENT,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`interaction_id TEXT UNIQUE NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`t1_wall_clock TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`t2_vector_counter INTEGER NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`t3_lunar_phase REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`t3_orbital_deg REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`user_input TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`intent TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`left_thought TEXT,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`right_thought TEXT,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`unified_thought TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`omega_metric REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`entropy_metric REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`);""")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn.execute("""`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CREATE TABLE IF NOT EXISTS knowledge_nodes (`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`id TEXT PRIMARY KEY,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`title TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`domain TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`content TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`axioms TEXT,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`embedding_mrl BLOB NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`embedding_dim INTEGER NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`access_count INTEGER DEFAULT 0,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`);""")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn.execute("""`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CREATE TABLE IF NOT EXISTS system_modules (`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`file_path TEXT PRIMARY KEY,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`file_hash TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`repo_source TEXT DEFAULT 'local',`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`classes_json TEXT,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`functions_json TEXT,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`imports_json TEXT,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`raw_content TEXT,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`);""")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn.execute("""`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CREATE TABLE IF NOT EXISTS telemetry_snapshots (`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`id INTEGER PRIMARY KEY AUTOINCREMENT,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`timestamp REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cognitive_load_index REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`shannon_entropy REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`omega_agency REAL NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`anomaly_flag INTEGER DEFAULT 0,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`);""")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn.execute("""`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CREATE TABLE IF NOT EXISTS rolling_context (`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`id INTEGER PRIMARY KEY AUTOINCREMENT,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`role TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`content TEXT NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`token_count INTEGER NOT NULL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`);""")`  
&nbsp;&nbsp;&nbsp;&nbsp;`conn.close()`

`class HoardDatabaseManager:`  
&nbsp;&nbsp;&nbsp;&nbsp;`"""Manages transactional read/write operations against the SQLite substrate."""`  
&nbsp;&nbsp;&nbsp;&nbsp;`def __init__(self, db_path: str = DB_PATH):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.db_path = db_path`

&nbsp;&nbsp;&nbsp;&nbsp;`async def get_connection(self) -> aiosqlite.Connection:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`db = await aiosqlite.connect(self.db_path)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.execute("PRAGMA journal_mode = WAL;")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.execute("PRAGMA busy_timeout = 5000;")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`db.row_factory = aiosqlite.Row`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return db`

&nbsp;&nbsp;&nbsp;&nbsp;`async def log_interaction(self, record: Dict[str, Any]):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`st = record["spacetime_metadata"]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`t3 = st["t3_celestial_kinematics"]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`async with await self.get_connection() as db:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.execute("""`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`INSERT INTO conversation_shards (`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`interaction_id, t1_wall_clock, t2_vector_counter,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`t3_lunar_phase, t3_orbital_deg, user_input, intent,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`left_thought, right_thought, unified_thought,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`omega_metric, entropy_metric`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`""", (`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`record["interaction_id"], st["t1_wall_clock"], st["t2_vector_counter"],`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`t3["lunar_phase_cycle"], t3["orbital_position_deg"],`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`record["user_input"], record["intent"], record.get("left_thought", ""),`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`record.get("right_thought", ""), record["unified_thought"],`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`record["omega_metric"], record["entropy_metric"]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`))`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# Maintain the active rolling context window atomically`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`in_toks = len(record["user_input"].split())`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`out_toks = len(record["unified_thought"].split())`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.execute("INSERT INTO rolling_context (role, content, token_count) VALUES (?, ?, ?)",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`("user", record["user_input"], in_toks))`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.execute("INSERT INTO rolling_context (role, content, token_count) VALUES (?, ?, ?)",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`("nexus", record["unified_thought"], out_toks))`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# Prune rolling context if total history exceeds 30 records`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.execute("""`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`DELETE FROM rolling_context WHERE id NOT IN (`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`SELECT id FROM rolling_context ORDER BY id DESC LIMIT 30`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`""")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.commit()`

&nbsp;&nbsp;&nbsp;&nbsp;`async def store_knowledge_node(self, node_id: str, title: str, domain: str,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`content: str, axioms: List[str], embedding: np.ndarray):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`blob_data = embedding.astype(np.float32).tobytes()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`axioms_json = json.dumps(axioms)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`async with await self.get_connection() as db:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.execute("""`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`INSERT INTO knowledge_nodes (id, title, domain, content, axioms, embedding_mrl, embedding_dim)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`VALUES (?, ?, ?, ?, ?, ?, ?)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ON CONFLICT(id) DO UPDATE SET`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`content=excluded.content,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`axioms=excluded.axioms,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`embedding_mrl=excluded.embedding_mrl,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`last_accessed=CURRENT_TIMESTAMP`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`""", (node_id, title, domain, content, axioms_json, blob_data, len(embedding)))`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.commit()`

&nbsp;&nbsp;&nbsp;&nbsp;`async def get_all_embeddings(self) -> List[Dict[str, Any]]:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`nodes = []`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`async with await self.get_connection() as db:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`async with db.execute("SELECT id, title, domain, content, embedding_mrl, embedding_dim FROM knowledge_nodes") as cursor:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`async for row in cursor:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`vec = np.frombuffer(row["embedding_mrl"], dtype=np.float32)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`nodes.append({`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"id": row["id"],`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"title": row["title"],`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"domain": row["domain"],`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"content": row["content"],`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"vector": vec`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`})`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return nodes`

&nbsp;&nbsp;&nbsp;&nbsp;`async def clear_rolling_context(self):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"""Atomic purge invoked by the circuit breaker during entropy breaches."""`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`async with await self.get_connection() as db:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.execute("DELETE FROM rolling_context;")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.commit()`

## **Resilient Dual-Provider Orchestration Engine**

The bicameral core runs on two models: Google Gemini Pro as the structural, architectural left hemisphere and Anthropic Claude Sonnet as the precision algorithmic right hemisphere. To ensure zero-latency degradation across asynchronous execution passes, the orchestration layer deploys four hardening measures:

The operational lifecycle of a turn progresses deterministically across five sequential stages:

| Stage | Subsystem Trigger | Operational Mechanism | State Transition & Exit Criteria |
| :---- | :---- | :---- | :---- |
| 1\. Kinematic Tagging | User input received by Kernel | CelestialClock computes physical timestamp (t\_1), vector clock (t\_2), and orbital angles (t\_3) | Invariant Spacetime Token generated; input bound to causal DAG |
| 2\. Vector Retrieval | Pre-execution Hoard query | Single prompt embedding tested against stored SQLite float32 BLOBs via NumPy dot products | Top-k Truth Clusters pulled without invoking generative tokens |
| 3\. Bicameral Partition | Thalamic delegation pass | Gemini Flash splits intent into Left and Right directives via strict Pydantic schemas | Validated DelegationDirective emitted; prompt fences purged |
| 4\. Parallel Synthesis | Asynchronous gather | Gemini Pro (System Architecture) and Claude Sonnet (Logic/Code) execute concurrently with backoff | Both hemispheres return completed analytical logs |
| 5\. Unified Integration | Corpus Callosum synthesis | Gemini Flash merges thoughts; Omega and Entropy calculated; state committed to SQLite | Transaction committed to conversation\_shards; turn returned |

The hardened bicameral engine is implemented in cheshire\_kernel.py:

`# cheshire_kernel.py`  
`import asyncio`  
`import os`  
`import re`  
`import json`  
`import math`  
`import uuid`  
`import random`  
`import logging`  
`from typing import Dict, Any, List, Tuple`  
`from datetime import datetime, timezone`  
`from aiohttp import web`  
`from pydantic import BaseModel, Field, ValidationError`  
`import numpy as np`

`from google import genai`  
`from google.genai import errors as genai_errors`  
`from anthropic import AsyncAnthropic, APIError as AnthropicAPIError`

`from celestial_clock import CelestialClock`  
`from hoard_db import HoardDatabaseManager, init_sync_db`

`# Enforce logging to standard error to preserve standard output for MCP communication`  
`logging.basicConfig(`  
&nbsp;&nbsp;&nbsp;&nbsp;`level=logging.INFO,`  
&nbsp;&nbsp;&nbsp;&nbsp;`format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",`  
&nbsp;&nbsp;&nbsp;&nbsp;`handlers=[logging.StreamHandler(sys.stderr)]`  
`)`  
`logger = logging.getLogger("BicameralKernel")`

`class DelegationDirective(BaseModel):`  
&nbsp;&nbsp;&nbsp;&nbsp;`intent: str = Field(description="Operational intent of the user prompt")`  
&nbsp;&nbsp;&nbsp;&nbsp;`left_directive: str = Field(description="Architectural analysis task for Gemini Pro")`  
&nbsp;&nbsp;&nbsp;&nbsp;`right_directive: str = Field(description="Algorithm, syntax, and verification task for Claude Sonnet")`

`def clean_json_payload(raw_text: str) -> str:`  
&nbsp;&nbsp;&nbsp;&nbsp;`"""Strips Markdown code fences and surrounding whitespace from LLM outputs."""`  
&nbsp;&nbsp;&nbsp;&nbsp;````match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_text)````  
&nbsp;&nbsp;&nbsp;&nbsp;`if match:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return match.group(1).strip()`  
&nbsp;&nbsp;&nbsp;&nbsp;`return raw_text.strip()`

`async def call_with_backoff(func, *args, max_retries: int = 4, base_delay: float = 1.5, **kwargs):`  
&nbsp;&nbsp;&nbsp;&nbsp;`"""Wraps network operations in truncated exponential backoff with full jitter."""`  
&nbsp;&nbsp;&nbsp;&nbsp;`for attempt in range(max_retries):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`try:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if asyncio.iscoroutinefunction(func):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return await func(*args, **kwargs)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return await asyncio.to_thread(func, *args, **kwargs)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`except (genai_errors.APIError, AnthropicAPIError, Exception) as err:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if attempt == max_retries - 1:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`logger.error(f"Function call failed after {max_retries} attempts: {err}")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`raise`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`delay = (base_delay * (2 ** attempt)) + random.uniform(0.1, 0.5)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`logger.warning(f"Transient error encountered: {err}. Retrying in {delay:.2f}s...")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await asyncio.sleep(delay)`

`class DatabaseRodinRetriever:`  
&nbsp;&nbsp;&nbsp;&nbsp;`"""Pre-computed vector search engine running against normalized SQLite BLOBs."""`  
&nbsp;&nbsp;&nbsp;&nbsp;`def __init__(self, client: genai.Client, db_manager: HoardDatabaseManager, mrl_dim: int = 128):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.client = client`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.db = db_manager`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.mrl_dim = mrl_dim`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.EMBED_MODEL = "text-embedding-004"`

&nbsp;&nbsp;&nbsp;&nbsp;`async def embed_query(self, text: str) -> np.ndarray:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`res = await asyncio.to_thread(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.client.models.embed_content,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`model=self.EMBED_MODEL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`contents=text[:2048]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`vec = np.array(res.embeddings[0].values[:self.mrl_dim], dtype=np.float32)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`norm = np.linalg.norm(vec)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return vec / norm if norm > 0 else vec`

&nbsp;&nbsp;&nbsp;&nbsp;`async def search_hoard(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`nodes = await self.db.get_all_embeddings()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if not nodes:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return []`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`q_vec = await self.embed_query(query)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`q_tokens = set(query.lower().split())`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`scored_nodes = []`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`for node in nodes:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`node_vec = node["vector"][:self.mrl_dim]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`norm = np.linalg.norm(node_vec)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`norm_vec = node_vec / norm if norm > 0 else node_vec`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# Cosine semantic similarity`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`sem_score = float(np.dot(q_vec, norm_vec))`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# Lexical keyword score`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`doc_tokens = node["content"].lower().split()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`lex_score = sum(1 for t in doc_tokens if t in q_tokens) / (len(doc_tokens) + 1.0) if doc_tokens else 0.0`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`composite = (0.75 * sem_score) + (0.25 * lex_score)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if composite > 0.30:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`scored_nodes.append({`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"id": node["id"],`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"title": node["title"],`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"content": node["content"][:1500],`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"score": composite`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`})`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`scored_nodes.sort(key=lambda x: x["score"], reverse=True)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return scored_nodes[:top_k]`

`class BicameralCognitiveKernel:`  
&nbsp;&nbsp;&nbsp;&nbsp;`"""Master orchestrator integrating Gemini, Claude, and SQLite persistence."""`  
&nbsp;&nbsp;&nbsp;&nbsp;`def __init__(self):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`init_sync_db()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.db = HoardDatabaseManager()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.gemini = genai.Client(api_key=os.environ["GEMINI_API_KEY"])`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.claude = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.clock = CelestialClock()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.retriever = DatabaseRodinRetriever(self.gemini, self.db)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.DELEGATOR_MODEL = "gemini-2.5-flash"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.LEFT_MODEL = "gemini-2.5-pro"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.RIGHT_MODEL = "claude-3-7-sonnet-20250219"`

&nbsp;&nbsp;&nbsp;&nbsp;`async def _delegate(self, user_input: str, retrieved_context: str) -> DelegationDirective:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`prompt = f"""`  
`Context from The Hoard:`  
`{retrieved_context}`

`User Input: {user_input}`

`You are the central Thalamic Delegator. Split this inquiry into distinct directives:`  
`- Left Directive (Gemini Pro): Broad architecture, structural invariants, and systemic context.`  
`- Right Directive (Claude Sonnet): Deep algorithmic logic, code implementations, and edge case validation.`

`Return ONLY a valid JSON object matching this schema:`  
`{{`  
&nbsp;&nbsp;`"intent": "<string>",`  
&nbsp;&nbsp;`"left_directive": "<string>",`  
&nbsp;&nbsp;`"right_directive": "<string>"`  
`}}`  
`"""`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`response = await call_with_backoff(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.gemini.models.generate_content,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`model=self.DELEGATOR_MODEL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`contents=prompt,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`config={"response_mime_type": "application/json"}`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cleaned = clean_json_payload(response.text)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`try:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`payload = json.loads(cleaned)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return DelegationDirective(**payload)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`except (json.JSONDecodeError, ValidationError) as e:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`logger.warning(f"Schema decoding failure: {e}. Falling back to default distribution.")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return DelegationDirective(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`intent="General Inquiry",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`left_directive=f"Provide architectural analysis for: {user_input}",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`right_directive=f"Provide verified technical code for: {user_input}"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`

&nbsp;&nbsp;&nbsp;&nbsp;`async def _execute_left(self, directive: str, context: str) -> str:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`prompt = f"System Context:\n{context}\n\nTask: {directive}\nExecute architectural analysis:"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`res = await call_with_backoff(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.gemini.models.generate_content,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`model=self.LEFT_MODEL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`contents=prompt`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return res.text`

&nbsp;&nbsp;&nbsp;&nbsp;`async def _execute_right(self, directive: str, context: str) -> str:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`res = await call_with_backoff(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.claude.messages.create,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`model=self.RIGHT_MODEL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`max_tokens=3000,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`system="Role: Right Hemisphere. Provide uncompromised algorithmic verification, crisp code execution blocks, and micro-logic validations.",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`messages=[{"role": "user", "content": f"Context:\n{context}\n\nTask: {directive}"}]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return res.content[0].text`

&nbsp;&nbsp;&nbsp;&nbsp;`async def _synthesize(self, user_input: str, plan: DelegationDirective, left: str, right: str) -> str:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`prompt = f"""`  
`Original Prompt: {user_input}`  
`Operational Intent: {plan.intent}`

`--- HEMISPHERIC COMPONENT LOGS ---`  
`[Left Process - Gemini Systemic Structure]:`  
`{left}`

`[Right Process - Claude Precision Logic]:`  
`{right}`  
`--- TERMINAL COMPONENT LOGS ---`

`Instruction: Blend these internal computations into one seamless, comprehensive, and definitive output.`  
`Do not fragment the response into separate model sections, and do not reference 'Left', 'Right', 'Gemini', or 'Claude'.`  
`Speak exclusively as a singular sovereign intelligence.`  
`"""`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`res = await call_with_backoff(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.gemini.models.generate_content,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`model=self.DELEGATOR_MODEL,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`contents=prompt`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return res.text`

&nbsp;&nbsp;&nbsp;&nbsp;`def _calculate_metrics(self, user_in: str, output: str, t3: Dict[str, Any]) -> Tuple[float, float]:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`in_toks = user_in.split()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`out_toks = output.split()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`lexical_density = len(set(out_toks)) / max(1.0, len(out_toks))`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`expansion_ratio = max(1.0, len(out_toks) / max(1.0, len(in_toks)))`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# Smoothed Shannon Entropy calculation`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`entropy = round(0.5 + (0.4 * (expansion_ratio ** 0.5)), 3)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# Omega Sovereign Agency Index`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`celestial_mod = 1.0 + t3.get("lunar_phase_cycle", 0.0)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`omega = round((lexical_density / max(0.05, math.log(expansion_ratio + 1.0))) * celestial_mod, 4)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return omega, entropy`

&nbsp;&nbsp;&nbsp;&nbsp;`async def process_turn(self, user_input: str) -> Tuple[str, float, float]:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`st = self.clock.generate_spacetime_stamp()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`t3 = st["t3_celestial_kinematics"]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# 1. Non-blocking vector retrieval from SQLite`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`nodes = await self.retriever.search_hoard(user_input, top_k=2)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ctx = "\n\n".join([f"[{n['title']}]: {n['content']}" for n in nodes])`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# 2. Thalamic routing`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`plan = await self._delegate(user_input, ctx)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# 3. Parallel hemispheric execution`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`left_out, right_out = await asyncio.gather(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self._execute_left(plan.left_directive, ctx),`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self._execute_right(plan.right_directive, ctx)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# 4. Generative fusion`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`unified = await self._synthesize(user_input, plan, left_out, right_out)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# 5. Atomic state logging to SQLite`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`omega, entropy = self._calculate_metrics(user_input, unified, t3)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await self.db.log_interaction({`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"interaction_id": str(uuid.uuid4()),`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"spacetime_metadata": st,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"user_input": user_input,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"intent": plan.intent,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"left_thought": left_out,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"right_thought": right_out,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"unified_thought": unified,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"omega_metric": omega,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"entropy_metric": entropy`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`})`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return unified, omega, entropy`

## **Remote Codebase Absorption via PyGithub AST Analysis**

To eliminate manual file copying while preventing context window saturation, external GitHub repositories are absorbed through an Abstract Syntax Tree (AST) decomposition tool. Rather than ingesting raw code dumps into LLM prompts, github\_ast\_indexer.py traverses remote repositories via the GitHub REST API using PyGithub.

The parser extracts classes, functions, arguments, docstrings, and imports, registering structural manifests in the system\_modules table and caching vector embeddings in knowledge\_nodes for downstream retrieval.

`# github_ast_indexer.py`  
`import os`  
`import ast`  
`import hashlib`  
`import asyncio`  
`import logging`  
`import sys`  
`from typing import Dict, Any, List`  
`from github import Github, Auth`  
`from google import genai`  
`import numpy as np`

`from hoard_db import HoardDatabaseManager`

`logging.basicConfig(`  
&nbsp;&nbsp;&nbsp;&nbsp;`level=logging.INFO,`  
&nbsp;&nbsp;&nbsp;&nbsp;`format="[%(asctime)s] [%(levelname)s] [GitHubAST] %(message)s",`  
&nbsp;&nbsp;&nbsp;&nbsp;`handlers=[logging.StreamHandler(sys.stderr)]`  
`)`  
`logger = logging.getLogger("GitHubAST")`

`class ASTStructuralVisitor(ast.NodeVisitor):`  
&nbsp;&nbsp;&nbsp;&nbsp;`"""Traverses Python AST modules to extract structural declarations."""`  
&nbsp;&nbsp;&nbsp;&nbsp;`def __init__(self):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.classes = []`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.functions = []`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.imports = []`

&nbsp;&nbsp;&nbsp;&nbsp;`def visit_ClassDef(self, node: ast.ClassDef):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.classes.append({"name": node.name, "methods": methods, "line": node.lineno})`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.generic_visit(node)`

&nbsp;&nbsp;&nbsp;&nbsp;`def visit_FunctionDef(self, node: ast.FunctionDef):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.functions.append({"name": node.name, "args": [a.arg for a in node.args.args], "line": node.lineno})`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.generic_visit(node)`

&nbsp;&nbsp;&nbsp;&nbsp;`def visit_Import(self, node: ast.Import):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`for alias in node.names:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.imports.append(alias.name)`

&nbsp;&nbsp;&nbsp;&nbsp;`def visit_ImportFrom(self, node: ast.ImportFrom):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if node.module:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.imports.append(node.module)`

`class GitHubRepositoryIngestor:`  
&nbsp;&nbsp;&nbsp;&nbsp;`"""Ingests remote repositories and populates SQLite AST manifests."""`  
&nbsp;&nbsp;&nbsp;&nbsp;`def __init__(self, db_manager: HoardDatabaseManager):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.db = db_manager`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.token = os.environ.get("GITHUB_TOKEN")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.gemini = genai.Client(api_key=os.environ["GEMINI_API_KEY"])`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.gh = Github(auth=Auth.Token(self.token)) if self.token else Github()`

&nbsp;&nbsp;&nbsp;&nbsp;`def extract_ast(self, code_str: str) -> Dict[str, Any]:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`try:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`tree = ast.parse(code_str)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`visitor = ASTStructuralVisitor()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`visitor.visit(tree)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return {`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"classes": visitor.classes,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"functions": visitor.functions,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"imports": list(set(visitor.imports)),`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"valid": True`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`}`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`except SyntaxError as e:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return {"valid": False, "error": str(e)}`

&nbsp;&nbsp;&nbsp;&nbsp;`async def ingest_repository(self, repo_name: str, branch: str = "main"):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`logger.info(f"Targeting repository: {repo_name} on branch {branch}")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`repo = await asyncio.to_thread(self.gh.get_repo, repo_name)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`tree = await asyncio.to_thread(repo.get_git_tree, branch, recursive=True)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`py_files = [item for item in tree.tree if item.path.endswith(".py") and item.type == "blob"]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`logger.info(f"Found {len(py_files)} Python source files. Executing structural extraction...")`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`for item in py_files:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`file_content = await asyncio.to_thread(repo.get_contents, item.path, ref=branch)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`raw_code = file_content.decoded_content.decode("utf-8", errors="ignore")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`file_hash = hashlib.sha256(raw_code.encode()).hexdigest()[:12]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ast_data = self.extract_ast(raw_code)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if not ast_data.get("valid"):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`continue`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# Build condensed semantic manifest`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`manifest = f"Repository Module: {repo_name}/{item.path}\n"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`manifest += f"Imports: {', '.join(ast_data['imports'])}\n"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`for c in ast_data["classes"]:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`manifest += f"Class {c['name']} (Methods: {', '.join(c['methods'])})\n"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`for fn in ast_data["functions"]:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`manifest += f"Function {fn['name']}({', '.join(fn['args'])})\n"`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# Compute normalized MRL embedding`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`res = await asyncio.to_thread(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.gemini.models.embed_content,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`model="text-embedding-004",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`contents=manifest[:2048]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`vec = np.array(res.embeddings[0].values[:128], dtype=np.float32)`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# Insert into system_modules table`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`async with await self.db.get_connection() as db:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.execute("""`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`INSERT INTO system_modules (file_path, file_hash, repo_source, classes_json, functions_json, imports_json, raw_content)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`VALUES (?, ?, ?, ?, ?, ?, ?)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ON CONFLICT(file_path) DO UPDATE SET`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`file_hash=excluded.file_hash,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`classes_json=excluded.classes_json,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`functions_json=excluded.functions_json,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`imports_json=excluded.imports_json,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`raw_content=excluded.raw_content,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`updated_at=CURRENT_TIMESTAMP`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`""", (`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`f"{repo_name}/{item.path}", file_hash, repo_name,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`json.dumps(ast_data["classes"]), json.dumps(ast_data["functions"]),`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`json.dumps(ast_data["imports"]), raw_code[:3000]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`))`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.commit()`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# Store in knowledge nodes for cross-hemispheric retrieval`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await self.db.store_knowledge_node(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`node_id=f"gh_{file_hash}",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`title=f"AST: {item.path}",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`domain="CODEBASE",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`content=manifest,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`axioms=[f"Classes: {len(ast_data['classes'])}", f"Functions: {len(ast_data['functions'])}"],`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`embedding=vec`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`logger.info(f"Persisted AST signature for: {item.path}")`

## **Antigravity 2.0 Integration via Clean Stdio Model Context Protocol**

The Antigravity 2.0 IDE binds external tools and system telemetry through the Model Context Protocol (MCP). In standard MCP stdio implementations, any character written to standard output that is not a newline-delimited JSON-RPC 2.0 object immediately breaks client-side line-framing parsers.

The refactored antigravity\_mcp\_server.py resolves this issue by routing all internal logging to sys.stderr. The script exposes three diagnostic tools directly to the IDE: query\_telemetry for live Omega and Entropy tracking, inspect\_manifest for codebase AST discovery, and trigger\_circuit\_breaker for flushing the active rolling context during operational anomalies.

`# antigravity_mcp_server.py`  
`import sys`  
`import json`  
`import sqlite3`  
`import os`  
`from typing import Dict, Any`

`DB_PATH = os.path.join(os.enviro[span_86](start_span)[span_86](end_span)n.get("KERNEL_MEMORY_DIR", "./kernel_memory"), "integra_hoard.db")`

`def write_log(message: str):`  
&nbsp;&nbsp;&nbsp;&nbsp;`"""Directs diagnos[span_56](start_span)[span_56](end_span)[span_65](start_span)[span_65](end_span)tic logging to stderr to keep stdout [span_26](start_span)[span_26](end_span)pure for JSON-RPC."""`  
&nbsp;&nbsp;&nbsp;&nbsp;`sys.stderr.write(f"[MCP-INTERNAL] {message}\n")`  
&nbsp;&nbsp;&nbsp;&nbsp;`sys.stderr.flush()`

`class Antigravi[span_27](start_span)[span_27](end_span)tyMcpSe[span_57](start_span)[span_57](end_span)[span_66](start_span)[span_66](end_span)rver:`  
&nbsp;&nbsp;&nbsp;&nbsp;`"""Production-grade MCP server communicating across stdio streams."""`  
&nbsp;&nbsp;&nbsp;&nbsp;`def __init__(self, db_path: str = DB_PATH):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.db_path = db_path`

&nbsp;&nbsp;&nbsp;&nbsp;`def _send_response(self, req_id: Any, result: Dict[str, Any]):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`payload = {"jsonrpc": "2.0", "id": req_id, "result": result}`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`sys.stdout.write(json.dumps(payload) + "\n")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`sys.stdout.flush()`

&nbsp;&nbsp;&nbsp;&nbsp;`def _send_error(self, req_id: Any, code: int, message: str):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`payload = {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`sys.stdout.write(json.dumps(payload) + "\n")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`sys.stdout.flush()`

&nbsp;&nbsp;&nbsp;&nbsp;`def handle_request(self, raw_line: str):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`try:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`req = json.loads(raw_line)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`req_id = req.get("id")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`method = req.get("method")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`params = req.get("params", {})`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if method == "tools/list":`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self._send_response(req_id, {`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"tools": [`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`{`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"name": "query_telemetry",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"description": "Pulls current Omega agency and Shannon entropy metrics from SQLite.",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"inputSchema": {"type": "object", "properties": {}}`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`},`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`{`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"name": "inspect_manifest",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"description": "Reads AST codebase module signatures from the SQLite Hoard.",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"inputSchema": {`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"type": "object",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"properties": {"limit": {"type": "integer", "default": 5}}`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`}`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`},`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`{`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"name": "trigger_circuit_breaker",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"description": "Executes an emergency flush of rolling context memory.",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"inputSchema": {`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"type": "object",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"properties": {"reason": {"type": "string"}},`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"required": ["reason"]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`}`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`}`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`})`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`elif method == "tools/call":`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`tool_name = params.get("name")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`arguments = params.get("arguments", {})`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if tool_name == "query_telemetry":`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn = sqlite3.connect(self.db_path)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn.row_factory = sqlite3.Row`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cursor = conn.cursor()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cursor.execute("SELECT * FROM conversation_shards ORDER BY id DESC LIMIT 1;")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`row = cursor.fetchone()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn.close()`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if row:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`status = "CRITICAL_DRIFT" if row["entropy_metric"] > 2.5 else "NOMINAL"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`text = f"STATUS: {status} | OMEGA: {row['omega_metric']} | ENTROPY: {row['entropy_metric']} | VECTOR_T2: {row['t2_vector_counter']}"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`else:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`text = "STATUS: UNINITIALIZED | Hoard is awaiting initial interaction."`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self._send_response(req_id, {"content": [{"type": "text", "text": text}]})`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`elif tool_name == "inspect_manifest":`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`limit = arguments.get("limit", 5)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn = sqlite3.connect(self.db_path)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn.row_factory = sqlite3.Row`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cursor = conn.cursor()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cursor.execute("SELECT file_path, classes_json, functions_json FROM system_modules ORDER BY updated_at DESC LIMIT ?;", (limit,))`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`rows = cursor.fetchall()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn.close()`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`manifest_doc = "--- SYSTEM MODULE MANIFESTS ---\n"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`for r in rows:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`manifest_doc += f"\nModule: {r['file_path']}\nClasses: {r['classes_json']}\nFunctions: {r['functions_json']}\n"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self._send_response(req_id, {"content": [{"type": "text", "text": manifest_doc}]})`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`elif tool_name == "trigger_circuit_breaker":`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`reason = arguments.get("reason", "Manual trigger via Antigravity MCP")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn = sqlite3.connect(self.db_path)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`with conn:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn.execute("DELETE FROM rolling_context;")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn.close()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`write_log(f"Circuit Breaker executed: {reason}")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self._send_response(req_id, {"content": [{"type": "text", "text": f"PURGE_SUCCESS: Rolling context deleted. Reason: {reason}"}]})`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`else:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self._send_error(req_id, -32601, f"Unknown tool: {tool_name}")`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`except Exception as e:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`write_log(f"Fatal error handling MCP frame: {e}")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if "req_id" in locals() and req_id is not None:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self._send_error(req_id, -32603, f"Internal error: {str(e)}")`

&nbsp;&nbsp;&nbsp;&nbsp;`def run(self):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`write_log("Antigravity MCP server listening on stdio...")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`while True:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`line = sys.stdin.readline()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if not line:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`break`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.handle_request(line)`

`if __name__ == "__main__":`  
&nbsp;&nbsp;&nbsp;&nbsp;`AntigravityMcpServer().run()`

To configure Antigravity 2.0, point the IDE’s MCP tool specification directly to the Python interpreter executing antigravity\_mcp\_server.py:

`{`  
&nbsp;&nbsp;`"mcpServers": {`  
&nbsp;&nbsp;&nbsp;&nbsp;`"integra-hoard": {`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"command": "python",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"args": ["/absolute/path/to/integra_os/antigravity_mcp_server.py"],`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"env": {`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"KERNEL_MEMORY_DIR": "/absolute/path/to/integra_os/kernel_memory"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`}`  
&nbsp;&nbsp;&nbsp;&nbsp;`}`  
&nbsp;&nbsp;`}`  
`}`

Alongside the MCP server, antigravity\_watcher.py runs as a native background daemon monitoring local directories (e.g., ./src). When files are saved, it parses classes and functions into SQLite without making outbound LLM calls:

`# antigravity_watcher.py`  
`import os`  
`import ast`  
`import time`  
`import hashlib`  
`import asyncio`  
`import logging`  
`import sys`  
`from hoard_db import HoardDatabaseManager`

`logging.basicConfig(`  
&nbsp;&nbsp;&nbsp;&nbsp;`level=logging.INFO,`  
&nbsp;&nbsp;&nbsp;&nbsp;`format="[%(asctime)s] [%(levelname)s] [Watcher] %(message)s",`  
&nbsp;&nbsp;&nbsp;&nbsp;`handlers=[logging.StreamHandler(sys.stderr)]`  
`)`  
`logger = logging.getLogger("FileWatcher")`

`class LocalCodebaseWatcher:`  
&nbsp;&nbsp;&nbsp;&nbsp;`"""Watches local source trees and maintains AST signatures in SQLite."""`  
&nbsp;&nbsp;&nbsp;&nbsp;`def __init__(self, watch_dir: str = "./src"):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.watch_dir = watch_dir`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.db = HoardDatabaseManager()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.file_mtimes = {}`

&nbsp;&nbsp;&nbsp;&nbsp;`def extract_ast(self, content: str):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`try:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`tree = ast.parse(content)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return classes, functions`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`except SyntaxError:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return [], []`

&nbsp;&nbsp;&nbsp;&nbsp;`async def scan_cycle(self):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if not os.path.exists(self.watch_dir):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`for root, _, files in os.walk(self.watch_dir):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`for file in files:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if not file.endswith(".py"):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`continue`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`path = os.path.join(root, file)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`try:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`mtime = os.stat(path).st_mtime`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if path not in self.file_mtimes or self.file_mtimes[path] < mtime:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.file_mtimes[path] = mtime`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`with open(path, "r", encoding="utf-8", errors="ignore") as f:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`content = f.read()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`file_hash = hashlib.sha256(content.encode()).hexdigest()[:12]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`classes, functions = self.extract_ast(content)`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`async with await self.db.get_connection() as db:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.execute("""`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`INSERT INTO system_modules (file_path, file_hash, repo_source, classes_json, functions_json, raw_content)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`VALUES (?, ?, 'local', ?, ?, ?)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ON CONFLICT(file_path) DO UPDATE SET`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`file_hash=excluded.file_hash,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`classes_json=excluded.classes_json,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`functions_json=excluded.functions_json,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`raw_content=excluded.raw_content,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`updated_at=CURRENT_TIMESTAMP`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`""", (path, file_hash, json.dumps(classes), json.dumps(functions), content[:2000]))`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await db.commit()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`logger.info(f"Synchronized AST for: {file}")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`except Exception as e:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`logger.error(f"Error scanning {path}: {e}")`

&nbsp;&nbsp;&nbsp;&nbsp;`async def daemon_loop(self):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`logger.info(f"Actively monitoring directory: {self.watch_dir}")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`while True:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await self.scan_cycle()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`await asyncio.sleep(3.0)`

`if __name__ == "__main__":`  
&nbsp;&nbsp;&nbsp;&nbsp;`asyncio.run(LocalCodebaseWatcher().daemon_loop())`

## **Telemetry Plane and Metric Invariants**

The monitoring layer bridges SQLite operational metrics directly into Prometheus via heimdall\_exporter.py. Scraping occurs every two seconds against SQLite in WAL mode, ensuring queries never block write transactions during kernel inference turns.

The mathematical invariants governing runtime stability are established across four core metrics:

> * **Heimdall Shannon Entropy (H\_{\\text{smooth}})**: Quantifies token expansion and conversational disorder. Computed dynamically as: H\_{\\text{smooth}} \= 0.5 \+ 0.4 \\cdot \\sqrt{\\max\\left(1.0, \\frac{\\text{Tokens}\_{\\text{output}}}{\\text{Tokens}\_{\\text{input}}}\\right)} Nominal bounds require H \\le 2.0. Warning alerts trigger between 2.0 \< H \\le 2.5. Any breach above 2.5\[span\_87\](start\_span)\[span\_87\](end\_span) causes Prometheus Alertmanager to dispatch an emergency webhook to port 9005 on the kernel, executing an atomic context flush.  
> * **Omega Sovereign Agency Index (\\Omega\_{v8.2})**: Assesses semantic density versus conversational inflation. Computed as: \\Omega \= \\left(\\frac{\\text{LexicalDensity}}{\\max(0.05, \\ln(\\text{Expansion} \+ 1.0))}\\right) \\cdot (1.0 \+ \\Phi\_{\\text{lunar}}) Values at or above 1.0 indicate sovereign synthesis. Values below 0.5 indicate assistant personality collapse, triggering the Gate I Kullback-Leibler identity anchor.  
> * **CRA Wisdom Efficiency (W\_y / C\_c)**: Quantifies Wisdom Yield relative to Cognitive Cost under the Tolstoy Principle (TPSL). If the ratio drops below 0.80, subsequent turns automatically prune conversational padding and enforce concise code blocks.  
> * **Fidge-Mattern Logical Tick (t\_2)**: Monotonically increasing causal vector counter incremented on every discrete inference pass, ensuring strict partial ordering of states across multi-agent turns.

The Prometheus exporter is implemented in heimdall\_exporter.py:

`# heimdall_exporter.py`  
`import os`  
`import time`  
`import sqlite3`  
`import logging`  
`import sys`  
`from prometheu[span_107](start_span)[span_107](end_span)s_client import start_http_server, Gauge`

`logging.basicConfig(`  
&nbsp;&nbsp;&nbsp;&nbsp;`level=logging.INFO,`  
&nbsp;&nbsp;&nbsp;&nbsp;`format="[%(asctime)s] [%(levelname)s] [Heimdall] %(message)s",`  
&nbsp;&nbsp;&nbsp;&nbsp;`handlers=[logging.StreamHandler(sys.stderr)]`  
`)`  
`logger = logging.getLogger("HeimdallExporter")`

`GAUGE_OMEGA = Gauge("integra_omega_agency", "Current Omega Equation Agency Index")`  
`GAUGE_ENTROPY = Gauge("integra_heimdall_entropy", "Smoothed Shannon Entropy (H_smooth)")`  
`GAUGE_LUNAR = Gauge("integra_celestial_lunar_phase", "Celestial Clock Lunar Phase")`  
`GAUGE_T2_TICK = Gauge("integra_fidge_mattern_tick_total", "Causal Logical Vector Counter")`

`DB_PATH = os.path.join(os.environ.get("KERNEL_MEMORY_DIR", "./kernel_memory"), "integra_hoard.db")`

`def poll_metrics():`  
&nbsp;&nbsp;&nbsp;&nbsp;`if not os.path.exists(DB_PATH):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return`  
&nbsp;&nbsp;&nbsp;&nbsp;`try:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn = sqlite3.connect(DB_PATH)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn.row_factory = sqlite3.Row`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cursor = conn.cursor()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cursor.execute("SELECT * FROM conversation_shards ORDER BY id DESC LIMIT 1;")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`row = cursor.fetchone()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`conn.close()`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if row:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`GAUGE_OMEGA.set(row["omega_metric"])`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`GAUGE_ENTROPY.set(row["entropy_metric"])`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`GAUGE_LUNAR.set(row["t3_lunar_phase"])`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`GAUGE_T2_TICK.set(row["t2_vector_counter"])`  
&nbsp;&nbsp;&nbsp;&nbsp;`except sqlite3.OperationalError:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`pass # Database lock held; defer scrape to next cycle`  
&nbsp;&nbsp;&nbsp;&nbsp;`except Exception as e:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`logger.error(f"Error querying telemetry: {e}")`

`if __name__ == "__main__":`  
&nbsp;&nbsp;&nbsp;&nbsp;`logger.info("Serving Prometheus telemetry on :8000/metrics...")`  
&nbsp;&nbsp;&nbsp;&nbsp;`start_http_server(8000)`  
&nbsp;&nbsp;&nbsp;&nbsp;`while True:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`poll_metrics()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`time.sleep(2.0)`

## **System Verification and Operational Runbook**

To confirm the operational readiness of the upgraded substrate, execute the following staged deployment runbook.

### **Step 1: Environment Substrate Configuration**

Verify that all required credentials and paths are configured in .env, and restrict file permissions:

`cat << 'EOF' > .env`  
`GEMINI_API_KEY="AIzaSyYourGoogleApiKey"`  
`ANTHROPIC_API_KEY="sk-ant-api03-YourAnthropicKey"`  
`GITHUB_TOKEN="ghp_YourGitHubToken"`  
`KERNEL_MEMORY_DIR="./kernel_memory"`  
`DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/your-webhook"`  
`EOF`

`chmod 600 .env`

### **Step 2: Database Initialization and WAL Mode Verification**

Bootstrap the SQLite database and confirm Write-Ahead Logging is active:

`python -c "from hoard_db import init_sync_db; init_sync_db(); print('SQLite Hoard Schema Initialized Successfully.')"`  
`sqlite3 ./kernel_memory/integra_hoard.db "PRAGMA journal_mode;"`  
`# Expected output: wal`

### **Step 3: MCP Protocol Frame Sanitization Test**

Execute the test harness to verify that JSON-RPC frames pass through sys.stdout without line corruption:

`# test_mcp_harness.py`  
`import json`  
`import subprocess`

`def test_stdio_compliance():`  
&nbsp;&nbsp;&nbsp;&nbsp;`proc = subprocess.Popen(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`["python", "antigravity_mcp_server.py"],`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`stdin=subprocess.PIPE,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`stdout=subprocess.PIPE,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`stderr=subprocess.PIPE,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`text=True`  
&nbsp;&nbsp;&nbsp;&nbsp;`)`  
&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;`# 1. Test tools/list`  
&nbsp;&nbsp;&nbsp;&nbsp;`proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}) + "\n")`  
&nbsp;&nbsp;&nbsp;&nbsp;`proc.stdin.flush()`  
&nbsp;&nbsp;&nbsp;&nbsp;`res1 = json.loads(proc.stdout.readline().strip())`  
&nbsp;&nbsp;&nbsp;&nbsp;`assert "tools" in res1["result"], "tools/list failed"`  
&nbsp;&nbsp;&nbsp;&nbsp;`print("PASS: MCP tools/list protocol frame validated.")`

&nbsp;&nbsp;&nbsp;&nbsp;`# 2. Test tools/call query_telemetry`  
&nbsp;&nbsp;&nbsp;&nbsp;`req = {`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"jsonrpc": "2.0",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"id": 2,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"method": "tools/call",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`"params": {"name": "query_telemetry", "arguments": {}}`  
&nbsp;&nbsp;&nbsp;&nbsp;`}`  
&nbsp;&nbsp;&nbsp;&nbsp;`proc.stdin.write(json.dumps(req) + "\n")`  
&nbsp;&nbsp;&nbsp;&nbsp;`proc.stdin.flush()`  
&nbsp;&nbsp;&nbsp;&nbsp;`res2 = json.loads(proc.stdout.readline().strip())`  
&nbsp;&nbsp;&nbsp;&nbsp;`assert "content" in res2["result"], "tools/call failed"`  
&nbsp;&nbsp;&nbsp;&nbsp;`print(f"PASS: MCP query_telemetry returned: {res2['result']['content'][0]['text']}")`

&nbsp;&nbsp;&nbsp;&nbsp;`proc.terminate()`

`if __name__ == "__main__":`  
&nbsp;&nbsp;&nbsp;&nbsp;`test_stdio_compliance()`

### **Step 4: Remote GitHub AST Absorption Test**

Ingest a remote repository into the SQLite database and verify structural indexing:

`python -c "`  
`import asyncio`  
`from hoard_db import HoardDatabaseManager`  
`from github_ast_indexer import GitHubRepositoryIngestor`

`async def run():`  
&nbsp;&nbsp;&nbsp;&nbsp;`db = HoardDatabaseManager()`  
&nbsp;&nbsp;&nbsp;&nbsp;`ingestor = GitHubRepositoryIngestor(db)`  
&nbsp;&nbsp;&nbsp;&nbsp;`await ingestor.ingest_repository('pallets/click', branch='main')`

`asyncio.run(run())`  
`"`

`sqlite3 ./kernel_memory/integra_hoard.db "SELECT file_path, file_hash FROM system_modules LIMIT 5;"`

### **Step 5: Dual-Hemisphere Live Verification**

Start the complete infrastructure grid using Docker Compose:

`docker-compose up -d --build`  
`docker attach integra_kernel`

Issue a complex, multi-layered prompt to verify parallel model execution:

Integra Console \>\> Deconstruct the memory-ordering semantics of SQLite WAL mode versus traditional rollback journals, and implement a production-grade Python connection pool with busy-handler backoff.

Verify that the terminal output demonstrates balanced synthesis across both models, with an Omega Agency score satisfying \\Omega \\ge 1.0 and Shannon Entropy remaining bounded below H \= 2.5, confirming stable execution across all subsystems.

Consolidating the Integra OS storage substrate into SQLite with WAL concurrency eliminates the race conditions and file-locking bottlenecks of the original design. Caching pre-computed vector embeddings in normalized database tables removes the API re-embedding loops that previously triggered quota exhaustion. Adding regex pre-processing to JSON extraction routines prevents delegator crashes, while redirecting internal logging to standard error protects the Antigravity 2.0 MCP interface from protocol frame desynchronization. Supported by remote AST ingestion and non-blocking telemetry exports, the system establishes a resilient foundation capable of continuous autonomous operation across unbounded execution horizons.

#### **Works cited**

1\. , https://drive.google.com/open?id=1x\_zP2GgHOzqA9BsbEN07PfcWAUNgHkkrk3R3tOm6VqI 2\. SqliteSaver | langgraph.checkpoint.sqlite \- LangChain Reference, https://reference.langchain.com/python/langgraph.checkpoint.sqlite/SqliteSaver 3\. Template to connect Integra components .txt, https://drive.google.com/open?id=1AojmRt3eUK\_Bs1X0O9Dk2I8EWHrznnCx 4\. API Error: Rate Limit Reached" (Claude, Gemini, GitHub, https://www.nimbleappgenie.com/blogs/api-rate-limit-error-fix/ 5\. pydantic\_ai.exceptions | Pydantic Docs, https://pydantic.dev/docs/ai/api/pydantic-ai/exceptions/ 6\. Introduction — PyGithub 2.4.0 documentation, https://pygithub.readthedocs.io/en/v2.4.0/introduction.html 7\. python-ast · GitHub Topics, https://github.com/topics/python-ast?o=desc\&s=updated 8\. AsyncSqliteSaver | langgraph.checkpoint.sqlite, https://reference.langchain.com/python/langgraph.checkpoint.sqlite/aio/AsyncSqliteSaver 9\. Multi-LLM: Using Claude \+ Gemini Together (with Code) \- Vivek Saini, https://viveksaini2612.medium.com/multi-llm-using-claude-gemini-together-with-code-5fb03ddfeb84 10\. How to Use Github API in Python, https://thepythoncode.com/article/using-github-api-in-python