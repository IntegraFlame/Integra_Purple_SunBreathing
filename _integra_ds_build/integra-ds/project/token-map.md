# Token map

Where an existing Integra file names a value, use the Integra DS token on the right. Values are identical; only the names changed, so one scheme replaces two.

## Colors

| `static/brand.css` | Dashboards and reports | Integra DS |
| --- | --- | --- |
| `--color-void` | `--void` | `void` |
| (none) | `--card-bg` | `card` |
| `--color-monolith` | `--monolith` | `monolith` |
| (none) | `--monolith-dim` | `monolith-dim` |
| (none) | `--card-border` | `card-border` |
| `--color-flame-core` | `--flame-core` | `flame-core` |
| `--color-flame-primary` | `--flame-primary` | `flame-primary` |
| `--color-flame-deep` | `--flame-deep` | `flame-deep` |
| `--color-sentinel-cyan` | `--cyan` | `sentinel-cyan` |
| `--color-sentinel-ice` | (none) | `sentinel-ice` |
| (none) | `--cyan-dim` | `cyan-dim` |
| `--color-purple-neon` | `--purple` | `purple-neon` |
| `--color-purple-amethyst` | `--purple-amethyst` | `purple-amethyst` |
| `--color-purple-royal` | (none) | `purple-royal` |
| (none) | `--purple-dim` | `purple-dim` |
| (none) | `--green` | `green` |
| (none) | `--red` | `red` |
| (none) | `--table-row-alt` | `row-alt` |
| (none) | `--table-header-bg` | `table-head` |

Every other color token (`border-soft`, the `*-tint` and `*-edge` badge pairs, `celestial-*`, `clock-*`) names a hardcoded `rgba()` or hex that the dashboards write inline.

## Type, glow and gradient

| Source | Integra DS |
| --- | --- |
| `--font-primary`, `--font-mono` | `--font-primary`, `--font-mono` (unchanged) |
| `--flame-glow`, `--purple-glow`, `--cyan-glow` | `flame-glow`, `purple-glow`, `cyan-glow` |
| `--subtitle-gradient` | `--subtitle-gradient` in `bundle.css` (unchanged) |
| inline `linear-gradient(90deg, #00F0FF, #FFAA33, #FF7A00, #FF5500)` | `--brand-gradient` |
| inline five-stop footer gradient with `#4AE0B0` | `--footer-gradient` |

## Classes

| Source class | Integra DS |
| --- | --- |
| `.integra-logo-container`, `.integra-wordmark`, `.integra-subtitle` | `.ig-logo`, `.ig-wordmark`, `.ig-tagline` |
| `.report-header`, `.report-brand`, `.report-title`, `.report-meta` | `.ig-report-header`, `.ig-brand`, `.ig-report-title`, `.ig-report-meta` |
| `.dp-report-header` | `.ig-report-header--solid` |
| `.card`, `.card-label` | `.ig-card`, `.ig-card-label` (dashboard sizing: `--compact`) |
| `.metric-box`, `.metric-value`, `.metric-label` | `.ig-metric`, `.ig-metric-value`, `.ig-metric-label` |
| `.gauge-card`, `.gauge-value`, `.gauge-label`, `.gauge-sub` | `.ig-gauge`, `.ig-gauge-value`, `.ig-gauge-label`, `.ig-gauge-sub` |
| `.lens-box`, `.lens-count`, `.lens-name`, `.lens-desc` | `.ig-lens`, `.ig-lens-count`, `.ig-lens-name`, `.ig-lens-desc` |
| `.live-dot`, `.proto-badge` and `.proto-on/ready/active/standby` | `.ig-live-dot`, `.ig-proto` and `.ig-proto--on/ready/active/standby` |
| `.dp-status-ok`, `.dp-status-alert`, `.dp-status-sovereign` | `.ig-status-ok`, `.ig-status-alert`, `.ig-status-sovereign` |
| `table`, `th`, `td` | `.ig-table` (dashboard sizing: `--compact`) |
| `.lobe-active`, `.lobe-standby`, `.lobe-offline` | `.ig-lobe-active`, `.ig-lobe-standby`, `.ig-lobe-offline` |
| `.section-number`, `.section-title`, `.section-label` | `.ig-section-number`, `.ig-section-title`, `.ig-section-label` |
| `.clock-digital`, `.clock-time`, `.clock-date`, `.celestial-readout` | `.ig-clock`, `.ig-clock-time`, `.ig-clock-date`, `.ig-celestial-readout` |
| `.grid-2col`, `.grid-3col`, `.grid-4col`, `.grid-6col` | `.ig-grid--2`, `--3`, `--4`, `--6` |
| `.report-footer`, `.footer-brand`, `.footer-telemetry` | `.ig-footer`, `.ig-footer-tagline`, `.ig-footer-telemetry` |
| `em.thesis`, `em.antithesis`, `em.synthesis` | `.ig-thesis`, `.ig-antithesis`, `.ig-synthesis` |
| `#particles`, `.glow-ring` | `.ig-particles`, `.ig-glow-ring` |
