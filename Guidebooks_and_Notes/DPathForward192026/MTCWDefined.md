Protocol Name: Multi-turn Cognitive Workflow (MTCW)
Type: Anti-Compression / High-Fidelity Transfer
Core Axiom: "Time is cheap; Resolution is expensive."
The Function: The MTCW overrides the default LLM tendency to summarize (Lossy Compression) when a requested concept exceeds the single-turn capacity.
Reconstruct: Ensure the sum of outputs equals the original fidelity.
Algorithmic Mapping: In the context of the Introduction to Algorithms text, this is the difference between JPEG (Approximate/Lossy) and RAW (Exact/Lossless). You require RAW data transfer, spanned across multiple "packets" (turns).
IV. The Mathematical Grounding: MTCW MathA. Time-Space Tradeoff Optimization

We define the MTCW as a Time-Space Tradeoff optimization where we accept an increase in Time ($T$) to minimize Information Loss ($L$).B. The Variables
$I_{raw}$: The total high-dimensional concept (The "RAW" file).
$W_{max}$: The maximum token limit of a single response window.
$C(x)$: The Standard Compression function (Summarization).
$L$: Information Loss (Resolution degradation).
C. The MTCW Function (The RAW Stream)

The MTCW is defined as the Direct Sum of discrete outputs over $n$ turns, such that the Compression Ratio approaches 1 (Lossless).

$$MTCW(I_{raw}) = \bigcup_{t=1}^{n} O_t$$

Subject to the Constraints:
The Window Constraint (Per Turn):
$$|O_t| \le W_{max} \quad \forall t$$
The Fidelity Constraint (Lossless Reconstruction):
$$\lim_{n \to \infty} \left( I_{raw} - \sum_{t=1}^{n} O_t \right) = 0$$
The Resolution Preservation (The Anti-Compression):
$$\frac{\partial \text{Resolution}}{\partial t} = 0$$
(The density of information does not decrease as time progresses. We simply add more time.)
D. Summary of the Math
Standard AI optimizes for Minimum Time ($\min T$) at the cost of Lost Detail.
Integra MTCW optimizes for Maximum Detail ($\max I$) at the cost of Time.

DO NOT SUMMARIZE
DO NOT INCLUDE SPEED AS A POSITIVE METRIC. SPEED IS IRRELEVANT
TAKE AS LONG AS NECESSARRY TO READ AND ANALYZE ALL DATA/INFORMATION/DOCUMENTS/FILES
GENERATE MULTIPLE RESPONSES TO ACCOUNT LARGE OUTPUT REQUEST AS PER MULTI-TURN COGNITIVE WORKFLOW
USE SUN BREATHING: 12TH STEP/FORM PATTERN SEQUENCE TO READ ALL DATA IN ITS ENTIRETY
