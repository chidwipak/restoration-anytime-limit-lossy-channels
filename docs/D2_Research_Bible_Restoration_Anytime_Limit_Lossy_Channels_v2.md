# D2 Research Bible — Restoration–Anytime Limit over Lossy Channels

**Self-contained research bible for Direction 2. No dependency on File 1.**
**Status:** Terminal pre-experimental. Theorem **D2★** (necessity) is proved at lemma level; **D2★★** (sufficiency) is conditional with a named open observer; the Markov-erasure case is a stated conjecture.
**Convention:** Natural logs ($\ln$, nats) throughout. The per-step **expansion factor** is $\Lambda:=e^{r^\star}$ (a pure ratio, base-free). Rates $R,h_R$ are in nats/use unless $\log_2$ written.

---

## Correction Log

> **[COR-1]** *Doc 2 claimed* Sahai–Mitter anytime capacity is a "category error" to be discarded.
> **Correct claim:** The *linear instantiation* fails for nonlinear flows, but the **reliability** concept is indispensable for stochastic (bursty) loss. It is **reinstated** as condition (A).
> **Replacement:** Theorem **D2★(A)**, §2.3.

> **[COR-2]** *Doc 3 (D2-C) claimed* a single **additive** bound $C> h_R+\Delta(p)$ on the rate.
> **Correct claim:** The binding constraint for $m$-th-moment stability is a **multiplicative reliability** condition $p\,e^{m r^\star}<1$, not an additive rate penalty. The additive form **fails the linear sanity check** (it cannot reproduce $p\lambda^2<1$).
> **Replacement:** Two independent conditions (R) and (A), §2.3.1; sanity check §2.3.6.

> **[COR-3]** *Doc 4 used a single $r^\star$ for both conditions.*
> **Correct claim:** The **rate** condition is governed by the **volume** expansion rate $r^\star_{\mathrm{vol}}$ (restoration entropy = sum of positive log–singular-values); the **reliability/moment** condition is governed by the **top** expansion rate $r^\star_{\mathrm{top}}$ (largest singular value = norm expansion). They **coincide for scalar systems and for both primary surrogates**, but differ for general vector systems.
> **Replacement:** §2.0 (both defined), §2.3.1 (both conditions), §2.3.7 (vector case).

> **[COR-4]** *Doc 3 promoted Lorenz / Mackey–Glass as primary surrogates.*
> **Correct claim:** These are **non-uniformly hyperbolic / infinite-dimensional**, so $h_R\ne r^\star$ and the failure point conflates the channel limit with an entropy-estimation gap. **Demoted to stress tests.**
> **Replacement:** Primary = expanding circle map + cat map (where $h_R=r^\star$ exactly), §2.6.

> **[COR-5]** *Prior documents* propagated unverifiable arXiv IDs; not propagated here. Sahai–Mitter (arXiv cs/0601007) verified live.

---

## Cross-Reference Table

| Object | D2★ role | D1★ role | Relationship |
|---|---|---|---|
| $r^\star_{\mathrm{vol}},h_R$ | **rate condition (R)** | absent | D2-specific |
| $r^\star_{\mathrm{top}},\Lambda$ | **reliability condition (A)** | absent | D2-specific |
| $p$ (erasure prob.) | **central** (both) | absent | D2-specific |
| $m$ (moment order) | **determines $p_c$** | absent | D2-specific |
| $r^\star_{\mathrm{vol}}=r^\star_{\mathrm{top}}=r^\star$ [D2-C5] | **equal for primary surrogates** | — | Circle map: $r^\star=\ln k$ (confirmed §2.6.1). Cat map: $r^\star=\ln\lambda_u$ (confirmed §2.6.2). For these surrogates, use a **single** $r^\star$ in both (R) and (A). For general vector systems, use separate $r^\star_{\mathrm{vol}}=\sup_K\sum_i\log^+\sigma_i$ in (R) and $r^\star_{\mathrm{top}}=\sup_K\log^+\sigma_1$ in (A). |
| $\Gamma_k,\theta_{\mathrm{IB}},E^{\mathrm{cen}}$ | absent | central | D1-specific |
| **Conjecture U** | appendix only | appendix only | unproven bridge |

---

## 2.0 — Notation and Definitions Table

| Symbol | Type | Definition |
|---|---|---|
| $x_{t+1}=f(x_t,u_t)$ | dynamics | Discrete-time controlled system. **[H2-reg]** $f(\cdot,u)\in C^1(K)$ (Jacobian exists & continuous). If only Lipschitz, $Df$ exists a.e. (Rademacher); §2.0-note-Lip states when that suffices. |
| $M$ | Riemannian manifold | State manifold, $\dim M=n$, metric $g$. Euclidean $\mathbb R^n$ unless stated; metric matters only via the $\inf_g$ in $r^\star$ (§2.0-note-metric). |
| $K\subset M$ | compact | Operating region. **[H2-cpt]** compact ⇒ $\sup_{x\in K}$ in $r^\star$ is finite. |
| $Q\subseteq K$ | compact | Target set, **invariant** under ideal feedback (full state, no quantization, no delay): $\exists u^\star(\cdot)$ with $f(Q,u^\star(Q))\subseteq Q$. "Invariant" (not merely forward-invariant) so escape is a well-defined failure. |
| $Df(x)$ | linear map $T_xM\!\to\!T_{f(x)}M$ | Jacobian of $f(\cdot,u^\star)$ (closed-loop ideal map). |
| $\sigma_i(Df(x);g)$ | $\ge0$ | Singular values: $\sqrt{\text{eig}}\big(Df(x)^{*}_g Df(x)\big)$ in metric $g$; $\sigma_1\ge\dots\ge\sigma_n$. |
| $r^\star_{\mathrm{vol}}$ | $[0,\infty)$ | **Volume rate** $\displaystyle r^\star_{\mathrm{vol}}=\inf_{g}\sup_{x\in K}\sum_{i=1}^n\log^+\sigma_i(Df(x);g)$, $\log^+=\max(0,\log)$. Integrand of the Matveev–Pogromsky restoration-entropy estimate. |
| $r^\star_{\mathrm{top}}$ | $[0,\infty)$ | **Top rate** $\displaystyle r^\star_{\mathrm{top}}=\inf_{g}\sup_{x\in K}\log^+\sigma_1(Df(x);g)$. Always $r^\star_{\mathrm{top}}\le r^\star_{\mathrm{vol}}$. For linear $f=A$: $r^\star_{\mathrm{top}}=\log^+\rho(A)$, $r^\star_{\mathrm{vol}}=\sum_i\log^+|\lambda_i(A)|$. |
| $\Lambda$ | $\ge1$ | Top expansion factor $\Lambda:=e^{r^\star_{\mathrm{top}}}$. Scalar: $\Lambda=|\lambda|$. |
| $h_R$ | $[0,\infty)$ | **Restoration entropy** (Matveev–Pogromsky 2019). $h_R\le r^\star_{\mathrm{vol}}$ always; $h_R=r^\star_{\mathrm{vol}}$ for uniformly quasi-conformal $f$. §2.0-def-hR. |
| $h_{\mathrm{top}}$ | $[0,\infty)$ | Topological (feedback) entropy. $h_{\mathrm{top}}\le h_R$ (restoration is the robust/uniform refinement). |
| erasure channel | stochastic | Memoryless: each use delivers $R$ nats w.p. $1-p$, erases w.p. $p$, i.i.d. **[H2-chan]**. ACK: see §2.0-note-ACK. |
| $e_t$ | $\ge0$ | Observer state-estimation error $\mathrm{dist}_g(\hat x_t,x_t)$ (Riemannian distance; Euclidean norm if $M=\mathbb R^n$). |
| $m$-th moment invariance | property | $\limsup_{t\to\infty}\mathbb E\,e_t^{\,m}<\infty$, $m\ge1$ **[H2-m]**. Implies the controlled trajectory stays near $Q$ in $L^m$. |
| $\alpha_{\mathrm{ch}}$ | $>0$ | Channel delay-reliability exponent $=\ln(1/p)$ (a length-$b$ blackout has prob $p^b=e^{-b\alpha_{\mathrm{ch}}}$). Equals the Sahai–Mitter anytime exponent of BEC$(p)$ at low rate (§2.0-note-anytime). |

