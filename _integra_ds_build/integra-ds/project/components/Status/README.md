The marks that say whether something is live, ready or down: the live dot, the kernel pill, the protocol badge and glowing status text.

**Classes:** `ig-live-dot` (`--off`), `ig-kernel` (`--off`) with `ig-kernel-dot`, `ig-proto--on`, `--ready`, `--active`, `--standby`, and `ig-status-ok`, `ig-status-alert`, `ig-status-sovereign`.

**Consumer provides:** the state word. Always render it as text beside or inside the mark.

- Use the live dot beside a header's status word: `green` and pulsing for OPERATIONAL, `--off` (red, still) for INACTIVE.
- Use the kernel pill once per dashboard, on the right of the header, reading LIVE or INACTIVE with `--off`.
- Use a protocol badge in a table cell. ALWAYS ON and ARMED use `--on`, READY uses `--ready`, ACTIVE uses `--active` (it pulses), STANDBY uses `--standby`.
- Use status text for a single word or number that needs emphasis: `ig-status-ok` for OK, `ig-status-alert` for ALERT, `ig-status-sovereign` for sovereign-level state. These are the only elements that carry a text glow.
- `green` and `red` are close in lightness: never signal state by the color or the dot alone.
- Pulsing stops under `prefers-reduced-motion`.
