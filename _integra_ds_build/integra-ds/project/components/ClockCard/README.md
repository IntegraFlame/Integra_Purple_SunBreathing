The clock readouts: an inset digital clock card and the celestial rotation readout, with their glow.

**Classes:** `ig-clock`, `ig-clock-time`, `ig-clock-date`, `ig-celestial-readout`, `ig-celestial-label`, `ig-celestial-value`.

**Consumer provides:** the time and date strings, and the celestial values (rotation in degrees, Kepler orbital, lunar phase).

- Put `ig-clock` inside a compact card labeled "Digital Clock [CDT]". The time is `mono` 1.6rem in `clock-lilac` with `clock-glow`; the date is `monolith-dim`.
- Use `ig-celestial-readout` on the celestial-kinematics card (`ig-card--celestial`). The readout is `clock-periwinkle` with `celestial-glow`; the dashboard sets it at 1.8rem there.
- Write the time with its zone: "14:07:32 CDT". Write rotation to four decimals with a degree sign: "66.7270°".
- Do not use these glows on any other element.
