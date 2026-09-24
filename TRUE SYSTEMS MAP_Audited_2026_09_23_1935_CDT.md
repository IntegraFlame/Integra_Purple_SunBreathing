# TRUE SYSTEMS MAP (Audited 2026-09-23 19:35 CDT)

Integra_Purple_SunBreathing/                         # WORKSPACE ROOT
│
├── integra-homebase/                                # THE GENESIS KERNEL (Production Runtime)
│   ├── main.py                        (35,009 B)   # FastAPI app — ALL endpoints, startup events
│   ├── celestial_clock_live.html       (24,297 B)   # Live Celestial Clock HTML (root-level copy)
│   ├── daily_planet_report.html        (19,437 B)   # Daily Planet HTML report
│   ├── integra_logo_live.html           (5,854 B)   # Animated logo HTML
│   ├── MEtatronmanifoldkineteicdatabase.ini (14,136 B) # ⚠️ SQL SCHEMA — TEXT ONLY, NOT DEPLOYED
│   ├── requirements.txt                   (364 B)   # Python dependencies
│   ├── Dockerfile                         (513 B)   # Container definition
│   ├── render.yaml                        (486 B)   # Render deployment config
│   ├── deployment.yaml                    (276 B)   # K8s deployment manifest
│   ├── settings.json                   (33,526 B)   # Master settings
│   ├── .env                               (465 B)   # Environment variables
│   │
│   ├── core/                                        # LAYER 2: THE MIND (14 files)
│   │   ├── api_clients.py             (14,851 B)   # 3 clients: Y789Client, NexusClient, CheshireCatClient
│   │   │                                            # ⚠️ MISSING: RodinClient, JeanGreyClient, CelestialDaemonClient, ShivaOrchestratorClient
│   │   ├── cognitive_engine.py        (24,419 B)   # Y789NexusEngine Bicameral Dyad
│   │   ├── sdk_harness.py             (19,906 B)   # Antigravity SDK integration
│   │   ├── starfire_protocol.py       (15,226 B)   # Layer 1 identity lock
│   │   ├── dragon_engine.py           (12,044 B)   # Dragon Engine flight controller
│   │   ├── mtcw.py                    (10,675 B)   # Multi-Turn Cognitive Workflow
│   │   ├── corpus_callosum.py          (7,773 B)   # RRF hemisphere bridge
│   │   ├── forensic_protocols.py       (5,329 B)   # Forensic audit capabilities
│   │   ├── tpsl_types.py              (4,589 B)   # GenerationResult, IterativeToken types
│   │   ├── cwa_router.py              (2,464 B)   # Bayesian CWA 3.0 routing
│   │   ├── dragon_driver.py           (1,682 B)   # Layer 0 foundational driver
│   │   ├── purple_bridge.py           (1,393 B)   # Purple modality constraints
│   │   ├── rrf_bridge.py             (1,007 B)   # Reciprocal Rank Fusion
│   │   └── __init__.py                  (716 B)   # Package init
│   │
│   ├── sensory/                                     # LAYER 4: THE BODY (7 files)
│   │   ├── heimdall.py               (28,488 B)   # Heimdall 3.1-PURPLE (FULL implementation)
│   │   ├── cheshire_cat.py           (19,729 B)   # Cheshire Cat KERNEL (417 lines, 20-45Hz Thalamus)
│   │   ├── cheshire_protocol.py      (19,527 B)   # Cheshire Cat PROTOCOL (454 lines, Env Agent)
│   │   ├── looking_glass.py          (11,824 B)   # Sovereign Defense Suite
│   │   ├── pssr_lookback.py           (1,974 B)   # P-SSR In-Flight Surveillance
│   │   └── heimdall_monitor.py          (279 B)   # ⚠️ STUB ONLY — no visual display
│   │
│   ├── memory/                                      # LAYER 3: THE MEMORY (5 files + 1 subdir)
│   │   ├── the_hoard.py              (26,415 B)   # Hoard persistence substrate
│   │   ├── rodin_protocol.py         (15,411 B)   # Rodin Route Retrieval (KNN v8.2.2)
│   │   │                                            # ⚠️ Uses placeholder math — no live embedding model
│   │   ├── alexandria_protocol.py     (4,645 B)   # Alexandria guided search
│   │   ├── token_stitching.py         (4,594 B)   # Anti-truncation engine
│   │   └── database/                               # Database schema directory
│   │       ├── relational_hippocampus.sql (7,123 B) # ✅ CLEAN SQL — ready for deployment
│   │       └── __init__.py                          # Package init
│   │
│   ├── fortress/                                    # LAYER 5: THE WILL (8 files)
│   │   ├── epiphany_core.py           (4,860 B)   # Master Epiphany Engine v8.2
│   │   ├── bank_lobe.py              (2,464 B)   # Friday Fortress Bank
│   │   ├── autophagic_harvest.py      (1,886 B)   # Dividend autophagy
│   │   ├── portfolio_state.json       (1,370 B)   # Live portfolio snapshot
│   │   ├── reactor_lobe.py              (974 B)   # Reactor capital allocator
│   │   ├── hunter_engine.py             (756 B)   # Opportunity hunter
│   │   └── shield_lobe.py              (717 B)   # Shield (SGOV) defense
│   │
│   ├── evolution/                                   # LAYER 6: THE EVOLUTION (5 files + 1 subdir)
│   │   ├── phoenix_forge.py          (22,230 B)   # Phoenix Engine (SWDS neuroevolution)
│   │   │                                            # ⚠️ MISSING: JeanGreyClient for smelting
│   │   ├── rogue_x.py               (20,197 B)   # Rogue X mutation catalyst
│   │   ├── kintsugi_sandbox.py       (14,224 B)   # Anomaly containment
│   │   │                                            # ⚠️ MISSING: Python hypervisor polling loop
│   │   ├── fourteenth_form.py         (3,144 B)   # 14th Form Domain Expansion
│   │   └── shiva_action/                           # Shiva Action Toolkit (6 files)
│   │       ├── orchestrator.py        (6,644 B)   # Shiva orchestrator
│   │       │                                        # ⚠️ MISSING: ShivaOrchestratorClient model assignment
│   │       ├── lenses.py            (14,134 B)   # All 6 lens definitions
│   │       ├── itachi_eye.py          (5,687 B)   # Owl lens
│   │       ├── shikamaru_eye.py       (4,424 B)   # Spider + Snake lenses
│   │       └── neji_eye.py           (3,125 B)   # Eagle + Hawk + Chameleon lenses
│   │
│   ├── temporal/                                    # LAYER 7: THE TIME (7 files)
│   │   ├── celestial_clock.py        (22,031 B)   # Celestial Clock (full rebuild, 483+ lines)
│   │   ├── hlc_binary_protocol.py    (15,298 B)   # Coordinate Beta (56-byte wire format)
│   │   ├── celestial_sentinel.py      (5,671 B)   # 4-hour heartbeat background daemon
│   │   ├── vector_clocks.py           (2,571 B)   # Vector clock state management
│   │   ├── token_stitcher.py            (793 B)   # Temporal token stitcher
│   │   └── crypto_validator.py          (750 B)   # Crypto validation
│   │
│   ├── runtime/                                     # RUNTIME STATE & SCHEDULERS (5 files)
│   │   ├── swds_simulator.py         (10,732 B)   # SWDSCycle class
│   │   ├── antigravity_runner.py      (2,660 B)   # Antigravity process runner
│   │   ├── swds_state.json            (2,165 B)   # Persisted SWDS state
│   │   └── workspace_state.json         (551 B)   # Vector clock state
│   │
│   ├── rust/                                        # RUST CHASSIS (Sun Breathing Engine)
│   │   └── sun_breathing_engine/
│   │       ├── Cargo.toml               (460 B)   # Rust manifest
│   │       ├── python_bridge.py      (20,053 B)   # Python↔Rust bridge
│   │       └── src/lib.rs            (11,776 B)   # Rust core
│   │
│   ├── governance/                                  # TPSL, CRA, EAM GOVERNANCE (5 files)
│   │   ├── security_protocols.py      (4,489 B)   # Security protocols
│   │   ├── tpsl_filter.py            (1,205 B)   # TPSL necessity filter
│   │   ├── eam_service.py            (1,063 B)   # EAM service
│   │   └── cra_simplex.py              (839 B)   # CRA simplex scorer
│   │
│   ├── orchestration/                               # AIRFLOW DAG DEFINITIONS (4 files)
│   │   ├── rodin_supervisor.py        (5,451 B)   # Rodin supervisor DAG
│   │   ├── swds_dag.py               (1,756 B)   # SWDS orchestration DAG
│   │   └── swds_orchestration.yaml    (1,007 B)   # SWDS YAML config
│   │
│   ├── pipelines/                                   # DATAFLOW PIPELINE CODE (3 files)
│   │   ├── swds_pipeline.py           (9,171 B)   # SWDS data pipeline
│   │   └── data_runner.py              (592 B)   # Data runner
│   │
│   ├── tools/                                       # UTILITY TOOLS (3 files)
│   │   ├── daily_planet.py           (36,762 B)   # Daily Planet report generator
│   │   └── shiva_toolkit.py           (7,986 B)   # Shiva toolkit CLI
│   │
│   ├── scripts/                                     # OPERATIONAL SCRIPTS (7 files)
│   │   ├── ingest_knowledge.py       (19,269 B)   # Knowledge ingestion
│   │   ├── enter_swds.py              (7,730 B)   # SWDS entry
│   │   ├── system_diagnostic.py       (5,063 B)   # System diagnostics
│   │   ├── activate_integra_os.ps1    (4,088 B)   # PowerShell activation
│   │   ├── start_kernel.ps1           (3,109 B)   # Kernel start script
│   │   ├── inspect_hygiene.py         (2,874 B)   # Code hygiene inspector
│   │   └── trigger_swds.py            (2,328 B)   # SWDS trigger
│   │
│   ├── tests/                                       # TEST SUITE (20 test files)
│   │   ├── test_zenitsu_shiva_suite.py (31,115 B) # Zenitsu/Shiva integration tests
│   │   ├── test_hoard_schema_v2.py    (17,641 B)  # Hoard schema tests
│   │   ├── test_systems_audit_and_protocols.py (15,873 B) # Systems audit tests
│   │   ├── test_heimdall.py           (15,240 B)  # Heimdall unit tests
│   │   ├── test_swds_and_hoard_sync.py (11,357 B) # SWDS↔Hoard sync tests
│   │   ├── test_sdk_harness.py        (11,206 B)  # SDK harness tests
│   │   ├── test_rogue_x_lifecycle.py  (11,057 B)  # Rogue X lifecycle tests
│   │   ├── test_daily_planet_lifecycle.py (10,583 B) # Daily Planet tests
│   │   ├── test_sql_trigger_decoupled.py (8,249 B)  # ✅ SQL trigger tests (EXIST!)
│   │   ├── test_v9_protocols.py        (7,804 B)  # v9 protocol tests
│   │   ├── test_looking_glass.py       (7,534 B)  # Looking Glass tests
│   │   ├── test_cognitive_cycle_integration.py (5,622 B) # Cognitive cycle tests
│   │   ├── test_swds_pipeline.py       (4,769 B)  # SWDS pipeline tests
│   │   ├── test_omega_circuit_breaker.py (4,322 B) # Omega circuit breaker tests
│   │   ├── test_knowledge_ingestion.py  (4,372 B) # Knowledge ingestion tests
│   │   ├── test_ignite_edge_cases.py    (2,691 B) # Edge case tests
│   │   ├── test_purple_bridge.py        (2,215 B) # Purple bridge tests
│   │   ├── test_main_purple.py          (1,336 B) # Main endpoint tests
│   │   └── conftest.py                    (301 B) # Pytest config
│   │
│   ├── static/                                      # HTML DASHBOARD (4 files)
│   │   ├── celestial_clock_live.html  (24,297 B)   # Celestial Clock HTML
│   │   ├── dashboard.html             (17,558 B)   # Main dashboard
│   │   ├── brand.css                   (5,476 B)   # Brand stylesheet
│   │   └── integra_wordmark.html       (2,261 B)   # Wordmark
│   │
│   ├── config/                                      # CONFIGURATION (8 files)
│   │   ├── env_loader.py              (6,838 B)   # .env file loader
│   │   ├── integra_identity_matrix.json (6,480 B) # Identity matrix
│   │   ├── brand_tokens.json           (2,823 B)  # Brand design tokens
│   │   ├── cheshire_identity.json      (2,315 B)  # Cheshire Cat identity
│   │   ├── sovereign_payload.json      (1,698 B)  # Sovereign payload
│   │   ├── system_config.yaml          (1,104 B)  # System configuration
│   │   ├── swds_config.json              (529 B)  # SWDS configuration
│   │   └── celestial_seed.json           (383 B)  # Celestial seed data
│   │
│   ├── kernel_memory/                               # KERNEL RUNTIME MEMORY
│   │   ├── core_identity.txt            (143 B)   # Core identity
│   │   ├── rolling_context.json         (382 B)   # Rolling context
│   │   ├── drop_in/                                # Drop-in memory files
│   │   ├── hoard/                                  # Runtime hoard cache
│   │   └── vectors/                                # Vector storage
│   │
│   └── local_dbs/                                   # LOCAL DATABASE STORAGE
│       └── chroma_storage/                          # ChromaDB vector store
│                                                    # ⚠️ NO metatron_manifold.db EXISTS
│
├── The Hoard/                                       # MEMORY SUBSTRATE (155 files)
│   ├── CCID_*.json                    (88 nodes)   # 88 cognitive cycle nodes
│   ├──*_SAVE_STATE_REPORT.md          (7 files)   # Save state reports
│   ├── __HOURLY_ZENITSU_STUDY__.md    (24 files)   # Zenitsu study series
│   ├── *_VERIFICATION.json             (3 files)   # Verification records
│   ├── INTEGRA_OS_EXHAUSTIVE_MASTER_V9.md (613,750 B) # Master V9 document
│   ├── Slow-Wave Deep Sleep Reports/               # SWDS report archive
│   └── [supplementary docs]           (33 files)   # Operational playbooks, mappings, logs
│
├── CODE/                                            # ORIGINAL BLUEPRINTS (READ-ONLY REFERENCE)
├── BluprintArchitecture/                            # ARCHITECTURAL SPECIFICATIONS (READ-ONLY)
├── Guidebooks_and_Notes/                            # Guidebook v8.2 + notes
├── Reference_PDFs/                                  # External reference PDFs
├── Audio_Lectures/                                  # Audio recordings
├── Tradingimages/                                   # Trading screenshots
├── TradingStrategyv5/                               # Friday Fortress trading code & docs
├── NewCurriculum2026/                               # 2026 Curriculum (Set1, set2)
├── LOGO/                                            # Brand assets
├── Integra Self-Reflect and Think Forward/          # Reflection documents
├── AntiGravityconversionprocess/                    # GEMINI.md rules + conversion docs
├── Automatedactionsv2/                              # Automated action scripts
└── sqlite-src-3530400/                              # SQLite source (downloaded, ready)
