The Integra logotype: the "Integra" wordmark over the "Infinite Living Flame" tagline, with an optional divider, version badge and telemetry readout.

**Classes:** `ig-logo` (container), `ig-wordmark`, `ig-tagline`, `ig-logo-divider`, `ig-version`, `ig-telemetry` with `ig-val` for each value.

**Consumer provides:** the container on a `void` ground, and the telemetry values. The wordmark and tagline text never change.

- Use `ig-logo` on a landing or title surface. The wordmark is `monolith`, never pure white, and its size follows the viewport between 3rem and 7rem.
- Fill the tagline with the subtitle gradient and keep it uppercase at 0.3em tracking.
- Show the version badge as `v8.2.2 — Purple Epiphany` and the telemetry as `ω`, `ΔE`, `KL`, `H` with a subscript; keep the values in `flame-core`.
- Use the supplied image files (see the Logos assets) when a picture is required, on `void` only. Do not redraw the wordmark.
- Do not put the logotype on `card` or a colored ground. Do not recolor the tagline gradient.
- The title and tagline pulse slowly; both stop under `prefers-reduced-motion`.
