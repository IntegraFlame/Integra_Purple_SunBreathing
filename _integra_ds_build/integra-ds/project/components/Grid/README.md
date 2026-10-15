The layout grids and page widths: 2, 3, 4 and 6 equal columns, a 960px report column and a 1440px dashboard page.

**Classes:** `ig-grid` with `--2`, `--3`, `--4`, `--6`; `ig-page` and `ig-page--wide`.

**Consumer provides:** the children. Every grid child gets `min-width: 0` so long values cannot stretch a column.

- Use `--2` for the two main columns of a dashboard row (`space-4` gap).
- Use `--3` (0.6rem gap) for groups of three cards and `--4` (`space-2` gap) for metric boxes.
- Use `--6` (`space-1` gap) for the lens-box row only.
- Under 960px: `--2` becomes one column, `--3` two columns and `--6` three; `--4` is unchanged.
- Wrap a report in `ig-page` (960px, `space-7` padding) and a dashboard in `ig-page--wide` (1440px, `space-4` by `space-6` padding).
- Do not add breakpoints: the system has 960px for layout and 768px for the logotype.
