Build every Integra surface dark. Put `void` under everything, set text in `monolith`, and let color carry meaning rather than decoration: cyan labels and structure, gold values, purple categories and sovereignty, orange and ember for the flame, green and red for state.

## Content fundamentals

- Write operational telemetry, not marketing. Interface copy is impersonal and declarative: no "you", "we" or "I". Real labels: "Sovereign System Dashboard", "Cognitive Health Matrix", "Executive Intelligence Briefing", "Dual Sync Isolation: ACTIVE".
- Keep the system's own vocabulary: Heimdall, Sovereign, Purple Epiphany, Friday Fortress, Cheshire Cat Kernel, Looking Glass, The Hoard. Never swap these for plain terms.
- Set labels, titles, column headers and badges uppercase with CSS (`text-transform: uppercase` plus the tracking in the type style) and write the source text in title case. Brand lines and status words are the exception and are stored uppercase: "DAILY PLANET INTELLIGENCE", "STANDBY".
- Separate meta items with a middle dot `·`, qualify with an em dash `—`, and use `|` only inside a gauge caption: "+25 bps (Sept 16) | 12-0 Unanimous".
- Show numbers in `mono` at a fixed precision and keep units attached: `0.0000`, `1.267`, `66.727°`, `+25 bps`, `3.75%`, `$761.69 – $769.89`.
- Name system variables with Greek and math glyphs: `ω`, `ΔE`, `KL`, `H` with a subscript `smooth`, `L` with a subscript `t`.
- Write status as one uppercase word: LIVE, INACTIVE, OPERATIONAL, ALWAYS ON, ARMED, READY, ACTIVE, STANDBY, OFFLINE.
- Write versions as `v8.2.2 — Purple Epiphany`. The logotype copy never changes: the wordmark is "Integra", the tagline is "Infinite Living Flame".

## Visual foundations

**Color.** Use `void` for the page and `card` for every panel on it. Edge panels with `card-border`; use `border-soft` or `border-strong` inside a panel. Set body text in `monolith-dim` with emphasis in `monolith`; never use pure white. Show a measured value in `flame-core`, a column header or section title in `sentinel-cyan`, a category label or section number in `purple-neon`, and an alert in `flame-deep` with `flame-glow`. Use `green` for live, up and active, and `red` for down and offline; always add a word or arrow, because the pair is told apart by hue alone. The only gradients are the brand gradients: `--subtitle-gradient` for the tagline, `--brand-gradient` for the brand line, `--footer-gradient` for the footer tagline. Apply them to text, never to panels.

**Type.** Set brand, titles, labels, badges and large numbers in Orbitron (`font-primary`); set data, tables and body in JetBrains Mono (`font-mono`). Sizes are small and rem-based. Orbitron appears at 400, 700 and (footer wordmark only) 900, never 500 or 600. Tracking is wide on uppercase text: 0.04em on compact table headers up to 0.3em on the tagline.

**Spacing and shape.** Pad a report card with `space-5` and a dashboard card with `space-3` by `space-4`; separate cards by `space-4`. Use `radius-lg` (8px) on report cards and `radius-xl` (10px) on dashboard cards; use smaller radii for what sits inside them (`radius-md` metric boxes, `radius-sm` lens boxes, `radius-xs` badges); `radius-pill` is for the kernel pill only. Borders are 1px; the one 2px border is the solid header rule in `purple-neon`.

**Glow and depth.** Never put a shadow or glow on a card. Glow is reserved for text and status marks: `cyan-glow`, `flame-glow`, `purple-glow`, `green-glow`, `clock-glow`, `celestial-glow`, `title-glow`. Depth comes from `void`, `card` and the 1px borders.

**Layout.** A report is one 960px column with 2rem padding. A dashboard is a 1440px page, 1.5rem side padding, on a 2-column grid that drops to one column under 960px; the 3-column grid drops to two and the 6-column grid to three. The logotype drops its wordmark size under 768px.

**Background.** Pages sit on flat `void`. Dashboards and the logo page add the ambient layer behind the content: a particle canvas (z-index 0), a purple glow ring (z-index 1) and content at z-index 2. Report pages have no ambient layer.

**Motion.** Motion is slow and ease-in-out: `ig-glow-pulse` 5s, `ig-title-pulse` 4s, `ig-tagline-glow` 3s, `ig-orbital-pulse` 2s, `ig-live-pulse` 1.5s to 2s. Use it only for live state, the logotype and the ambient layer. Do not animate layout, and do not add hover or press transitions: the on-system sources define none.

## Iconography

- Do not add an icon set. The sources use none. State is shown by the live dot, the kernel pill, badges and colored text; direction by `▲` and `▼`; variables by Greek glyphs.
- Dashboard card labels and lens names lead with an emoji (🕐 🌍 🏰 🦉). Treat that as a dashboard-only habit: reports do not use it, and a new surface should leave it out unless it extends an existing dashboard.
- Use the files in `assets/Logos` for the logo image. Both have a black background baked in: place them on `void`.

## Components

Components are plain CSS classes in `components/bundle.css`, prefixed `ig-`. Compose them with the tokens; do not restyle them inline.

- `Logotype`: wordmark, tagline, divider, version badge, telemetry line.
- `ReportHeader`, `SectionHeading`, `ReportFooter`: the page frame.
- `Card`, `Metric`, `ClockCard`, `DataTable`: surfaces and data display.
- `Status`: live dot, kernel pill, protocol badge, status text.
- `Grid`: the four column grids and the two page widths.
- `Narrative`: report prose and its thesis, antithesis and synthesis emphasis.
- `AmbientLayer`: particle canvas and glow ring.

## Using the system

Load Orbitron 400, 700 and 900 and JetBrains Mono 400, 500 and 700 from Google Fonts; no font files ship with the system. Load `tokens.css`, then `components/bundle.css`. Put `class="ig-card"` and the rest on markup; take sizes and weights for new text from the type styles.

## Intentional additions

- The `ig-` class prefix and a single token naming scheme replace the five inline copies of the same variables; `Token map` lists every old name.
- The spacing steps `space-1` to `space-8` are derived from the rem values that recur in the sources; the sources themselves use raw rem lengths.
- `bundle.css` turns every animation off under `prefers-reduced-motion: reduce`. The sources define no reduced-motion behavior.