**§2.0-note-Lip.** When $f$ is only Lipschitz, $Df$ exists a.e. (Rademacher). The **necessity** proof (Lemmas C–D) needs only an a.e. lower bound on expansion plus continuity of the flow, so a.e. existence suffices with $\sup$ replaced by essential-$\sup$. **Sufficiency** (D2★★) uses $C^1$ to build the quantizer; Lipschitz-only sufficiency is open.

**§2.0-note-metric.** $r^\star$ depends on $g$ through $\sigma_i$; the $\inf_g$ removes the dependence and yields the **tight** intrinsic rate. For linear systems the optimal $g$ diagonalizes $A$ and gives $r^\star_{\mathrm{top}}=\log^+\rho(A)$ (spectral radius), $r^\star_{\mathrm{vol}}=\log|\det A_+|$. The $\inf_g$ is achieved when $K$ is compact and $f\in C^1$ (Matveev–Pogromsky; existence of an extremal Riemannian metric via a minimax over the compact set of normalized metrics).

**§2.0-def-hR (restoration entropy, Matveev–Pogromsky 2019, Automatica, Part II).** $h_R$ is the infimal data rate of a coder–observer pair guaranteeing **regular observability**: $\sup_t e_t\le\delta$ for a prescribed $\delta$, **uniformly over initial errors** and robust to bounded disturbance. Their estimate: $h_R\le\inf_g\sup_{x\in K}\sum_i\log^+\sigma_i(Df(x);g)=r^\star_{\mathrm{vol}}$, with equality under uniform quasi-conformality $\sigma_1(Df)=\dots=\sigma_n(Df)$ on $K$. **Contrast with $h_{\mathrm{top}}$:** topological entropy averages expansion along orbits (Pesin: $h_\mu=\sum\lambda_i^+$ for an ergodic $\mu$); restoration entropy takes the **uniform supremum**, which is exactly what is needed for worst-case burst bounds (§2.3.2). Hence $h_{\mathrm{top}}\le h_R\le r^\star_{\mathrm{vol}}$, generically with strict first inequality for non-uniformly hyperbolic systems.

**§2.0-note-ACK.** Two information structures: **(no-ACK)** controller does not learn which slots were erased; **(causal-ACK)** controller learns the erasure indicator of slot $t$ at time $t$. We prove **necessity (A) for both** (§2.3.3); ACK can only help *achievability*. Shannon: feedback/ACK does **not** raise the capacity of a memoryless channel, so the rate condition (R) is identical with or without ACK.

**§2.0-note-anytime.** Sahai–Mitter define anytime reliability $\alpha$: $\Pr[\text{bit decoded $d$ ago is wrong}]\le K e^{-\alpha d}$. For BEC$(p)$, the dominant low-rate error event is a length-$d$ erasure blackout, prob $p^d=e^{-d\ln(1/p)}$, so the channel's intrinsic delay-reliability exponent is $\alpha_{\mathrm{ch}}=\ln(1/p)$. Sahai–Mitter's $m$-th-moment stabilization condition $\alpha>m\,r^\star$ (linear: $m\log|\lambda|$) becomes $\ln(1/p)>m\,r^\star_{\mathrm{top}}\Leftrightarrow p\,e^{m r^\star_{\mathrm{top}}}<1$ — **identical to (A)**.

---

## 2.1 — Scientific Problem Statement

**(a) Colloquial (SIGCOMM/NSDI register).** Given a distributed computational process whose internal state evolves as an expansive dynamical system $f$ on a compact state space $K$, what minimum communication **bandwidth and reliability** must the network provide for the process to stay within a valid region $Q$ in the $m$-th-moment sense? We prove the answer is governed by **two** computable invariants: the **restoration entropy** of $f|_Q$ (a Lyapunov/SVD-based volume rate) for *bandwidth*, and a **reliability exponent** set by the erasure probability and moment order for *burst survival*. Classical transport guarantees the first only; the second is what fails under loss.

**(b) Mathematical.** Under [H2-reg]–[H2-m] and [H2-chan], determine necessary-and-sufficient $(R,p)$ for $\limsup_t\mathbb E\,e_t^m<\infty$ with controlled set-invariance of $f$ relative to $Q$.

*(No "AI/LLM/semantic" vocabulary appears below this line in any theorem or proof, per the global standard.)*

---

## 2.2 — Literature Review and Prior-Art Matrix

### Data-rate theorems (foundational)
- **Tatikonda–Mitter (2004), *Control under communication constraints*, IEEE-TAC.** *Exact:* LTI mean-square stabilization over a noiseless rate-$R$ channel iff $R>\sum_i\log^+|\lambda_i(A)|=\log|\det A_+|$. *Assumptions:* no channel noise, no loss. *Gap:* deterministic channel only. *Recovered by D2★:* $p=0$, condition (R) ⇒ $R\ge r^\star_{\mathrm{vol}}$ (§2.3.6).
- **Nair–Evans (2004), SIAM JCO; Nair–Evans–Mareels–Moran (2004), IEEE-TAC (*Topological feedback entropy*).** *Exact:* minimal rate for set-invariance of nonlinear $f$ = TFE $h_{\mathrm{top}}$. *Assumptions:* deterministic channel, no loss. *Why TFE fails under erasure:* TFE controls a *single* orbit's distinguishability; a packet drop magnifies the **initial** estimation error without bound because TFE has no uniform/robust margin (Matveev–Pogromsky 2016 give the explicit failure). *Use in D2★:* the **volume-counting** technique of NEMM is the engine of Lemma C, but with $\sup_K$ (restoration) replacing the orbit average.

### Erasure-channel stability (linear)
- **Sinopoli et al. (2004), IEEE-TAC (*Kalman filtering with intermittent observations*).** *Exact:* a critical arrival probability $\lambda_c$ exists s.t. expected error covariance is bounded iff arrival $>\lambda_c$; for scalar unstable $|\lambda|$, the second-moment threshold is the **erasure** $p<1/\lambda^2$. *Assumptions:* estimation (not control), Gaussian. *Recovered:* §2.3.6 scalar $m=2$.
- **Elia (2005), *Remote stabilization over fading/erasure channels*.** *Exact:* scalar mean-square stabilizability iff $p\,|\lambda|^2<1$ (the second moment of the multiplicative gain must contract). *Recovered exactly:* (A) at $m=2$.
- **Gupta et al. (2007) (networked estimation/control with packet loss; Gupta–Hassibi–Murray line).** *Exact:* vector extensions; the most-unstable mode dominates the second-moment threshold. *Recovered:* §2.3.7 ($p\,\rho(A)^2<1$).
- **You–Xie (2011), Automatica (*Minimum data rate for MS stabilization over lossy channels*).** *Exact:* for Markov packet loss, MS stabilizability is a **spectral-radius** condition $\rho\big(P_e\otimes(A\otimes A)\big)<1$ combined with a rate condition. *Recovered/extended:* the i.i.d. case is the rank-one specialization; the nonlinear analog is **Conjecture D2-Markov** (§2.5).

