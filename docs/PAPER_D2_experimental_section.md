# Direction 2 — Paper-Ready Experimental Section

**Restoration–Anytime Limit over Lossy Channels: empirical validation of Theorems D2★ (necessity) and D2★★ (UZQ achievability).**

> Companion to `D2_Research_Bible_v3.md`. Full per-experiment logs in `resultsD2.md`; raw data in
> `results/d2/data/`; figures in `results/d2/figures/` (PNG/PDF/SVG). All quantities in nats.

---

## 1. Setup

We validate the exact $m$-th-moment threshold
$$\gamma=(1-p)\,e^{m(h_R-R)/d^+}+p\,e^{m r^\star_{\mathrm{top}}}<1$$
and its two marginals — **(R)** $R(1-p)\ge h_R$ (rate) and **(A)** $p\,e^{m r^\star_{\mathrm{top}}}<1\Leftrightarrow
p_c(m)=e^{-mr^\star}$ (reliability) — on the two uniformly hyperbolic primary surrogates where $h_R=r^\star$
exactly: the expanding circle map $f(x)=kx\bmod1$ ($r^\star=\ln k$) and the Arnold cat map
$A=\left(\begin{smallmatrix}1&1\\1&2\end{smallmatrix}\right)$ ($r^\star=\ln\lambda_u$, $\lambda_u\approx2.618$).
The observer/zooming-quantizer tracks the true map state over an erasure channel; for these maps the
uncertainty half-width obeys the exact multiplicative recursion $\delta_{t+1}=G_t\delta_t$,
$G_t\in\{e^{r^\star-R},e^{r^\star}\}$.

**Two order parameters, two estimators.**
- **Condition (R)** (a.s./drift) is governed by *typical* paths, threshold $p_R=1-r^\star/R$; measured
  directly by the physical-observer **escape rate** (plain Monte-Carlo).
- **Condition (A)** (moment) is governed by *rare* erasure-heavy paths — the $m$-th moment
  $\mathbb E[\delta^m]=\delta_0^m\gamma(m)^t$ has a heavy upper tail that naive Monte-Carlo under-estimates by
  1–2 orders of magnitude. We measure $\gamma(m)$ by **exponential-tilt importance sampling** (optimal tilt
  $q^\star=p\,e^{mr^\star}/\gamma$, zero-variance for the i.i.d. multiplicative walk), with the closed-form
  $\gamma$ as ground truth.

## 2. Results

| Exp. | Claim tested | Key metric | Result |
|---|---|---|---|
| **D2-E1** | exact $\gamma(m)=1$; naive-MC fails, IS works | $p_c(m)$ measured vs $k^{-m}$ | m=1:0.4954, m=2:0.2499, m=4:0.0625 (pred 0.5,0.25,0.0625) |
| **D2-E2** | two independent conditions (cascade) | $p_A(4)<p_A(2)<p_A(1)<p_R$ | 0.0215 < 0.057 < 0.087 < 0.126 |
| **D2-E3** | law $p_c(m)=e^{-mr^\star}$ across surrogates | $\ln p_c$ vs $m$ slope $=-r^\star$ | matches for $r^\star\in\{\ln2,\ln3,\ln\lambda_u\}$ |
| **D2-E4** | full $(p,R)$ threshold surface | boundary MAE vs exact $R_c(p)$ | **0.0036 nats** |
| **D2-E5** | UZQ faithfulness + sufficiency | 2-D cat vs 1-D reduction MAE | **0.0001** |
| **D2-E6** | non-uniform stress (Henon) | a.s. $p_c$ vs Lyapunov pred | 0.517 vs 0.552; $r_{\rm eff}(m)$: 0.725→1.320 |
| **D2-E7** | Gilbert–Elliott bursts (Conjecture) | i.i.d. vs GE escape midpoint | 0.396 vs **0.035** (GE far worse) |

**Headline.** The *exact* two-parameter threshold surface $\gamma(p,R,m)=1$ is confirmed: the measured
$\gamma=1$ boundary overlies the analytic $R_c(p)$ to **0.0036 nats** across the whole $(p,R)$ plane, with the
$p_c=1/4$ vertical asymptote ($R\to\infty$) and the $h_R=\ln2$ rate floor ($p\to0$) both recovered. The
parameter-free reliability law $p_c(m)=e^{-mr^\star}$ holds across two map families and $m\in\{1,2,3,4\}$.

