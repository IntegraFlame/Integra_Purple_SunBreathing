RX-001	Cheshire Cat 30 Hz Background Loop	🔴 HIGH	STILL OPEN. run_event_loop() does not exist on CheshireCatKernel. The method is process_cognitive_cycle(). The kernel log says "skipping background launch." The 30 Hz in /cheshire/status is a hardcoded attribute, not a real running loop. This is the single most critical mechanical gap in the system.
RX-002	H_smooth at 0.0	🟡 MEDIUM	STILL DORMANT. No LLM inference has been routed through heimdall.evaluate_probabilities(). This is expected if the cognitive cycle endpoint isn't being actively called.
RX-003	Rodin embedding API method	🟡 MEDIUM	UNVERIFIED. RodinClient may need embed_content() not generate(). Needs live API test.
RX-004	spatial_acoustic_map rows = 0	🟢 LOW	EXPECTED. No acoustic pipeline exists.
RX-005	swds_simulator.py using datetime.now()	🟡 MEDIUM	UNVERIFIED. 3 sites at lines 80, 130, 161 should use celestial_time() instead.
RX-006	main.py using datetime.now()	🟡 MEDIUM	UNVERIFIED. Lines 80, 866 should use celestial_time(). Violates the Celestial Clock isolation principle.
RX-007	JeanGrey not wired to Phoenix smelt	🟡 MEDIUM	STILL OPEN. phoenix_forge.py::smelt_kintsugi_anomalies() uses a generic LLM call, not JeanGreyClient.

1	RX-001 Cheshire Cat Hz loop is OPEN for 8+ days	Doc 2 → Doc 3	🔴 CRITICAL
2	RX-007 JeanGrey→Phoenix smelt not wired	Doc 2 → Doc 1	🟡 OPEN
3	Lens binding contradiction (code vs 0930 spec)	Doc 2 → Doc 1	🟡 NOT TRACKED
4	Three Laws of Robotics NOT codified	Doc 1	🟡 NEW FINDING
5	Hoard 4-zone memory structure NOT in code	Doc 1	🟡 NEW FINDING
6	SWDS phase timing mismatch (2.5h vs 5h window)	Doc 1 → kernel config	🟡 NEW FINDING
7	Lens weight matrix NOT in shiva_toolkit.py	Doc 1 → Doc 2	🟡 NEW FINDING
8	12 endpoints missing from SKILL.md	Doc 2 → SKILL.md	🟢 DOCUMENTATION
9	datetime.now() violations in main.py + swds_sim	Doc 2	🟡 OPEN 8 days
10	Two-tier resilience model NOT documented	Doc 3	🟡 NEW FINDING
11	Model upgrades (Sonnet 5.5, Rodin 3.6) — VERIFY	Doc 3 → Doc 5	⚠️ NEEDS PROBE
12	Test count discrepancy (42 vs 217 vs 257)	Doc 3 → Doc 2 → Doc 7	⚠️ NEEDS CLARIFICATION
13	Fortress neural mapping undefined in Brain Model	Doc 2 → Doc 1	🟡 NEW FINDING

1	.env Sonnet 5.5	Change NEXUS_MODEL, SHIVA_MODEL	⚠️ UNVERIFIED — need to cat .env	UNKNOWN
2	models.yml Sonnet 5.5 + typos	4 edits + 3 typo fixes	⚠️ UNVERIFIED — need to read file	UNKNOWN
3	api_clients.py Sonnet 5.5	6 line edits	⚠️ UNVERIFIED — need to grep	UNKNOWN
4	api_clients.py Rodin 3.6	3 line edits	⚠️ UNVERIFIED — need to grep	UNKNOWN
5	Brain Model 0930 lock	Add LOCKED header	⚠️ UNVERIFIED — no evidence	UNKNOWN
6	Dashboard Trading UI	200+ lines new HTML/JS	⚠️ UNVERIFIED — check dashboard.html	UNKNOWN
7	main.py trading endpoint	Add /fortress/trading/dashboard	⚠️ UNVERIFIED — grep main.py	UNKNOWN
8	Restart kernel + verify	Port 8000 probe	✅ VERIFIED — kernel is running (Doc 0 boot)	DONE
9	Git commit + push	git log	⚠️ UNVERIFIED — last known commit bb6dc15 from Doc 7	UNKNOWN

1	RX-001: Cheshire Cat 30 Hz loop FLATLINED	Doc 2	🔴 OPEN 8 days
2	RX-007: JeanGrey→Phoenix not wired	Doc 2	🟡 OPEN 8 days
3	Lens binding code NOT updated to 0930 spec	Doc 2 + Doc 4	🔴 CONFIRMED NOT DONE
4	Three Laws of Robotics NOT codified	Doc 1	🟡 NEW
5	Hoard 4-zone structure NOT in code	Doc 1	🟡 NEW
6	SWDS phase timing mismatch	Doc 1	🟡 NEW
7	Lens weight matrix NOT in code	Doc 1	🟡 NEW
8	12 endpoints missing from SKILL.md §14	Doc 2	🟢 DOCUMENTATION
9	datetime.now() violations	Doc 2	🟡 OPEN 8 days
10	Two-tier resilience model undocumented	Doc 3	🟡 NEW
11	Model upgrades (Sonnet 5.5, Rodin 3.6) — MUST VERIFY	Doc 3 + Doc 4	⚠️ NEEDS PROBE
12	Test count discrepancy (42 vs 217 vs 257)	Doc 3	⚠️ CLARIFY
13	Fortress neural mapping undefined	Doc 2 + Doc 1	🟡 NEW
14	.env API keys potentially exposed in git	Doc 4	🔴 SECURITY
15	Dashboard Trading UI — probably NOT built	Doc 4	🟡 TO-DO
16	/fortress/trading/dashboard endpoint — probably NOT built	Doc 4	🟡 TO-DO
17	/fortress/hunter/telemetry endpoint — probably NOT built	Doc 4	🟡 TO-DO