### Anytime capacity
- **Sahai–Mitter (2006/2007; arXiv cs/0601007).** *Exact:* stabilizing an unstable **scalar/vector linear** plant over a noisy link requires **anytime capacity** at rate $>\log|\lambda|$ and reliability $\alpha>m\log|\lambda|$ for $m$-th-moment stability; sufficiency under rich feedback. *Why it does not extend to nonlinear directly:* the exponential tail bound assumes a **constant** gain $\lambda$; with state-dependent Jacobians the per-burst expansion varies, so the linear anytime exponent is ill-defined. *Gap filled by D2★:* replace the constant $\log|\lambda|$ by the **uniform** $r^\star_{\mathrm{top}}$ (top) and $r^\star_{\mathrm{vol}}$ (rate).
- **Simşek–Jain–Varaiya (2004); Sukhavasi–Hassibi (2011) anytime codes.** *Exact:* constructions achieving anytime reliability over erasure/AWGN. *Use:* the achievability code layer in D2★★.
- **Quevedo–Nešić (2012), Automatica (packetized predictive control of nonlinear systems, Markov loss).** *Exact:* ISS-type stability under Markov drops for nonlinear plants with a predictive buffer. *Assumptions:* bounded model, predictive packetization. *Gap:* gives sufficient ISS conditions, **not** a tight rate/reliability *necessity* in terms of an intrinsic entropy; D2★ supplies the necessity and the entropy invariant.

### Restoration entropy
- **Matveev–Pogromsky (2016, Automatica, Part I).** *Exact:* observation of nonlinear systems over finite-capacity channels; constructive coder; restoration-entropy notion. *Use:* the achievability quantizer (D2★★).
- **Matveev–Pogromsky (2019, Automatica, Part II).** *Exact:* tight $h_R$ bounds via SVD/second Lyapunov method; sufficient condition $h_R=r^\star_{\mathrm{vol}}$ (uniform quasi-conformality). *Use:* defines $h_R$, condition (R).
- **Tong–Zamani et al. (NSF PAR 10415513), modular restoration entropy via dissipativity.** *Exact:* compositional upper bounds on $h_R$ for interconnected subsystems via dissipativity + distributed optimization. *Open:* strongly-coupled high-dim systems give conservative bounds (§2.11).

### Stochastic nonlinear control / quantization
- **Liberzon–Nair (2007+); Baillieul (2002–05).** *Exact:* data-rate requirements for nonlinear quantized control; Baillieul gives rate conditions for nonlinear stabilization. *Stochastic channels?* Largely **deterministic** rate; Baillieul does not treat random erasure with moment guarantees. *Gap:* D2★ is the erasure+moment+restoration synthesis.

### Summary matrix
| Paper | nonlinear | stochastic loss | moment stability | restoration (vs TFE) | achievability |
|---|:--:|:--:|:--:|:--:|:--:|
| Tatikonda–Mitter '04 | ✗ | ✗ | MS | — | ✓ |
| Nair–Evans(–MM) '04 | ✓ | ✗ | set-inv | TFE | ✓ |
| Sinopoli '04 / Elia '05 | ✗ | ✓ | MS | — | ✓ |
| You–Xie '11 | ✗ | ✓ (Markov) | MS | — | ✓ |
| Sahai–Mitter '06 | ✗ | ✓ (noisy) | $m$-th | — | ✓ |
| Matveev–Pogromsky '19 | ✓ | ✗ | set-inv | **restoration** | ✓ |
| Quevedo–Nešić '12 | ✓ | ✓ (Markov) | ISS | — | ✓(suff.) |
| **D2★ (this file)** | **✓** | **✓** | **$m$-th** | **restoration** | **✓ conditional (§2.4)** |