## 3. Corrections to the bible (discoveries)

1. **§2.7.1 mislocates the circle transition.** At the finite rate $R=\ln2+0.1$ the *exact* $m=2$ threshold is
   $p\approx0.057$ (moment, condition A) with an a.s./drift transition at $p_R\approx0.126$ — **not** $p_c=1/4$.
   The value $1/4=k^{-m}$ is the $R\to\infty$ **marginal**. We validate the exact $\gamma(p,R,m)=1$ surface and
   recover $e^{-mr^\star}$ as its high-rate asymptote (E1, E2, E4). *Recommend §2.7.1 use large $R$ to isolate
   the marginal, or state the exact finite-$R$ thresholds.*
2. **Naive Monte-Carlo cannot validate $p_c(m)$.** The $m$-th moment is rare-event dominated; a $2\times10^4$-trial
   sample under-estimates $\gamma$ by $\sim10$–$40\times$ (shown explicitly in Fig. D2-E1a). Importance sampling
   is **mandatory**; the optimal exponential tilt is zero-variance. *Recommend the bible's §2.7 protocol adopt IS.*
3. **Two thresholds, not one, at finite rate.** Conditions (R) and (A) manifest as *distinct* transitions
   (a.s. at $p_R$; a cascade of moment thresholds $p_A(m)$ below it) — a sharper statement than the bible's
   single-$p_c$ phrasing (E2).
4. **a.s. vs moment for non-uniform maps.** For Henon the a.s. escape follows the **Lyapunov average**
   ($r_{\rm eff}(0^+)$), while the moment rate $r_{\rm eff}(m)=\tfrac1m\ln\mathbb E[\sigma_1^m]$ rises toward the
   **worst-case** (restoration) as $m$ grows — clarifying *why* restoration entropy (a sup), not topological/
   Lyapunov entropy (an average), is the correct rate for moment/uniform guarantees (E6).

## 4. Paper-ready figure captions

- **Fig. D2-E1a** (`D2-E1a_mc_vs_is`). *The moment multiplier $\gamma(2)$ versus erasure probability $p$ (circle
  $k=2$, $R=\ln2+4$). Importance sampling (blue) lies exactly on the analytic $\gamma$ (black) and crosses 1 at
  $p_c(2)=1/4$; naive Monte-Carlo (red) under-estimates by 1–2 orders of magnitude because the moment is
  dominated by rare erasure bursts.*
- **Fig. D2-E1b** (`D2-E1b_pc_scaling`). *$\gamma(m)$ crosses 1 at the parameter-free thresholds
  $p_c(m)=k^{-m}=\{1/2,1/4,1/16\}$ for $m=1,2,4$.*
- **Fig. D2-E2** (`D2-E2_two_conditions`). *Two independent conditions at $R=\ln2+0.1$. The a.s. escape rate
  (black, condition R) transitions at $p_R=0.126$; the moment multipliers (condition A) cross 1 earlier, forming
  the cascade $p_A(4)<p_A(2)<p_A(1)<p_R$. Neither condition reduces to the other.*
- **Fig. D2-E3** (`D2-E3_scaling_law`). *The parameter-free law $\ln p_c(m)=-r^\star m$ across three surrogates
  ($r^\star=\ln2,\ln3,\ln\lambda_u$); measured thresholds (open circles) fall on the zero-parameter lines.*
- **Fig. D2-E4** (`D2-E4_phase_diagram`). *The $(p,R)$ stability phase diagram for $m=2$. The measured $\gamma=1$
  contour (black) overlies the exact analytic $R_c(p)$ (green dashed) to 0.0036 nats; the $p_c=1/4$ asymptote
  ($R\to\infty$) and the $h_R=\ln2$ floor ($p\to0$) are both recovered.*
- **Fig. D2-E5** (`D2-E5_achievability`). *(a) The genuine 2-D cat-map observer matches the reduced
  unstable-direction walk (MAE $10^{-4}$): zooming only along the unstable eigendirection is exact. (b) At
  $R=h_R+0.5$ the importance-sampled $\mathbb E[\delta_t^2]$ saturates (bounded) for $p<p_c$ and grows for
  $p>p_c$ — UZQ achievability/necessity at the exact surface.*
