Report prose: dim paragraphs with bright strong words, and three colored emphasis styles for an argument in thesis, antithesis and synthesis.

**Classes:** `ig-prose` (on the wrapper), `ig-thesis`, `ig-antithesis`, `ig-synthesis` (on `<em>`).

**Consumer provides:** paragraphs of text; `<strong>` for the facts a reader should catch.

- Wrap prose in `ig-prose`: `body` type, `monolith-dim` text, a 1.7 line height and a 0.75rem gap between paragraphs.
- Wrap key figures in `<strong>` (`monolith`): "+25 bps to **3.75%–4.00%**".
- Open an argument paragraph with its label in `<em>`: `ig-thesis` (`sentinel-cyan`) for the working view, `ig-antithesis` (`flame-primary`) for the counter-view, `ig-synthesis` (`purple-neon`, bold) for the resolution.
- Write the label with its scope in brackets and a colon: "Thesis (Equities):".
- Use this order only: thesis, antithesis, synthesis. Do not use these colors for emphasis anywhere else.
