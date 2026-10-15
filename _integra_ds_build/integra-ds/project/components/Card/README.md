The panel every Integra surface is built from: a `card` fill, a 1px `card-border` edge and an uppercase label.

**Classes:** `ig-card`, `ig-card--compact`, `ig-card--celestial`, `ig-card-label`.

**Consumer provides:** a label and the content. Pass the label color inline when the card's meaning sets it (`sentinel-cyan` for health, `flame-core` for capital, `celestial-indigo` for celestial).

- Use `ig-card` on report pages: `radius-lg`, `space-5` padding.
- Use `ig-card--compact` on dashboards: `radius-xl`, `space-3` by `space-4` padding, and a 0.6rem bold label.
- Use `ig-card--celestial` for the celestial-kinematics card only: it swaps the edge to `celestial-edge`.
- Default the label to `purple-neon`. Small purple labels fall below 4.5:1; see the Audit notes.
- Nest metric boxes, lens boxes, clock cards and tables inside a card; do not nest a card in a card.
- Never add a shadow or glow to a card.