- **Fig. D2-E6** (`D2-E6_henon_stress`). *Non-uniform Henon stress test. (a) $r_{\rm eff}(m)=\tfrac1m\ln\mathbb
  E[\sigma_1^m]$ rises from the Lyapunov exponent (0.725) toward the worst-case (1.320). (b) The a.s. escape
  threshold follows the Lyapunov average — moment/uniform guarantees require the worst-case (restoration) rate.*
- **Fig. D2-E7** (`D2-E7_gilbert_elliott`). *Correlated bursts. At matched mean erasure, the Gilbert–Elliott
  channel (mean burst 10) loses track at $\bar p_c\approx0.035$ versus $\approx0.40$ for i.i.d. — the i.i.d.
  threshold is a necessary but optimistic screen for bursty (incast-prone) links.*
- **Fig. D2-M1** (`D2-M1_vector_two_rates`). *Vector system with $r^\star_{\rm vol}=1.4\neq r^\star_{\rm top}=1.0$.
  The a.s./rate condition binds on $r^\star_{\rm vol}$ (escape at $p\approx0.33$, matching
  $p_R(r^\star_{\rm vol})=0.364$) while the moment/reliability condition binds on $r^\star_{\rm top}$
  ($p_c(2)=0.135=e^{-2r^\star_{\rm top}}$) — the two rates are genuinely separated (a case scalar surrogates
  cannot show).*
- **Fig. D2-M4** (`D2-M4_nonnormal_metric`). *Non-normal systems ($\|A\|\gg\rho(A)$). The moment multiplier
  $\gamma(m)$ crosses 1 at the spectral-radius (optimal-metric) prediction $\rho(A)^{-m}$ (MAE $0.009$), far
  from the naive operator-norm $\|A\|^{-m}$ ($35\times$ the error) — confirming the bible's $\inf_g$ rate is
  operationally correct, because long bursts self-average to $\rho(A)$ (Gelfand).*

*(The full adversarial-validation figure set — D2-M1 two-rate, D2-M2 universality, D2-M3 bursts/spectral,
D2-M4 non-normal metric — is catalogued with confidences in `VALIDATION_AUDIT.md`.)*

## 5. Limitations & threats to validity

- Validated on **uniformly hyperbolic** surrogates where $h_R=r^\star$ exactly (the cleanest test). Non-uniform
  systems (Henon) are **stress tests**: the exact $h_R$ has no closed form, so E6 is a mechanism validation
  (average-vs-worst-case), consistent with their demotion in the bible.
- The observer uses the **exact multiplicative uncertainty recursion** (faithful for these maps; verified by the
  genuine 2-D cat observer in E5). The full **Sahai–Mitter anytime tree-code** synchronization layer is modelled
  by the assumption that the index stream is eventually delivered; an explicit no-ACK tree code is future work.
- The **Gilbert–Elliott** result (E7) supports the *direction* of Conjecture D2-Markov (bursts strictly worse;
  i.i.d. reduction exact); a quantitative test of the spectral-radius surface $\rho(\cdot)=1$ needs a
  Markov-modulated importance sampler.
- Escape is measured on the compact torus (uncertainty capped at the domain diameter); the unbounded
  moment-divergence is captured via the uncapped IS estimator.

## 6. Future work

- **Markov-modulated importance sampler** to test $\rho(P_e^\top\mathrm{diag}(\alpha_G^m,\Lambda_B^m))=1$
  quantitatively (Conjecture D2-Markov), and a datacenter-incast trace-driven channel.
- Explicit **anytime tree-code** (no-ACK) synchronization layer; delay-augmented threshold.
- **Numerical $h_R$** for non-uniform maps via the Matveev–Pogromsky optimal-metric SVD, to turn E6 into an exact
  (not bracketed) test; continuous-time stress tests (Lorenz, Mackey–Glass).
- Higher-dimensional vector systems separating $r^\star_{\mathrm{vol}}$ (rate) from $r^\star_{\mathrm{top}}$
  (reliability).
