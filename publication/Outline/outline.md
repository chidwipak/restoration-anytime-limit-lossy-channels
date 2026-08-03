# D2 Outline Freeze — one continuous scientific story

Title: Restoration and Reliability: The Exact Moment Threshold for Controlling Expansive Systems over Erasure
Channels

Working abstract target: 150 to 200 words. One paragraph. States the gap (nonlinear plant, random erasure,
moment guarantee), the exact threshold gamma = 1, the two marginals (restoration-entropy rate and top-rate
reliability), the matched necessity and zooming-quantizer achievability with no quasi-conformality, and the
importance-sampling validation.

Section flow (prose only, tables allowed, no lists, no dash connectors):

I. Introduction
   Motivation (an unstable process controlled over a lossy link); the two coupled failures (too little average
   rate, too many consecutive drops); the one-line result gamma = 1; the four contributions; roadmap.

II. Problem Formulation
   The plant as a C1 expansive map on a compact set, the target set, the observer error, the erasure channel,
   m-th-moment set-invariance. Defines the two expansion rates (volume and top), the restoration entropy, and
   the anytime reliability exponent. Ends by asking for the exact stabilizable region.

III. Related Work
   The six strands: data-rate theorems, packet-loss stability, anytime capacity, invariance and restoration
   entropy, nonlinear predictive control, and the mathematical foundations. Ends with the row no prior work
   occupies.

IV. Main Results
   Theorem 1 (necessity D2-star: conditions R and A), Theorem 2 (achievability D2-star-star: the exact gamma = 1
   surface via the universal zooming quantizer), the zero-gap corollary, the independence of R and A, the linear
   sanity check, and the vector two-rate structure. Intuition before formal mathematics.

V. Proof of Necessity
   Strategy paragraph; Lemma 1 (uniform burst expansion), Lemma 2 (renewal moment divergence, including why
   acknowledgment cannot help), Lemma 3 (rate necessity by the law of large numbers and volume counting).

VI. Achievability by the Universal Zooming Quantizer
   Strategy paragraph; Lemma 4 (the common-index zooming quantizer that removes the state-dependent-grid
   obstacle), Lemma 5 (the geometric drift giving stable iff gamma < 1), Lemma 6 (the cat-map verification
   without quasi-conformality); composition.

VII. Surrogates and the Moment Estimator
   The circle map and the cat map as analytic surrogates; why naive Monte Carlo fails on the moment and why the
   exponential-tilt importance sampler is exact. Ends by setting up the experiments.

VIII. Experiments
   Each experiment as prose with why-it-exists, setup, and finding: the phase diagram (Fig. phase), the
   necessity and reliability law with importance sampling (Fig. reliability), the two independent conditions
   (Fig. conditions), the zooming-quantizer achievability (Fig. achievability), the vector two-rate separation
   (Fig. tworate), and the scaling law, universality, non-normal spectral radius, restoration-versus-Lyapunov,
   and correlated bursts summarized in tables. A results-summary table anchors the section.

IX. Discussion and Limitations
   Scope (i.i.d. erasure and uniformly hyperbolic surrogates), the Gilbert-Elliott conjecture and its evidence,
   the modelled anytime code, the non-uniform stress systems, and delay.

X. Conclusion
   The closed loop, the message that average throughput alone is not enough for expansive workloads, and the
   outlook.

Figures (exactly six, each one scientific idea):
   1. System model (TikZ): plant, observer with zooming quantizer, erasure channel, controller, and the two
      requirements.
   2. fig_e4_phase: the exact (p, R) threshold surface gamma = 1 with both marginals (main result).
   3. fig_e1_reliability: naive Monte Carlo fails, importance sampling is exact, and the reliability law
      p_c(m) = e^{-m r star}.
   4. fig_e2_two_conditions: the rate and reliability conditions are distinct transitions.
   5. fig_e5_achievability: the zooming quantizer is faithful and stabilizes below threshold.
   6. fig_m1_two_rates: the volume rate governs bandwidth and the top rate governs reliability.

Tables (unlimited): notation; prior-art matrix; the m-scaling law across surrogates; the results summary; the
universality across five maps; the non-normal spectral-radius comparison.

Writing rules enforced: no itemized lists; no dash sentence connectors; simple English; every figure and table
referenced and explained; every numerical value traceable to resultsD2.md.