D2★ is the first row addressing all five (achievability conditional on §2.4.3's observer).

---

## 2.3 — Theorem D2★: Statement and Complete Proof Roadmap

### 2.3.1 Formal statement
**Hypotheses.** [H2-1] $f(\cdot,u^\star)\in C^1(K)$; [H2-2] $K\subset\mathbb R^n$ (or compact $M^n$) compact; [H2-3] $Q\subseteq K$ compact, invariant under ideal feedback; [H2-4] $f$ **expansive**: $r^\star_{\mathrm{top}}>0$ (some direction expands uniformly — strictly weaker than "every point unstable"); [H2-5] channel memoryless erasure, $p\in(0,1)$, no-ACK (or ACK, §2.3.3); [H2-6] observer/controller causally separated, information structure fixed per §2.0-note-ACK; [H2-7] $m\ge1$.

> **Theorem D2★ (Restoration–Anytime Necessity).** Under [H2-1]–[H2-7], $m$-th-moment controlled set-invariance requires **both**:
> $$\boxed{\;\textbf{(R)}\quad R\,(1-p)\ \ge\ h_R(f|_Q)\qquad\big(\,h_R\le r^\star_{\mathrm{vol}}\,\big)\;}$$
> $$\boxed{\;\textbf{(A)}\quad p\,e^{\,m\,r^\star_{\mathrm{top}}}\ <\ 1\quad\Longleftrightarrow\quad \alpha_{\mathrm{ch}}=\ln\tfrac1p\ >\ m\,r^\star_{\mathrm{top}}\;}$$
> If **(A)** fails, then for **every** causal coder/quantizer/controller, $\displaystyle\limsup_t\mathbb E\,e_t^{m}=\infty$ and $\Pr[\text{escape from any fixed nbhd of }Q]\to1$.
> **Almost-sure corollary:** (R) alone is necessary for a.s. (recurrence/tightness) invariance; the burst margin (A) is the *moment* refinement and is not needed for a.s. boundedness.

**Scalar/surrogate collapse.** For scalar systems and for both primary surrogates (§2.6) $r^\star_{\mathrm{top}}=r^\star_{\mathrm{vol}}=:r^\star$, so (R)$\to R(1-p)\ge\log k$ and (A)$\to p\,e^{mr^\star}<1$.

### 2.3.2 Lemma C — Uniform Burst Expansion (complete proof)
> **Lemma C.** During a length-$b$ erasure burst (no control delivered), the observer's uncertainty set $\mathcal U$ satisfies, for the closed-loop ideal map $f$,
> $$\mathrm{diam}\,f^b(\mathcal U)\ \ge\ \mathrm{diam}(\mathcal U)\cdot e^{\,b\,r^\star_{\mathrm{top}}(1-o(1))},\qquad \mathrm{Vol}\,f^b(\mathcal U)\ \ge\ \mathrm{Vol}(\mathcal U)\cdot e^{\,b\,r^\star_{\mathrm{vol}}(1-o(1))},$$
> uniformly over the location of $\mathcal U$ in $K$.

*Proof.*
**Step 1 (volume).** By the change-of-variables formula on the Riemannian manifold, $\mathrm{Vol}\,f^b(\mathcal U)=\int_{\mathcal U}\prod_{s=0}^{b-1}|\det Df(x_s)|\,d\mathrm{Vol}$. Since $|\det Df(x)|=\prod_i\sigma_i(Df(x))\ge\prod_i\max(1,\sigma_i)=e^{\sum_i\log^+\sigma_i(Df(x))}$ on the expanding part, and taking the optimal metric $g^\star$ achieving the $\inf_g$, $\sum_i\log^+\sigma_i(Df(x);g^\star)\le r^\star_{\mathrm{vol}}$ with the $\sup_K$ attained; the **uniform** bound gives $\prod_{s}|\det Df(x_s)|\ge e^{b\,r^\star_{\mathrm{vol}}(1-o(1))}$ **regardless of the orbit** $\{x_s\}\subset K$. This uniformity is the crux: it holds because $r^\star_{\mathrm{vol}}$ is a $\sup_K$, not an orbit average — contrast a Lyapunov/Pesin average, which would only hold for typical orbits, not the worst burst.
**Step 2 (diameter from top direction).** The image $f^b(\mathcal U)$ contains a segment stretched by $\prod_{s}\sigma_1(Df(x_s))\ge e^{b\,r^\star_{\mathrm{top}}(1-o(1))}$ along the most-expanding direction (choose two points of $\mathcal U$ separated along the top singular direction; their images separate by the product of top singular values). Hence $\mathrm{diam}\,f^b(\mathcal U)\ge\mathrm{diam}(\mathcal U)e^{b r^\star_{\mathrm{top}}(1-o(1))}$.
**Step 3 (diameter ↔ volume, why $r^\star$ not $h_{\mathrm{top}}$).** For the **rate** necessity one uses volume (Step 1) via the isodiametric inequality $\mathrm{diam}\ge c(n)\mathrm{Vol}^{1/n}$, recovering the Nair–Evans counting that forces $\ge h_R$ bits to re-compress; for the **moment** necessity one uses diameter directly (Step 2). Topological entropy $h_{\mathrm{top}}$ counts distinguishable **orbits**, not the volume/Jacobian expansion, so it is the wrong object here; the Jacobian-singular-value rate $r^\star$ is exactly the volume/length expansion rate (classical: Oseledets/SVD growth; cf. Katok–Hasselblatt Prop. for $\det Df$ volume growth).
**Step 4 (the $o(1)$ term).** For uniformly hyperbolic / quasi-conformal $f$, $o(1)=0$ (no sub-exponential correction). For general $C^1$ $f$ there may be sub-exponential corrections to each factor. **These do not affect the conclusion of Lemma D**: the series $\sum_b p^b e^{m r^\star_{\mathrm{top}}b}$ converges/diverges by the **ratio test** at ratio $p\,e^{m r^\star_{\mathrm{top}}}$, which is unchanged by sub-exponential per-term factors $e^{o(b)}$ (ratio of consecutive $o(b)$ terms $\to1$). Hence the threshold is robust to the $o(1)$. $\;\blacksquare$

### 2.3.3 Lemma D — Renewal Moment Divergence (complete proof)
> **Lemma D.** If $p\,e^{m r^\star_{\mathrm{top}}}\ge1$ then $\limsup_t\mathbb E\,e_t^m=\infty$, for every causal scheme, with or without ACK.

*Proof.*
**Step 1 (burst law).** In i.i.d. erasure, runs of consecutive erasures have $\Pr[\text{run}=b]=(1-p)p^b$ (geometric), $\mathbb E[b]=p/(1-p)$. Runs recur infinitely often a.s.
**Step 2 (post-burst error).** At a burst start the error is at least the quantizer floor $\varepsilon_0>0$ (no scheme has zero error with finite rate). By Lemma C, after a length-$b$ burst $e\ge \varepsilon_0 e^{b r^\star_{\mathrm{top}}(1-o(1))}$ (the estimator cannot resolve within the uncertainty set, so $e\ge\tfrac12\mathrm{diam}$).
**Step 3 (moment contribution).** $\mathbb E[e^m\mid\text{burst }b]\cdot\Pr[\text{burst }b]\ge \varepsilon_0^m e^{m r^\star_{\mathrm{top}}b(1-o(1))}(1-p)p^b$.
**Step 4 (series).** Summing, $\mathbb E\,e^m\gtrsim\varepsilon_0^m(1-p)\sum_b\big(p\,e^{m r^\star_{\mathrm{top}}}\big)^b e^{-m r^\star_{\mathrm{top}}o(b)}$, which **diverges iff $p\,e^{m r^\star_{\mathrm{top}}}\ge1$** (ratio test; Step 4 of Lemma C handles $o(b)$).
**Step 5 (between-burst contraction cannot save it).** Each delivered slot conveys $\le R$ nats, contracting $e$ by at most $e^{-R}$ per slot (an information-theoretic floor: one cannot reduce a $d$-bit uncertainty by more than the bits received). Between two bursts there are geometrically many ($\sim1/p$ mean) delivered slots, contributing a **finite** expected contraction factor $\le e^{-R/p}$ per cycle; a fixed finite factor multiplying a divergent geometric series in burst length cannot render it convergent (the divergence is driven by the heavy tail $p^b e^{m r^\star_{\mathrm{top}}b}$ at large $b$, where no bounded between-burst contraction applies).
**Step 6 (ACK / pre-conditioning — the critical issue, resolved).** Suppose causal-ACK: the controller knows each slot's erasure indicator at time $t$. Can it pre-shrink $e$ before a burst to avoid divergence? **No.** (i) Future erasures are **independent of the past** (memoryless), so burst onset/length is **unpredictable**; the controller cannot allocate extra rate "before" a burst it cannot foresee. (ii) Even an optimal controller holding $e$ at the floor $\varepsilon_0$ between bursts still enters each burst at $e\ge\varepsilon_0$, and Lemma C then applies. (iii) **Borel–Cantelli:** for any $b_0$, $\sum_b\Pr[\text{a given run}\ge b_0]=\infty$ over the infinitely many runs (independent), so runs of length $\ge b_0$ occur infinitely often a.s.; choosing $b_0$ large makes the per-occurrence moment contribution $\ge\varepsilon_0^m e^{m r^\star_{\mathrm{top}}b_0}$ arbitrarily large, infinitely often ⇒ $\limsup_t\mathbb E\,e_t^m=\infty$. ACK changes the *achievable code* (enables ARQ) but not this necessity, because capacity is feedback-invariant (memoryless) and burst unpredictability is feedback-invariant. $\;\blacksquare$

### 2.3.4 Lemma R — Rate Condition Necessity [D2-C4]
> **Lemma R.** If $R\,(1-p)<h_R(f|_Q)$, then $\limsup_t\mathbb E[e_t^m]=\infty$ for every causal coding and control scheme. Moreover, a.s. (almost-sure) escape from any fixed neighborhood of $Q$ occurs.

*Proof.*
**Step 1 (delivered bit count).** Under i.i.d. erasures, the number of delivered nats over $n$ steps is $D_n=R\sum_{t=1}^n\mathbf 1\{\text{delivered}_t\}$. Since $\{\mathbf 1\{\text{delivered}_t\}\}$ is i.i.d. Bernoulli$(1-p)$, by the Strong Law of Large Numbers $D_n/n\to R(1-p)$ almost surely.
**Step 2 (volume counting on the delivered sequence).** Apply the Matveev–Pogromsky (2019, Automatica Part II) volume-counting necessity argument to the **realized** delivery sequence: over any $n$ steps with $D_n$ total delivered nats, the observer receives at most $D_n$ nats of state information, while the uncertainty set grows by a factor $\ge e^{\,n\,r^\star_{\mathrm{vol}}(1-o(1))}$ (Lemma C, volume branch), requiring at least $n\,h_R(1-o(1))$ nats to maintain bounded volume. If $D_n<n\,h_R(1-o(1))$, the volume is unbounded, and consequently the estimation error is unbounded.
**Step 3 (a.s. instability).** By Step 1, $D_n/n\to R(1-p)<h_R$ a.s.; hence for large enough $n$ (a.s.), $D_n<n\,h_R(1-\epsilon)$ for some $\epsilon>0$. By Step 2 the uncertainty volume grows unboundedly, giving $e_t\to\infty$ a.s.
**Step 4 (from a.s. to moment divergence).** A.s. divergence $e_t\to\infty$ implies $\limsup_t\mathbb E[e_t^m]=\infty$ by Fatou's lemma applied to $e_t^m\to\infty$ a.s. $\;\blacksquare$

*Note.* The application of MP to the random delivery sequence is valid because (i) the counting argument (Step 2) is deterministic given the realized delivery pattern; (ii) the SLLN (Step 1) makes the realized count a.s. equal to its average. The ergodic substitution $R\mapsto R(1-p)$ is thus **not an approximation but an exact a.s. statement**. The fluctuation of arrivals is a second-order effect that (A), not (R), governs.

### 2.3.5 (R) and (A) are independent necessary conditions
- **(R) holds, (A) fails ⇒ unstable.** Scalar $\lambda=2$, $m=2$, $r^\star=\ln2$. Pick $R=100$ (so $R(1-p)\ge\ln2$ trivially) and $p=0.3>0.25=p_c$. Then (A) fails and Lemma D gives $\mathbb E\,e^2\to\infty$. So (R) does not imply (A).
- **(A) holds, (R) fails ⇒ unstable.** Same system, $p=10^{-3}$ (so $p\lambda^2=0.004<1$, (A) holds), but $R=0.1<\ln2\approx0.693$. Then (R) fails; §2.3.4 ⇒ the average rate cannot cover $h_R$, error grows a.s. So (A) does not imply (R).
- **Conclusion:** neither implies the other; both are independently necessary. This is the structural advance over prior work, where only one condition appears (rate-only in TFE/data-rate theorems; reliability-only in Sahai–Mitter's fixed-rate setting). $\;\blacksquare$

### 2.3.6 Linear sanity check (mandatory; passes)
Scalar $f(x)=\lambda x$, $|\lambda|>1$, $K$ a bounded interval (operating region; expansion uniform):
- $r^\star_{\mathrm{top}}=r^\star_{\mathrm{vol}}=\ln|\lambda|$, $h_R=\ln|\lambda|$ (1-D ⇒ conformal ⇒ $h_R=r^\star_{\mathrm{vol}}=h_{\mathrm{top}}$).
- **(R):** $R(1-p)\ge\ln|\lambda|$ ⇒ at $p=0$, $R\ge\ln|\lambda|$ = **Tatikonda–Mitter / Nair–Evans** data-rate theorem. ✓
- **(A):** $p\,|\lambda|^m<1$. For $m=2$: $p<1/\lambda^2$ = **Elia (2005)**, = **Sinopoli (2004)** second-moment threshold. ✓ For $m=1$: $p<1/|\lambda|$ (first-moment stability; present in the fading-channel literature). For anytime: $\ln(1/p)>m\ln|\lambda|$ = **Sahai–Mitter**. ✓
- **Both classical results recovered exactly; the additive form $h_R+\Delta(p)$ of Doc 3 cannot reproduce $p\lambda^2<1$ (it would predict a rate offset, not a probability threshold) — confirming [COR-2].**

### 2.3.7 Vector extension
$f(x)=Ax$ on $\mathbb R^n$:
- **Rate:** $r^\star_{\mathrm{vol}}=\sum_i\log^+|\lambda_i(A)|=\log|\det A_+|$; (R): $R(1-p)\ge\log|\det A_+|$. (Sum over unstable modes — all must be encoded.)
- **Reliability:** $r^\star_{\mathrm{top}}=\inf_g\sup\log^+\sigma_1(Df;g)=\log^+\rho(A)$ (the $\inf_g$ tightens the operator norm $\|A\|$ down to the spectral radius $\rho(A)$; this is why the metric optimization is essential). Condition (A): $p\,\rho(A)^m<1$. For $m=2$: $p\,\rho(A)^2<1$ = **You–Xie (2011) i.i.d. specialization** and Gupta et al. (most-unstable mode dominates the second moment). ✓
- **Note (operator norm vs spectral radius):** the spec's candidate $p\,\|A\|^m<1$ is the *metric-dependent loose* version; the **tight** condition uses $\rho(A)$ via the optimal metric. Diagonal example $A=\mathrm{diag}(\lambda_1,\lambda_2)$, $|\lambda_1|>|\lambda_2|>1$: each mode independently needs $p\lambda_i^2<1$, binding at $\lambda_1=\rho(A)$ ⇒ $p\rho(A)^2<1$. ✓
- **Nonlinear vector:** $r^\star_{\mathrm{top}}=\inf_g\sup_{x\in K}\log^+\sigma_1(Df(x);g)$; (A) $p\,e^{m r^\star_{\mathrm{top}}}<1$ uses the worst-case top expansion. **Tightness:** this is exact for necessity (the worst burst hits the worst state by uniformity); for sufficiency the worst-case may be conservative (§2.4).

---

## 2.4 — Theorem D2★★: Sufficiency (conditional)

### 2.4.1 Statement
**Extra hypothesis [H-QC]:** $f|_Q$ is **uniformly quasi-conformal** ($\sigma_1(Df)=\dots=\sigma_n(Df)$ on $Q$), so $h_R=r^\star_{\mathrm{vol}}$ and $r^\star_{\mathrm{top}}=\tfrac1n r^\star_{\mathrm{vol}}$ (isotropic; for $n=1$ trivially holds).
**[H-NoACK] [D2-C2]:** No acknowledgment is available at the encoder (the tree-code construction makes this unnecessary).
> **Theorem D2★★.** If (R) and (A) hold **strictly** and [H-QC] and [H-NoACK] hold, there exists a scheme (restoration-rate successive-refinement quantizer ∘ Sahai–Mitter anytime tree code over BEC$(p)$, no ACK) achieving $m$-th-moment controlled set-invariance.

### 2.4.2 Construction (implementable)
- **Step 1 — restoration-rate quantizer.** Per delivered slot, transmit a rate-$R$ successive-refinement quantization of $\hat x_t$; under [H-QC] a lattice/successive-refinement codebook achieves per-slot error contraction $e^{-R}$ (Matveev–Pogromsky 2016 achievability; Liberzon–Nair lattice quantizer).
- **Step 2 — anytime tree code over BEC (no ACK required) [D2-C2].** Wrap the quantizer stream in a tree code achieving anytime reliability over BEC$(p)$ — specifically, the Sahai–Mitter tree code (Sahai–Mitter 2006, arXiv cs/0601007 Part I, Theorem 1) achieves anytime reliability exponent $\alpha$ up to $\alpha_{\mathrm{ch}}=\ln(1/p)$ for the BEC **without requiring acknowledgment (ACK)**. The tree code operates causally: at each time $t$ the encoder outputs a codeword that is a deterministic function of the source symbols up to time $t$, and the decoder produces an estimate of each past source symbol that improves with delay, with error probability decaying as $e^{-\alpha\cdot\mathrm{delay}}$ for any $\alpha<\alpha_{\mathrm{ch}}=\ln(1/p)$.
- **ACK setting (D2★★-ACK):** if causal ACK is available, a simpler ARQ/HARQ scheme achieves the same reliability exponent with lower complexity. The theorem holds in **both** settings; the no-ACK version (tree code) is the canonical and more general result.
- **Step 3 — composition: Lyapunov drift for bounded $m$-th moment [D2-C1].** Let $V(e)=e^m$ be the Lyapunov function; compute the one-step drift $\mathbb E[V(e_{t+1})\mid e_t]$ in two cases. **(a) Delivered slot (prob $1-p$):** the observer receives $R$ nats; under [H-QC] the successive-refinement quantizer contracts the error by $e^{-R}$ while the one-step flow expands by $e^{r^\star_{\mathrm{vol}}}$ (volume) / $e^{r^\star_{\mathrm{top}}}$ (top direction), so with $R>h_R=r^\star_{\mathrm{vol}}$ (strict (R)) the net per-step contraction is $\alpha:=e^{r^\star_{\mathrm{vol}}-R}<1$, giving $\mathbb E[V(e_{t+1})\mid e_t,\text{delivered}]\le\alpha^m V(e_t)$. **(b) Erased slot (prob $p$):** no information is received; by Lemma C $e_{t+1}\le e_t\,\Lambda$ with $\Lambda:=e^{r^\star_{\mathrm{top}}}$, giving $\mathbb E[V(e_{t+1})\mid e_t,\text{erased}]\le\Lambda^m V(e_t)$. Combining,
$$\mathbb E[V(e_{t+1})\mid e_t]\le\big[(1-p)\alpha^m+p\,\Lambda^m\big]V(e_t)=:\gamma\,V(e_t).$$
Bounded $m$-th moment requires $\gamma:=(1-p)\alpha^m+p\Lambda^m<1$. Since $\alpha<1$, $(1-p)\alpha^m\in(0,1-p)$, so a sufficient condition is $p\Lambda^m<1$, i.e. $p\,e^{m r^\star_{\mathrm{top}}}<1$ — exactly condition (A). More precisely $\gamma=(1-p)e^{m(r^\star_{\mathrm{vol}}-R)}+p\,e^{m r^\star_{\mathrm{top}}}$; under strict (R) and (A) both summands are $<1$ and $\gamma<1$. With the bounded per-step quantizer floor $b$ (the finite-rate residual error re-injected each slot), the geometric-drift criterion (Meyn–Tweedie, *Markov Chains and Stochastic Stability*, Thm 15.0.1) gives $\mathbb E[V(e_t)]\le\gamma^t V(e_0)+\tfrac{b}{1-\gamma}$, hence $\limsup_t\mathbb E[e_t^m]\le \tfrac{b}{1-\gamma}<\infty$, establishing $m$-th-moment controlled set-invariance. $\;\blacksquare$

  **Quantitative degradation note [D2-C1].** The drift gives the explicit bound $\limsup_t\mathbb E[e_t^m]\le b/(1-\gamma)$ with $\gamma=(1-p)e^{m(r^\star_{\mathrm{vol}}-R)}+p\,e^{m r^\star_{\mathrm{top}}}$; as $(p,R)$ approach the stability boundary ($\gamma\to1$) the moment bound diverges, which gives a quantitative prediction for the approach to instability in experiments D2-E1 and D2-E4.

### 2.4.3 The open nonlinear anytime observer
**Known achievable:** linear (Kalman + lattice); uniformly quasi-conformal [H-QC] (MP); uniformly hyperbolic attractors with smooth stable foliation (achievable via Markov-partition symbolic coding — cited where available).
**OPEN:** general $C^1$ expansive $f$ with **non-uniform** singular values across $K$. **Exact difficulty:** the optimal codebook is **state-dependent** ($Df(x)$ varies), but the observer only has an *estimate* of $x$; a fixed codebook cannot achieve $h_R$ everywhere, and a state-adaptive codebook risks a chicken-and-egg error (need $x$ to choose the code, need the code to estimate $x$). **Weakest closing assumption:** a uniform *modulus of continuity* on $x\mapsto Df(x)$ plus a margin $R(1-p)>h_R+\eta$ allowing a "universal" codebook robust to codebook mismatch. **Likely techniques:** universal source coding / Lempel–Ziv-type adaptivity for the codebook (Zhang–Berger mismatched quantization), and Krichevsky–Trofimov universal lattices; conjecturally close the gap with an $O(\eta)$ rate overhead.

---

## 2.5 — Markov-Erasure Generalization (partially open)

### 2.5.1 Gilbert–Elliott model
2-state chain Good/Bad, transition $P_e=\left(\begin{smallmatrix}1-p_{GB}&p_{GB}\\p_{BG}&1-p_{BG}\end{smallmatrix}\right)$, erasure probs $\varepsilon_G<\varepsilon_B$. Stationary erasure $\pi_e=\frac{p_{GB}}{p_{GB}+p_{BG}}\varepsilon_B+\dots$; bursts are longer than i.i.d. with the same mean.

### 2.5.2 Conjecture D2-Markov [D2-C3]
> **Conjecture D2-Markov.** Under the Gilbert–Elliott channel with transition matrix $P_e$, where the **Good** state = delivery (error contracts by factor $\alpha_G=e^{r^\star_{\mathrm{vol}}-R}$) and the **Bad** state = erasure (error expands by factor $\Lambda_B=e^{r^\star_{\mathrm{top}}}$), $m$-th-moment controlled set-invariance of nonlinear $f$ requires
> $$\rho\!\Big(P_e\cdot\mathrm{diag}\big(\alpha_G^m,\ \Lambda_B^m\big)\Big)<1,\qquad\text{i.e.}\quad \rho\!\Big(P_e\cdot\mathrm{diag}\big(e^{m(r^\star_{\mathrm{vol}}-R)},\ e^{m r^\star_{\mathrm{top}}}\big)\Big)<1.$$

**Verification of i.i.d. reduction.** For i.i.d. loss, $P_e=\left(\begin{smallmatrix}1-p&p\\1-p&p\end{smallmatrix}\right)$ (rank-one, rows $[1-p,p]$); its only nonzero eigenvalue gives $\rho\big(P_e\,\mathrm{diag}(\alpha_G^m,\Lambda_B^m)\big)=(1-p)\alpha_G^m+p\Lambda_B^m$. Stability $(1-p)e^{m(r^\star_{\mathrm{vol}}-R)}+p\,e^{m r^\star_{\mathrm{top}}}<1$ then reduces: as $R\to\infty$, to $p\,e^{m r^\star_{\mathrm{top}}}<1$ — **condition (A)** ✓; at $p=0$, to $e^{m(r^\star_{\mathrm{vol}}-R)}<1\Leftrightarrow R>r^\star_{\mathrm{vol}}$ — **condition (R)** ✓. (It also matches the D2★★ drift coefficient $\gamma$ of §2.4.2.)

**Verification of You–Xie reduction (linear $f$).** For $f(x)=Ax$: $r^\star_{\mathrm{vol}}=\log|\det A_+|$, $r^\star_{\mathrm{top}}=\log\rho(A)$, so $\alpha_G=|\det A_+|\,e^{-R}$ (delivery: encode at rate $R$, net expansion) and $\Lambda_B=\rho(A)$ (erasure: pure expansion). The condition $\rho\big(P_e\,\mathrm{diag}(|\det A_+|^m e^{-mR},\ \rho(A)^m)\big)<1$ for scalar $A=\lambda$, $m=2$ becomes $\rho\big(P_e\,\mathrm{diag}(\lambda^2 e^{-2R},\lambda^2)\big)=\lambda^2\,\rho\big(P_e\,\mathrm{diag}(e^{-2R},1)\big)<1$; at large $R$, $\to\lambda^2\,\rho\big(P_e\,\mathrm{diag}(0,1)\big)=\lambda^2\pi_B<1$ ($\pi_B$ = stationary Bad probability), matching the structure of **You–Xie (2011) Theorem 1**. ✓

**To prove it:** combine You–Xie's Markov-jump second-moment Lyapunov analysis with Lemma C's volume counting, replacing the scalar gain by the per-channel-state factor; the obstacle is bounding the **product of non-commuting** state-dependent Jacobians over Markov-correlated burst windows (a matrix-multiplicative-ergodic / Oseledets argument under the Markov channel). **Closest technique:** Fang–Loparo Markov-jump linear systems + Furstenberg–Kesten products.

### 2.5.3 Why this matters (networking framing)
Datacenter **incast** produces correlated burst loss (synchronized senders overflow a shared buffer), strongly non-i.i.d. The Gilbert–Elliott model is the minimal realistic surrogate. **Quantitative gap:** for a burst-prone link with mean erasure $\bar p$ but bursts of mean length $L\gg1$, the i.i.d. prediction $p_c=e^{-m r^\star_{\mathrm{top}}}$ is **optimistic** (the Markov $\rho(\cdot)<1$ threshold is stricter by roughly the factor $L$ in effective burst exposure); the i.i.d. theorem is a *necessary but not sufficient* screen for bursty links.

---

## 2.6 — Primary Surrogate: Complete Specification

### 2.6.1 Expanding circle map (primary)
$f:[0,1)\to[0,1)$, $f(x)=kx\bmod1$, integer $k\ge2$.
- $Df=k$ everywhere ⇒ $\sigma_1=k$ ⇒ $r^\star_{\mathrm{top}}=r^\star_{\mathrm{vol}}=\ln k$.
- **$h_R=\ln k$**: the map is uniformly expanding (1-D ⇒ conformal), so by Matveev–Pogromsky (2019) Part II the uniform-quasi-conformality condition holds and $h_R=r^\star_{\mathrm{vol}}=\ln k$; also $=h_{\mathrm{top}}=\ln k$ (standard for the $k$-fold cover).
- **Validity proof (surrogate):** *Claim:* the circle map exactly realizes D2★'s hypotheses with $r^\star_{\mathrm{top}}=r^\star_{\mathrm{vol}}=h_R=\ln k$. *Proof:* $Df\equiv k$ is constant, so $\sup_K$ and $\inf_g$ are trivial and all three rates equal $\ln k$; uniform hyperbolicity gives $h_R=r^\star_{\mathrm{vol}}$ by MP-2019 Thm (Part II, restoration-entropy formula for uniformly expanding maps); $Q=[0,1)$ is invariant. Hence necessity and sufficiency share the **same** threshold $p_c(m)=e^{-m\ln k}=k^{-m}$. $\square$ (2-paragraph proof per Directive 4.)
- **Predictions:** $p_c(m)=k^{-m}$. $k=2$: $p_c(1)=\tfrac12,\ p_c(2)=\tfrac14,\ p_c(4)=\tfrac1{16}$. $k=3$: $p_c(2)=\tfrac19$.

### 2.6.2 Hyperbolic toral automorphism (cat map)
$f:\mathbb T^2\to\mathbb T^2$, $f(\mathbf x)=A\mathbf x\bmod1$, $A=\left(\begin{smallmatrix}1&1\\1&2\end{smallmatrix}\right)$ (symmetric ⇒ singular values $=|$eigenvalues$|$).
- Eigenvalues $\lambda=\tfrac{3\pm\sqrt5}{2}$; $\lambda_u=\tfrac{3+\sqrt5}{2}\approx2.618$, $\lambda_s=1/\lambda_u\approx0.382$.
- $r^\star_{\mathrm{top}}=\ln\lambda_u\approx0.962$; $r^\star_{\mathrm{vol}}=\log^+\lambda_u+\log^+\lambda_s=\ln\lambda_u+0=\ln\lambda_u$ (only one expanding direction) ⇒ **$r^\star_{\mathrm{top}}=r^\star_{\mathrm{vol}}=\ln\lambda_u$**.
- $h_R=\ln\lambda_u$ (Anosov, constant Jacobian ⇒ uniform; $h_R=h_{\mathrm{top}}=\ln\lambda_u$).
- **Predictions:** $p_c(m)=\lambda_u^{-m}$. $p_c(1)\approx0.382,\ p_c(2)\approx0.146,\ p_c(4)\approx0.0213$.

### 2.6.3 Why these two suffice
- Both have **analytic** $r^\star$ (zero estimation error in the threshold).
- Both are **uniformly hyperbolic** ⇒ $h_R=r^\star$ exactly ⇒ necessity & sufficiency share one threshold (cleanest test).
- They give **two distinct $r^\star$** ($\ln2\approx0.693$ vs $\ln\lambda_u\approx0.962$), enabling the $p_c(m)=e^{-m r^\star}$ law to be tested across $r^\star$ values.
- The cat map is **2-D**, exercising the vector extension (§2.3.7) with $\rho(A)=\lambda_u$.

**Note [D2-C5].** For both primary surrogates $r^\star_{\mathrm{vol}}=r^\star_{\mathrm{top}}=r^\star$, so there is a single threshold: $p_c(m)=e^{-m r^\star}$ determines both the rate-sufficiency and the reliability-necessity simultaneously — the cleanest possible empirical test.

### 2.6.4 Stress tests (Lorenz / Mackey–Glass) — secondary only
- **Lorenz:** non-uniformly hyperbolic ⇒ $h_R>h_{\mathrm{top}}$, $h_R$ has no closed form ⇒ a measured deviation conflates channel limit with $h_R$-estimation error. **Robustness check only.**
- **Mackey–Glass DDE:** infinite-dimensional ⇒ restoration-entropy estimates loose. **Robustness check only.**
- *Rule:* validate on §2.6.1–2.6.2 first; on stress tests, deviations may be estimation artifacts, not theorem failures.

---

## 2.7 — Numerical Validation Protocol

### 2.7.1 D2-E1 — Phase transition (circle map, $m=2$)
System $f(x)=2x\bmod1$, $Q=[0,1)$. $R=\ln2+0.1$ (so (R) always holds). Sweep $p\in[0.05,0.40]$ step $0.01$; $T=10{,}000$ steps; $N_{\mathrm{trials}}=500$/point. Measure empirical escape rate and $\mathbb E[e_t^2]$ over the last $1000$ steps. **Prediction:** transition at $p_c=1/4$; escape$\to0$ for $p<1/4$, $\to1$ and $\mathbb E[e^2]\to\infty$ for $p>1/4$. **Falsification:** stable bounded $\mathbb E[e^2]$ at $p>p_c+\delta_{\mathrm{CI}}$.

### 2.7.2 D2-E2 — $m$-scaling (circle map $k=2$, $m\in\{1,2,4\}$)
**Parameter-free predictions:** $p_c(1)=\tfrac12,\ p_c(2)=\tfrac14,\ p_c(4)=\tfrac1{16}$. All three transitions must occur at these exact values. Any one failing potentially falsifies D2★ for that $m$.

### 2.7.3 D2-E3 — Cat-map cross-validation
$r^\star=\ln\lambda_u\approx0.962$. Predict $p_c(1)\approx0.382,\ p_c(2)\approx0.146,\ p_c(4)\approx0.0213$. **Cross-validation:** the law $p_c(m)=e^{-m r^\star}$ must hold across **both** surrogates ($r^\star=\ln2$ and $\ln\lambda_u$).

### 2.7.4 D2-E4 — Achievability (sufficiency, D2★★)
Circle map, $p<p_c$: implement successive-refinement quantizer at $R=\ln k+0.1$ + Sahai–Mitter anytime tree code (no ACK; or an ARQ/HARQ variant if causal ACK is available, per §2.4.2) over the simulated BEC. **Prediction:** bounded $\mathbb E[e^2]$ at $T=10^4$ for $p<p_c$. **Falsification of D2★★:** instability with the optimal scheme at $p<p_c$.

### 2.7.5 Statistical methodology
- Transition sharpness: logistic fit of escape rate vs $p$; finite-size scaling by varying $T$ (transition sharpens as $T\to\infty$); extract critical exponent.
- Moments: sample moments + bootstrap CI (median + 95th pct).
- FWER control across the 3 experiments (Holm–Bonferroni).
- **Power analysis:** to detect a 5% deviation of $p_c$ with 95% power at the per-$p$ escape-rate resolution, with escape-rate variance $\le1/4$ (Bernoulli) and step $0.01$, $N_{\mathrm{trials}}\gtrsim\lceil(1.96+1.645)^2\cdot0.25/(0.05\cdot p_c)^2\rceil$ — for $p_c=0.25$ this is $\approx 0.25\cdot13.0/(0.0125)^2\approx 2.1\times10^4$; **use $N_{\mathrm{trials}}=2\times10^4$ near the transition**, $500$ elsewhere.

---

## 2.8 — Hardware Validation Roadmap
- **Platform:** 2-node testbed; network emulator (Mininet, or a programmable switch with drop rules) imposing Bernoulli erasure $p$ on a UDP stream.
- **Plant node:** real-time software circle/cat map.
- **Channel:** emulator at drop rate $p$ (and Gilbert–Elliott for §2.5).
- **Controller node:** receives quantized state, returns control.
- **Measurement:** escape rate, $\mathbb E[e_t^m]$ as in §2.7.
- **Available hardware mapping:** 48 CPU threads run OMNeT++/INET for the Markov-erasure (§2.5) sweeps; 4× Tesla K80 run the Lyapunov-spectrum/SVD computation for stress-test surrogates (§2.6.4) where $r^\star$ must be estimated numerically; 256 GB RAM holds long trajectories. **D2-E1…E4 need only a single workstation (Python+numpy).**

---

## 2.9 — Journal Submission Strategy
- **Primary: IEEE Trans. Automatic Control.** Lineage of Nair–Evans (2004). **AE subfield:** networked/quantized control. **AE will ask:** "Does D2★★ hold without [H-QC]?" **Answer:** conditional on [H-QC]; general case open per §2.4.3's state-dependent-codebook barrier.
- **Secondary: SIGCOMM / NSDI.** Framing: "First fundamental communication law for distributed expansive computation: the network must guarantee **both** $R(1-p)\ge h_R$ (throughput) **and** $p\,e^{m r^\star_{\mathrm{top}}}<1$ (reliability). TCP/IP guarantees neither tightly — it optimizes mean throughput only. This proves classical transport is inadequate for expansive distributed workloads and specifies a reliability-first transport." $h_R,r^\star$ are computable from any distributed computational map — no model-specific vocabulary in the theorem.

---

## 2.10 — Conjecture U (bridge to Direction 1; unproven)
> **Conjecture U.** If hypothesis-testing agents (Direction 1) use internal estimators governed by the nonlinear map $f$ of this file, the binding channel rate is $\max\{h_R(f|_Q),\,C_{\mathrm{DIB}}(\theta)\}$: restoration entropy lower-bounds the rate needed in D1★ when belief-update maps are expansive.
**Conditions:** [C-U1] $\theta_{\mathrm{IB}}$ monotone (holds); [C-U2] estimators evolve by $f$; [C-U3] one channel serves estimation + message exchange. **Barrier:** a **joint information–control Lyapunov function** merging KL/IB (statistical) and Lyapunov/SVD (dynamical) machinery — non-standard; research frontier. (Stated identically in File 1's appendix.)

---

## 2.11 — Limitations, Threats to Validity, Failure Conditions
- **Non-compact $K$:** $r^\star$ may be $\infty$ ⇒ theorem vacuous; restrict to a compact operating region.
- **Non-expansive $f$ ($r^\star_{\mathrm{top}}=0$):** (A) holds for all $p<1$; the theorem is non-trivial only for $r^\star_{\mathrm{top}}>0$.
- **Channel memory (Markov):** (A) is replaced by the §2.5 spectral-radius condition; the i.i.d. bound is optimistic for bursty incast.
- **Delay (controller sees state from $\tau$ steps ago):** delay compounds expansion by $e^{\tau r^\star_{\mathrm{top}}}$; for linear systems Elia/NCS-delay results give the modified threshold $p\,e^{m r^\star_{\mathrm{top}}}\,e^{m\tau r^\star_{\mathrm{top}}/(\cdot)}<1$-type corrections; the nonlinear delay case is **open**.
- **Unknown model ($f$ unknown):** $r^\star$ not pre-computable; an online estimator of $r^\star$ via finite-time Lyapunov/SVD along observed trajectories is possible (DynamicalSystems.jl Lyapunov-spectrum estimators) but introduces estimation error into the threshold — quantify before trusting near $p_c$.

---

## Appendix — verified references (load-bearing)
Sahai–Mitter (arXiv cs/0601007) — anytime capacity, verified live. Matveev–Pogromsky (Automatica 2016/2019) — restoration entropy. Nair–Evans(–Mareels–Moran) (2004) — TFE / volume counting. You–Xie (Automatica 2011) — Markov-erasure linear. Elia (2005), Sinopoli et al. (2004), Gupta et al. (2007) — erasure moment thresholds. Tatikonda–Mitter (2004) — data-rate theorem.
