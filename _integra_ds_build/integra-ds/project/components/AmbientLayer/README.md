The ambient layer behind dashboards and the logo page: an 80-particle canvas and a pulsing purple glow ring.

**Classes:** `ig-particles` (a `<canvas>`), `ig-glow-ring`, `ig-orbital`.

**Consumer provides:** a `<canvas class="ig-particles">`, a `<div class="ig-glow-ring">` and the particle script. Content sits above them at z-index 2.

- Use it on dashboards and the logo page only. Report pages stay flat `void`.
- Stack it: the canvas at z-index 0, the glow ring at 1, page content at 2. Both layers are `position: fixed` with `pointer-events: none`.
- The script draws 80 particles with a radius of 0.3 to 1.8px and an opacity of 0.1 to 0.5, in `sentinel-cyan`, `purple-neon`, `flame-primary` and `flame-core`; each drifts by up to 0.15px a frame and respawns when it leaves the canvas.
- Keep the ring at 500px, `rgba(157, 0, 255, 0.06)` fading to clear, pulsing over 5s.
- Use `ig-orbital` on a canvas that draws a planetary or orbital diagram: it pulses opacity between 0.7 and 1 over 2s.
- The specimen here stops the particles and the pulse under `prefers-reduced-motion`; do the same in a page script.
