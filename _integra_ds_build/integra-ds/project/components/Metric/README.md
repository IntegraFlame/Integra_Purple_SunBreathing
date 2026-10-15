Three tiles for showing a measured value: the metric box, the gauge card and the lens box.

**Classes:** `ig-metric` with `ig-metric-value` (`--sm`) and `ig-metric-label`; `ig-gauge` with `ig-gauge-value`, `ig-gauge-label`, `ig-gauge-sub`; `ig-lens` with `ig-lens-count`, `ig-lens-name`, `ig-lens-desc`.

**Consumer provides:** a value, a label and, for a gauge, a one-line context caption. Set the value color inline from its meaning.

- Use the metric box for a dense row of system readouts inside a compact card, four across on `ig-grid--4`. The value is `flame-core` unless its meaning sets `sentinel-cyan`, `green` or `red`.
- Use the gauge card for one headline number on a report page: a 2rem Orbitron value, an uppercase label and a caption such as "▼ 0.34% | Complacency Zone (<20)". Lay two or more side by side with a flex row.
- Use the lens box for a count with a name and a short descriptor, six across on `ig-grid--6`. The count is `purple-amethyst`.
- Keep values on one line (`white-space: nowrap`) at a fixed precision.
- The 0.45rem labels are the smallest text in the system; do not go smaller, and do not use them for anything a person must act on.
