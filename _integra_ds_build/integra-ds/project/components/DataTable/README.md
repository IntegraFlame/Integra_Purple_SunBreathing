The data table: uppercase cyan column headers over a zebra-striped body, in a standard and a compact size.

**Classes:** `ig-table` (`--compact`), and cell classes `ig-ticker`, `ig-price`, `ig-up`, `ig-down`, `ig-neutral`, `ig-lobe-active`, `ig-lobe-standby`, `ig-lobe-offline`.

**Consumer provides:** a plain `<table>` with `<thead>` and `<tbody>`. The classes color cells; the component adds no sort or selection.

- Use the standard table on report pages: 0.78rem cells with `0.55rem 0.75rem` padding.
- Use `--compact` on dashboards, inside a compact card: 0.65rem cells with 3px 6px padding and bold 0.5rem headers.
- Set a ticker or name in `ig-ticker`, a price or measured value in `ig-price` (`flame-core`), a direction in `ig-up` or `ig-down`, and a neutral state in `ig-neutral`.
- Show lobe state with `ig-lobe-active`, `ig-lobe-standby` or `ig-lobe-offline`, written as a word.
- Left-align text columns; right-align numeric columns.
- Do not add vertical rules or heavier borders.
