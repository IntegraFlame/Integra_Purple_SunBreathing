# Audit notes

What the extraction found in the existing Integra files. Nothing here was silently fixed: every source value is kept as written, and each item below is a decision for you.

## Contrast (WCAG 2, measured)

Failing text pairs, all on dark grounds. Each token's usage note carries the same number.

| Pair | Ratio | Where the source uses it | Suggested fix |
| --- | --- | --- | --- |
| `purple-neon` on `card` | 3.65:1 | `card-label` and compact card labels, 0.55–0.65rem | Move small purple labels to `purple-amethyst` (4.30:1 on `card`, 4.57:1 on `void`), or set them 14px bold |
| `purple-neon` on `void` | 3.88:1 | `section-number`, 0.65rem | `purple-amethyst` on `void` (4.57:1) |
| `purple-neon` at 70% opacity on `void` | 2.31:1 | The version badge on the logo page | Drop the opacity or use `monolith-dim` |
| `purple-amethyst` on `card` | 4.30:1 | Lens counts, 0.85rem bold | Just under 4.5:1; raise the size to 14px bold or put it on `void` |
| `purple-faint` on `void` | 1.64:1 | Report footer telemetry | Use `monolith-dim`, as the dashboard footer already does |
| `monolith-faint` on `card` | 3.42:1 | Lens descriptions, 0.45rem | Use `monolith-dim` |
| `purple-royal` on `card` | 3.31:1 | Declared, never used as text | Keep it out of text |

Everything else passes 4.5:1, including `monolith-dim` on `void` and `card` (8.3:1 and 7.8:1), every flame color, `sentinel-cyan`, `green`, `red` and the celestial indigos.

`green` and `red` are 7.8:1 and 5.3:1 on `card`, close in lightness, so they are told apart by hue alone. The report tables mark up and down moves with color only; the protocol badges and lobe states carry a word as well.

## Type size

The smallest text is 0.45rem (7.2px) in `metric-label`, `lens-name` and `lens-desc`; 0.5rem (8px) in badges, compact table headers and the footer tagline and telemetry. These are below the 11–12px floor most dense dashboards hold. Orbitron's wide letterforms help, but a floor of 0.65rem for anything a person must read is worth setting.

## Structure

- Two naming schemes for one palette: `static/brand.css` uses `--color-*`, every dashboard and report uses bare `--*`. The Token map resolves this.
- `static/brand.css` defines 9 classes (the logotype, the solid report header, section title, metric value, three status styles). Cards, grids, tables, badges, gauges, clocks and footers exist only as inline `<style>` blocks, copied between `static/dashboard.html`, `daily_planet_report.html` and `static/celestial_clock_live.html`. Their `:root` blocks already differ (`--purple-amethyst`, `--red`, `--table-*` appear in some files only).
- The repo root, `static/`, `CODE/` and `integra-homebase/` hold copies of the same UI files (`celestial_clock_live.html`, `integra_logo_live.html`, `daily_planet_report.html`, the dual clock widget). They will drift.
- `glowPulse` is defined two ways: `translateX(-50%)` on dashboards and `translate(-50%, -50%)` on the logo page. `ig-glow-pulse` follows the dashboard.
- The compact dashboard table and the report table differ by tiny alphas (`hairline` 0.04 against 0.03, `row-alt` 0.02 against 0.015, `table-head` 0.06 against 0.04). Both are kept as `*-compact` tokens; merge them if the difference is not intended.
- The kernel pill's live border is 0.4 in markup and 0.5 once the dashboard script sets it. `green-ring` keeps 0.4.

## Off-system and missing

- `swds_simulation_dashboard.html` (and its duplicate `Correctswds_simulation_dashboard.html`) uses Tailwind and an unrelated palette: era colors `#ef4444`, `#f59e0b`, `#8b5cf6`, hover lifts and a tab control. It was not extracted. Re-skinning it with this system would need a Tabs component, which the on-system files do not have.
- No hover, focus, active or disabled states, and no buttons, inputs, selects or links are defined on any on-system page. Interactive components would be new.
- Orbitron and JetBrains Mono load from Google Fonts at runtime. No font files exist in the repo, so offline use falls back to `sans-serif` and `monospace`.
- The sources define no reduced-motion behavior; `bundle.css` adds it.
