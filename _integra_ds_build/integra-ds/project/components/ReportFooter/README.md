The footer that closes a report or dashboard: the Integra wordmark and tagline, an optional meta line and a telemetry readout.

**Classes:** `ig-footer`, `ig-footer-lockup`, `ig-footer-wordmark`, `ig-footer-tagline`, `ig-footer-meta`, `ig-footer-telemetry` (`--dim`).

**Consumer provides:** the telemetry values, and for a report the meta line (report name and ID).

- Always include the lockup: "Integra" in 900 weight and `monolith`, over "INFINITE LIVING FLAME" in the five-stop footer gradient.
- On a dashboard, set the telemetry in `ig-footer-telemetry--dim` (`monolith-dim`): "ω = 1.00 · ΔE = 0.0000 · H smooth = 0.00 · DUAL SYNC ISOLATION: ACTIVE".
- On a report, the telemetry is `purple-faint`. That is 1.6:1 on `void`; keep it decorative and put anything a person needs in the meta line.
- A `card-border` rule sits above the footer.
