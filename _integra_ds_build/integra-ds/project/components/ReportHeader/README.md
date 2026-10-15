The header at the top of a report or dashboard: a gradient brand line, a title and a meta row.

**Classes:** `ig-report-header` with `--compact` (dashboard) or `--solid` (brand.css rule), `ig-brand`, `ig-report-title`, `ig-report-meta` with `ig-label` and `ig-value`.

**Consumer provides:** the brand line (uppercase text), the title, and meta items as label and value pairs. A compact header also takes a right-hand block for the kernel pill and uptime.

- Use the standard header on a 960px report: brand line, `report-title`, then a wrapping meta row with `sentinel-cyan` labels and `monolith-dim` values.
- Use `--compact` on a dashboard: the brand line at 0.9rem, a 1.1rem title, and a single meta line separated with `·`. Put a live dot before the status word, and the kernel pill on the right.
- Use `--solid` only to match brand.css: a 2px `purple-neon` rule under a 1.25rem title.
- Color a meta value only when its meaning sets it, for example `green` on "1.267 (Approved)".
- Do not put the brand gradient on anything except the brand line.
