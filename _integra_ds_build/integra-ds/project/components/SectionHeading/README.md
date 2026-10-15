The headings that divide a page: a numbered section title for reports and a single label for dashboard rows.

**Classes:** `ig-section`, `ig-section-number`, `ig-section-title`, `ig-section-label`.

**Consumer provides:** the section number ("Section 01") and title, or the divider label.

- On a report, wrap each section in `ig-section` (a `space-8` gap below) and lead with `ig-section-number`, then `ig-section-title`. The title is uppercase `sentinel-cyan` over a `cyan-rule`.
- On a dashboard, put `ig-section-label` between rows: uppercase `purple-amethyst` over a `border-soft` rule.
- Number sections in order, with two digits: "Section 01", "Section 02".
- Do not use these for card labels (use `Card`) or the page title (use `ReportHeader`).
