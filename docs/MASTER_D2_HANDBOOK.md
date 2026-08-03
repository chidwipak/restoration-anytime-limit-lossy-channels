# MASTER HANDBOOK — DIRECTION 2
## Restoration–Anytime Limit over Lossy Channels

> **Purpose of this document.** An *internal master handbook*, written by the first author, to teach a future
> reader who remembers *nothing* beyond undergraduate mathematics everything needed to **understand, derive,
> defend, and answer reviewer questions** about Direction 2 (D2). It explains intuition *before* mathematics,
> every time, and it is deliberately long and repetitive.
>
> **Source of truth.** Grounded in the repository: `D2_Research_Bible_v3.md` (theory), `code/theory.py`,
> `code/d2_sim.py` (implementation), `resultsD2.md` (experiment logs), `VALIDATION_AUDIT.md` (validation), and
> `results/d2/figures/`. Where a claim cannot be verified from those files, the text says so.
>
> **Convention.** All logarithms are natural ($\ln$); information/rates are in **nats**. The per-step
> *expansion factor* is written $\Lambda = e^{r^\star}$ (a pure ratio). This matches the bible and the code.
>
> **Independence from D1.** D2 shares *no theorems* with D1. Do not import D1 intuition. The only shared spirit
> is "a system needs a communication rate exceeding its intrinsic expansion" — but the objects
> ($\Gamma_k, \theta_{\mathrm{IB}}$ vs $r^\star, h_R, p$) are entirely different.

---

# SECTION 1 — THE BIG PICTURE (plain English, almost no mathematics)

## 1.1 A story to fix the setting

Imagine you are remotely balancing a broomstick on your fingertip — except you are doing it over the internet.
A camera watches the stick and sends you its angle; you send back a nudge to keep it upright. A balancing
broomstick is an **unstable** system: any tiny error *grows* on its own. If the stick leans a hair to the left,
next instant it leans more, and more, until it falls — *unless* you keep correcting it.

Now put two obstacles in the way, which are the entire subject of Direction 2:

1. **The link is thin.** The camera can only send you a few numbers per second — a limited *bit rate* $R$. You
   cannot see the exact angle; you see a coarse, quantized version.
2. **The link drops packets.** Sometimes a message is simply lost (**erased**), at random, with probability $p$
   each time. During a run of lost packets (a **burst**), you are flying blind — no information at all — while
   the stick keeps falling faster and faster on its own.

The scientific question of D2 is: **exactly how much bit rate $R$, and how reliable a link (how small an
erasure probability $p$), do you need to keep an unstable, possibly chaotic system under control?** And the
answer must be a *hard limit*: below it, no controller on earth can keep the system from blowing up; above it, a
specific controller succeeds.

## 1.2 Why this is subtle: two different resources, two different failures

There are two *distinct* ways the link can be inadequate, and they fail in two *distinct* ways. This split is
the heart of D2.

- **Not enough average bandwidth (a "rate" failure).** Even with perfect reliability, if the average number of
  bits you receive per second is less than the rate at which the system *manufactures new uncertainty*, you
  fall permanently behind. The system generates information (unpredictability) at a rate called its
  **restoration entropy** $h_R$; you must receive bits at least that fast *on average*. Because a fraction $p$
  of slots are erased, your *effective* average rate is $R(1-p)$. The rate condition is $R(1-p) \ge h_R$.
- **Not enough burst reliability (a "reliability" failure).** Even with enormous average bandwidth, a *long
  enough run of dropped packets* lets the unstable system expand without correction for so long that the error
  grows beyond recovery. The longer the system's worst-case expansion rate $r^\star$, and the higher the moment
  of error you care about (variance vs mean), the more you must fear bursts. The reliability condition is
  $p\, e^{m r^\star} < 1$.

These two conditions are **independent** — you can satisfy one and violate the other, and each failure is real.
That is a central, non-obvious contribution: *classical transport (like TCP/IP) optimizes average throughput
only, and provides no burst-reliability guarantee — so it is inadequate for controlling unstable/expansive
systems, no matter how fast it is on average.*

## 1.3 The one-paragraph punchline

Let the system's worst-case per-step expansion rate be $r^\star$ (how fast errors grow), its
uncertainty-generation rate be $h_R$ (its restoration entropy), the link rate be $R$, the erasure probability be
$p$, and let $m$ be the moment of the error you want to keep bounded (e.g. $m=2$ for variance/"mean-square"). D2
proves that keeping the $m$-th moment of the error bounded forever is possible **if and only if** a single
number is below 1:
$$ \gamma \;=\; (1-p)\, e^{\,m(h_R - R)/d^+} \;+\; p\, e^{\,m r^\star} \;<\; 1. $$
The two terms are exactly the two resources: the first ($1-p$ times a contraction factor) is what *delivered*
slots buy you; the second ($p$ times an expansion factor) is what *erased* slots cost you. Stability is a tug of
war between contraction on good slots and expansion on bad slots, and $\gamma$ is the net per-step multiplier of
the $m$-th moment. Two clean special cases fall out: the **rate** marginal $R(1-p)\ge h_R$ and the
**reliability** marginal $p_c(m) = e^{-m r^\star}$ (the critical erasure probability above which the $m$-th
moment blows up).

## 1.4 Why is this important / where does it appear

- **Networked control systems (NCS).** Drones, robots, power grids, autonomous vehicles controlled over
  wireless or shared networks. Any unstable plant controlled over a lossy digital link is exactly this problem.
- **Distributed computation with feedback.** Any iterative process whose internal state *expands* errors (a
  chaotic simulation, an unstable optimization, a recurrent computation) that is being tracked/steered over a
  network.
- **Datacenter reliability.** The bible's framing: bursty **incast** loss (synchronized senders overflowing a
  shared buffer) is exactly the correlated-burst regime where the reliability condition, not the average rate,
  is what bites — and where standard transport silently fails.

The practical payoff is again a **design law**: it tells you the *minimum* bit rate *and* the *maximum*
tolerable loss/burstiness to keep a given unstable system safe, and it proves that provisioning average
throughput alone (the classical goal) is not enough.

## 1.5 What motivated the research / what exactly is the gap

Four neighboring results existed (details in Section 5), each solving a *piece*:
1. **Tatikonda–Mitter (2004) / Nair–Evans (2004):** the minimum bit rate to control an unstable system over a
   *perfect* (no-loss) channel. Nair–Evans even did *nonlinear* systems (topological feedback entropy). But: no
   packet loss.
2. **Sinopoli (2004) / Elia (2005):** control/estimation of *linear* systems over a *lossy* channel — the
   famous scalar threshold $p\,\lambda^2 < 1$ for mean-square stability. But: linear only.
3. **Sahai–Mitter (2006):** the "anytime capacity" needed to stabilize an unstable *linear* plant over a noisy
   link — a *reliability* (not just rate) requirement. But: linear.
4. **Matveev–Pogromsky (2019):** *restoration entropy* $h_R$ — the exact minimum rate to observe a *nonlinear*
   system over a *perfect* finite-rate channel, robustly. But: no packet loss.

**The gap** is the intersection: a **nonlinear** system, over a **lossy (erasure)** channel, with an **$m$-th
moment** stability guarantee, using **restoration entropy** as the rate object. No prior work fused nonlinearity
+ stochastic loss + moment stability + restoration entropy. D2 does, proving the exact threshold $\gamma < 1$
(Theorems D2★ necessity and D2★★ achievability).

## 1.6 What we are trying to prove (two halves, as always)

- **Necessity (D2★): "below the threshold, everything fails."** If $\gamma \ge 1$ (equivalently, if either the
  rate condition (R) or the reliability condition (A) is violated), then *no* causal coder/controller can keep
  the $m$-th moment bounded — it diverges to infinity, and the system escapes any fixed safe region with
  probability approaching 1. This is proved for *every* scheme.
- **Achievability (D2★★): "above the threshold, a specific controller succeeds."** There is an explicit scheme —
  the **Universal Zooming Quantizer (UZQ)** paired with an anytime code — that keeps the $m$-th moment bounded
  whenever $\gamma < 1$. This is a construction.

They meet at the exact surface $\gamma = 1$ with **zero gap** for general $C^1$ expansive maps over i.i.d.
erasure channels. That is the closed-loop result.

## 1.7 An honesty note carried throughout

The clean, closed result is for **i.i.d. (independent) erasures** and **uniformly expansive $C^1$ maps** where
the restoration entropy equals the expansion rate ($h_R = r^\star$). Two extensions are explicitly *not* fully
closed and are flagged as such: (i) **correlated (bursty) erasures** — the Gilbert–Elliott channel — where a
*spectral-radius* generalization is conjectured and numerically confirmed but not proven from first principles;
and (ii) **non-uniformly hyperbolic maps** (like Hénon/Lorenz) where $h_R > $ the average expansion and has no
closed form, so those are used only as *stress tests*. Keeping "i.i.d. + uniform" (closed) separate from
"bursty / non-uniform" (open) is the key discipline for defending D2.

---

# SECTION 2 — REQUIRED BACKGROUND (taught from near zero)

Intuition first, then minimal math, then a tiny example, then where it is used in D2.

## 2.1 Dynamical systems and maps (how a state evolves)

**Intuition.** A *dynamical system* is a rule that says how a "state" changes from one instant to the next. If
the state at step $t$ is $x_t$, the rule is $x_{t+1} = f(x_t)$ — apply the function $f$ to get the next state.
Iterating $f$ traces the system's trajectory. A *controlled* system also has an input: $x_{t+1} = f(x_t, u_t)$,
where $u_t$ is your control nudge.

**Minimal math.** $f: K \to K$ maps a state space $K$ (here, a compact region of $\mathbb R^n$, or a torus) to
itself. The $b$-fold composition $f^b = f\circ f \circ \cdots \circ f$ ($b$ times) gives the state $b$ steps
later.

**Numerical example.** The *doubling map* $f(x) = 2x \bmod 1$ on $[0,1)$: start at $x_0 = 0.1$, get $0.2, 0.4,
0.8, 0.6, 0.2, \dots$. Small differences double each step — a hallmark of instability.

**Where used in D2.** The "plant" being controlled is such a map. The two primary test systems (surrogates) are
the *expanding circle map* $f(x)=kx\bmod 1$ and the *Arnold cat map* (a 2-D version).

## 2.2 Stability, instability, and expansion

**Intuition.** A system is *stable* if small errors shrink (a marble in a bowl returns to the bottom); *unstable*
if small errors grow (a marble on a hilltop rolls away). D2 is about *unstable / expansive* systems — the
interesting, hard case where you *must* keep correcting or it blows up.

**Minimal math.** Near a point, $f$ acts like its derivative. In 1-D, if $|f'(x)| > 1$ everywhere, errors grow
by a factor $|f'|$ each step — *expansion*. In $n$-D, the derivative is the **Jacobian matrix** $Df(x)$ (the
matrix of partial derivatives), and expansion is measured by its **singular values** (below).

**Numerical example.** For $f(x)=2x\bmod 1$, $f'(x)=2$ everywhere: an error $\delta$ becomes $2\delta$ next step,
$2^b\delta$ after $b$ steps. It *expands* at rate $\ln 2$ per step.

**Where used in D2.** The whole point is that during erased slots the error expands unchecked; the expansion
rate is the enemy the controller races against.

## 2.3 Jacobians, singular values, and the two expansion rates

**Intuition.** In more than one dimension, a system can stretch space in some directions and squeeze it in
others. The **singular values** $\sigma_1 \ge \sigma_2 \ge \cdots \ge \sigma_n$ of the Jacobian $Df(x)$ are the
stretch factors along the principal directions. $\sigma_1$ is the *most* it stretches (top direction); the
*product* $\prod_i \sigma_i = |\det Df|$ is how much it inflates *volume*.

**The two rates that matter (this is a D2-specific subtlety).**
- **Top rate** $r^\star_{\mathrm{top}} = \sup_x \log^+ \sigma_1(Df(x))$ — the worst-case stretch of the
  *most-expanding direction* (here $\log^+ = \max(0,\log)$). This governs *reliability*: how fast the error's
  *length* grows during a burst.
- **Volume rate** $r^\star_{\mathrm{vol}} = \sup_x \sum_i \log^+ \sigma_i(Df(x))$ — the worst-case stretch of
  *volume* (sum over all expanding directions). This governs *rate*: how many bits/second of new uncertainty
  the system makes.

For a *scalar* system or a *uniformly-expanding* one, these coincide ($r^\star_{\mathrm{top}} =
r^\star_{\mathrm{vol}} =: r^\star$). For a *vector* system with several expanding directions, they differ, and
D2 is careful to use the right one for each condition (rate $\to$ volume; reliability $\to$ top).

**Numerical example.** A diagonal linear map $\mathrm{diag}(e^{1.0}, e^{0.4})$: $r^\star_{\mathrm{top}} =
\max(1.0, 0.4) = 1.0$; $r^\star_{\mathrm{vol}} = 1.0 + 0.4 = 1.4$. (These exact numbers appear in experiment
D2-M1.)

**The "$\sup$ over states," not "average" (crucial).** These rates are *worst-case suprema over the region* $K$,
not averages along typical trajectories. Why: a *burst* of erasures can strike when the system is at its
*worst-expanding* state, and you must survive that, not the average. This is exactly why *restoration entropy*
(a sup) is the right object, not *topological/Lyapunov entropy* (an average) — a distinction we return to
repeatedly.

**Where used in D2.** $r^\star_{\mathrm{top}}$ sets the reliability threshold $p_c = e^{-m r^\star_{\mathrm{top}}}$;
$r^\star_{\mathrm{vol}}$ (via $h_R$) sets the rate threshold $R(1-p)\ge h_R$.

## 2.4 The optimal-metric refinement: spectral radius vs operator norm

**Intuition (why the "worst case" is not the naive worst case).** For a *non-normal* matrix (one whose
stretching directions are skewed, not orthogonal), a single step can stretch a vector by the large **operator
norm** $\|A\|$ (the top singular value), but *repeated* application stretches at the smaller **spectral radius**
$\rho(A)$ (the largest eigenvalue magnitude). Over a *long* burst, the average per-step growth converges to
$\rho(A)$, not $\|A\|$ (this is **Gelfand's formula**: $\|A^b\|^{1/b} \to \rho(A)$). Since the dangerous events
are *long* bursts, the reliability rate is set by $\rho(A)$, not $\|A\|$. Formally, $r^\star_{\mathrm{top}} =
\inf_g \sup_x \log^+\sigma_1(Df; g)$ — an *infimum over Riemannian metrics* $g$ — and this inf collapses the
operator norm down to the spectral radius.

**Numerical example.** The shear $A = \begin{pmatrix} 1.5 & 3 \\ 0 & 1.2\end{pmatrix}$ has eigenvalues $1.5,
1.2$ so $\rho(A)=1.5$ ($\ln\rho = 0.405$), but operator norm $\|A\| = 3.53$ ($\ln\|A\| = 1.26$) — nearly $3\times$
larger. The reliability threshold uses $\rho(A)$: $p_c(2) = \rho^{-2} = 0.444$, *not* $\|A\|^{-2} = 0.08$.
(Experiment D2-M4 confirms this precisely.)

**Where used in D2.** This is the content of "correction COR-3" and experiment D2-M4 — a subtle but genuine
point that a reviewer will probe, and that scalar/normal test systems cannot reveal.

## 2.5 Chaos, and why "restoration" (worst-case) beats "topological" (average) entropy

**Intuition.** A *chaotic* system amplifies tiny differences exponentially ("butterfly effect"). There are two
ways to quantify "how much information per step it makes":
- **Topological / Lyapunov entropy $h_{\mathrm{top}}$** — the *average* expansion along typical trajectories.
- **Restoration entropy $h_R$** — the *worst-case (uniform)* expansion over the whole region, robust to *any*
  initial error and to disturbances.

For a *uniformly* hyperbolic system (expansion is the same everywhere), these are equal. For a *non-uniform*
one (expansion varies wildly with position, like the Hénon map), $h_R > h_{\mathrm{top}}$ — the worst case
exceeds the average. D2 uses $h_R$ because a controller must give a *uniform* guarantee (survive the worst
burst at the worst state, from any error), not just handle typical behavior.

**Where used in D2.** The rate condition uses $h_R$ (not $h_{\mathrm{top}}$). Experiment D2-E6 (Hénon) shows the
*average* (Lyapunov) governs *typical* behavior while the *worst-case* governs *moment/uniform* guarantees — a
clean, honest demonstration of why restoration entropy is the correct object.

## 2.6 The erasure channel (i.i.d. and bursty)

**Intuition.** A digital link that either delivers a packet perfectly (probability $1-p$) or loses it entirely
(probability $p$). The **i.i.d.** version loses each packet independently. The **bursty** version (Gilbert–
Elliott) has "good" and "bad" periods: in a bad period, losses cluster into long runs — much more dangerous for
control, even at the same *average* loss.

**Minimal math (i.i.d.).** Each slot is delivered with prob $1-p$, erased with prob $p$, independently. The
length of a run of consecutive erasures is *geometric*: $\Pr[\text{run} = b] = (1-p)p^b$. Long bursts are rare
($\sim p^b$) but not impossible — and it is exactly the tail of long bursts that determines whether high moments
of the error stay bounded.

**Minimal math (Gilbert–Elliott).** A 2-state Markov chain (Good/Bad); in Good the erasure prob is low, in Bad
it is high; transitions $p_{GB}, p_{BG}$ control how sticky the bad state is (mean burst length $\approx
1/p_{BG}$). The stationary bad probability sets the *average* loss.

**Where used in D2.** The channel is the source of the reliability threat. i.i.d. is the closed case; Gilbert–
Elliott is the open/conjectured extension (experiments D2-E7, D2-M3).

## 2.7 Moments and "$m$-th moment stability"

**Intuition.** A random error $e_t$ can be summarized by its *moments*: the 1st moment $\mathbb E[e_t]$ (mean),
the 2nd moment $\mathbb E[e_t^2]$ (mean-square / related to variance), the 4th $\mathbb E[e_t^4]$, etc. Higher
moments weigh *large* deviations more heavily. "$m$-th moment stability" means $\limsup_t \mathbb E[e_t^m] <
\infty$ — the $m$-th moment stays bounded forever. Higher $m$ is a *stricter* requirement (it demands the *tails*
of the error stay controlled), so it needs a better channel.

**Why $m$ matters for the threshold.** The reliability threshold is $p_c(m) = e^{-m r^\star}$ — it *decreases*
as $m$ grows. Bounding the mean ($m=1$) tolerates more loss than bounding the mean-square ($m=2$), which
tolerates more than the 4th moment. Intuition: high moments are dominated by rare *large* errors, which come
from rare *long* bursts, so protecting them requires a more reliable channel.

**Numerical example (circle map $k=2$, $r^\star=\ln 2$).** $p_c(1) = 2^{-1} = 0.5$; $p_c(2) = 2^{-2} = 0.25$;
$p_c(4) = 2^{-4} = 0.0625$. (These exact values are validated in experiment D2-E1.)

**Where used in D2.** The entire threshold is stated per moment $m$; the $m$-dependence $p_c(m) = e^{-m r^\star}$
is a *discriminating fingerprint* tested across systems.

## 2.8 The observer, the zooming quantizer, and the uncertainty set

**Intuition.** The controller cannot see the exact state; it maintains an **uncertainty set** $\Omega_t$ — a
small region guaranteed to contain the true state $x_t$, with half-width $\delta_t$. Each step: (1) *predict* —
the map expands $\Omega_t$ (the true state moved, and the set inflates by the expansion factor); (2) *update* —
if a packet is delivered, the encoder tells you which sub-cell of the (expanded) set the true state is in,
*shrinking* $\delta$ by the rate factor $e^{-R}$; if erased, no shrink. A **zooming quantizer** is one whose
grid adapts ("zooms") to the current uncertainty, so it never wastes bits — the key to hitting the exact rate
$h_R$ with no slack.

**Minimal math (the uncertainty recursion — the heart of every D2 experiment).** For a uniformly-expanding map,
$$ \delta_{t+1} = G_t\,\delta_t, \qquad G_t = \begin{cases} e^{r^\star - R} & \text{delivered (prob } 1-p) \\
e^{r^\star} & \text{erased (prob } p)\end{cases}. $$
So $\delta$ does a *multiplicative random walk*: shrink by $e^{r^\star - R}$ on good slots, grow by $e^{r^\star}$
on bad slots. Whether $\delta$ (and its moments) stay bounded is *the* question, and it is answered by $\gamma$.

**Where used in D2.** This recursion *is* the simulated system in every D2 experiment; the whole theory is
statements about this random walk.

## 2.9 The moment multiplier $\gamma$ and why it is exact

**Intuition.** Take the $m$-th moment of one step of the recursion: on a good slot $\delta^m$ multiplies by
$(e^{r^\star-R})^m$; on a bad slot by $(e^{r^\star})^m$. Averaging over the coin flip,
$$ \mathbb E[\delta_{t+1}^m] = \big[\underbrace{(1-p)e^{m(r^\star-R)}}_{\text{good slots buy contraction}} +
\underbrace{p\,e^{m r^\star}}_{\text{bad slots cost expansion}}\big]\,\mathbb E[\delta_t^m] = \gamma\cdot
\mathbb E[\delta_t^m]. $$
So $\mathbb E[\delta_t^m] = \delta_0^m\,\gamma^t$ *exactly* — it grows if $\gamma > 1$, shrinks/stays bounded if
$\gamma < 1$. The threshold $\gamma = 1$ is therefore not an approximation; it is arithmetic. (The general form
replaces $r^\star - R$ by $(h_R - R)/d^+$ to account for how the rate is spread across $d^+$ expanding
directions.)

**Where used in D2.** $\gamma$ is *the* object; every experiment measures it or its threshold.

## 2.10 Anytime reliability (Sahai–Mitter)

**Intuition.** For controlling an unstable system, it is not enough that bits *eventually* arrive; they must
arrive with a *reliability that improves with delay*. **Anytime reliability** $\alpha$ means: the probability
that a bit sent $d$ steps ago is still wrong (undelivered) decays as $e^{-\alpha d}$. For an erasure channel,
the dominant way a bit is delayed by $d$ is a length-$d$ erasure burst, probability $p^d = e^{-d\ln(1/p)}$ — so
the channel's intrinsic anytime exponent is $\alpha_{\mathrm{ch}} = \ln(1/p)$. Sahai–Mitter proved that
$m$-th-moment stabilization of an unstable system needs $\alpha > m\,r^\star$ — which is *exactly* the
reliability condition $\ln(1/p) > m r^\star \iff p\,e^{m r^\star} < 1$.

**Where used in D2.** The reliability condition (A) *is* the anytime condition; the burst-tail mechanism
$p^b$ is what drives moment divergence.

## 2.11 Importance sampling (the tool that makes rare-event moments measurable)

**Intuition.** The $m$-th moment $\mathbb E[\delta^m]$ is dominated by *rare* erasure-heavy trajectories (long
bursts), which naive simulation almost never generates — so naive Monte Carlo *underestimates* the moment badly
(by orders of magnitude). **Importance sampling (IS)** fixes this: simulate under a *tilted* channel that makes
erasures more common (so the rare heavy paths become typical), then *reweight* each sample by the likelihood
ratio to correct the bias. With the *optimal* tilt, the estimator is essentially exact.

**Minimal math.** To estimate $\mathbb E_p[g]$, sample under $q \ne p$ and average $g\cdot\frac{p}{q}$ (the
likelihood ratio). For the multiplicative walk, the zero-variance tilt is $q^\star = p\,e^{m r^\star}/\gamma$.

**Where used in D2.** Every moment/threshold measurement uses IS; experiment D2-E1 shows naive MC failing and IS
succeeding side by side. This is a methodological necessity, not a nicety — the naive protocol in the bible is
infeasible for these moments.

## 2.12 Spectral radius of a modulated matrix (for bursty channels)

**Intuition.** When the channel has memory (Gilbert–Elliott), the moment growth is no longer a scalar
multiplier $\gamma$ but the growth rate of a *product of matrices* (one factor per channel state). The right
quantity is the **spectral radius** $\rho(M)$ of the transfer matrix $M = P_e^\top \mathrm{diag}(\text{good
factor}^m, \text{bad factor}^m)$, where $P_e$ is the channel's transition matrix. Stability $\iff \rho(M) < 1$.
For i.i.d. loss this reduces to $\gamma < 1$.

**Where used in D2.** The Gilbert–Elliott generalization (Conjecture D2-Markov, experiment D2-M3): the
spectral-radius threshold is confirmed numerically to be exact (MAE $0.0009$), though a first-principles proof
for nonlinear maps remains open.

---

# SECTION 3 — NOTATION BIBLE (every symbol)

Grounded in `D2_Research_Bible_v3.md` §2.0 and `code/theory.py` / `code/d2_sim.py`.

| Symbol | Meaning | Type / units | Range | First seen | Used later | Common confusion |
|---|---|---|---|---|---|---|
| $x_t$ | system state at step $t$ | point in $K$ | — | §2.1 | dynamics | the *true* state (unknown to controller) |
| $f$ | the system map (plant) | function $K\to K$ | $C^1$ | §2.1 | everywhere | closed-loop *ideal* map $f(\cdot,u^\star)$ |
| $K$ | operating region (state space) | compact set | $\subset\mathbb R^n$ or torus | §2.1 | $\sup_K$ | must be compact (else $r^\star=\infty$) |
| $Q$ | target/safe set | compact $\subseteq K$ | invariant | §4 | set-invariance | escape from $Q$ = failure |
| $u_t$ | control input | vector | — | §2.1 | achievability | your nudge |
| $Df(x)$ | Jacobian of $f$ at $x$ | matrix | — | §2.3 | $\sigma_i$ | the local linearization |
| $\sigma_i$ | singular values of $Df$ | $\ge 0$ | $\sigma_1\ge\dots$ | §2.3 | $r^\star$ | stretch factors; $\sigma_1$=top |
| $r^\star_{\mathrm{top}}$ | **top expansion rate** | nats/step | $\ge 0$ | §2.3 | condition (A) | $\sup_x\log^+\sigma_1$; reliability |
| $r^\star_{\mathrm{vol}}$ | **volume expansion rate** | nats/step | $\ge 0$ | §2.3 | condition (R) | $\sup_x\sum\log^+\sigma_i$; rate |
| $r^\star$ | the common rate (scalar/uniform case) | nats/step | $\ge 0$ | §1.3 | surrogates | $=r^\star_{\mathrm{top}}=r^\star_{\mathrm{vol}}$ only when they coincide |
| $\Lambda$ | expansion factor | ratio $\ge 1$ | $=e^{r^\star_{\mathrm{top}}}$ | §2.0 | drift | pure number |
| $h_R$ | **restoration entropy** | nats/step | $[0, r^\star_{\mathrm{vol}}]$ | §2.5 | condition (R) | $=r^\star_{\mathrm{vol}}$ for uniform maps; a *sup*, not average |
| $h_{\mathrm{top}}$ | topological/Lyapunov entropy | nats/step | $\le h_R$ | §2.5 | stress test | the *average*; the *wrong* object for moments |
| $d^+$ | number of expanding directions | integer | $\ge 1$ | §2.9 | $\gamma$ | $\#\{i:\sigma_i>1\}$; for circle/cat $=1$ |
| $R$ | channel bit rate | nats/use | $\ge 0$ | §1.1 | condition (R), $\gamma$ | delivered *only when not erased* |
| $p$ | erasure probability | probability | $(0,1)$ | §1.1 | everywhere | the loss rate |
| $m$ | moment order | $\ge 1$ | integer usually | §2.7 | $p_c(m), \gamma$ | higher $m$ = stricter |
| $e_t$ | estimation/tracking error | $\ge 0$ | — | §2.8 | moment stability | $\mathrm{dist}(\hat x_t, x_t)$ |
| $\delta_t$ | uncertainty half-width | $\ge 0$ | — | §2.8 | recursion | bounds $e_t$; the simulated quantity |
| $\gamma$ | **$m$-th-moment multiplier** | ratio | $>0$ | §1.3 | main theorem | stable iff $\gamma<1$; $=E[G^m]$ |
| $p_c(m)$ | critical erasure prob (reliability marginal) | probability | $(0,1)$ | §2.7 | condition (A) | $=e^{-m r^\star_{\mathrm{top}}}$ |
| $\alpha_{\mathrm{ch}}$ | channel anytime exponent | nats | $=\ln(1/p)$ | §2.10 | condition (A) | burst-tail exponent |
| $G_t$ | per-step error multiplier | ratio | $\in\{e^{r^\star-R}, e^{r^\star}\}$ | §2.8 | recursion | random (channel-driven) |
| $P_e$ | Gilbert–Elliott transition matrix | $2\times2$ stochastic | — | §2.6 | D2-M3 | channel memory |
| $\rho(\cdot)$ | spectral radius (largest $\vert$eigenvalue$\vert$) | ratio | $\ge 0$ | §2.4 | D2-M4, M3 | the *repeated*-application rate |
| $\Vert A\Vert$ | operator norm (top singular value) | ratio | $\ge\rho$ | §2.4 | D2-M4 | the *single-step* rate; NOT the threshold |
| $k$ | expanding-circle-map factor | integer $\ge2$ | — | §2.1 | surrogate | $r^\star=\ln k$ |
| $\lambda_u$ | cat-map unstable eigenvalue | $\approx2.618$ | $=(3+\sqrt5)/2$ | §4 | surrogate | $r^\star=\ln\lambda_u\approx0.962$ |

**Decorations.** $\hat x$: the controller's *estimate*. $\log^+ = \max(0, \log)$: keeps only *expanding*
directions. $f^b$: $b$-fold composition. $\limsup_t \mathbb E\,e_t^m$: the object that must be finite for
$m$-th-moment stability. **The three symbols never to confuse:** $r^\star_{\mathrm{top}}$ (reliability, a *max*
over directions) vs $r^\star_{\mathrm{vol}}$ (rate, a *sum* over directions) vs $h_{\mathrm{top}}$ (the *average*,
which is the *wrong* object). And $\rho(A)$ (long-run rate, correct) vs $\|A\|$ (single-step, too pessimistic).

---

# SECTION 4 — PROBLEM FORMULATION (every assumption, every equation)

## 4.1 The abstract problem

**Given:** a $C^1$ expansive map $f$ on a compact region $K$, with a compact target set $Q$ that ideal feedback
keeps invariant; a memoryless erasure channel with rate $R$ and loss $p$; a moment order $m \ge 1$. **Asked:**
the exact necessary-and-sufficient $(R, p)$ for **$m$-th-moment controlled set-invariance** — i.e. for a causal
coder/controller to guarantee $\limsup_t \mathbb E[e_t^m] < \infty$ while keeping the controlled state near $Q$.

## 4.2 The seven standing assumptions (bible §2.3.1), each explained

- **[H2-1] $f(\cdot, u^\star) \in C^1(K)$** (continuously differentiable). *Why:* so the Jacobian $Df$, hence
  the expansion rates, exist and vary continuously. *If weakened to Lipschitz:* the *necessity* proof still
  works (derivative exists almost everywhere by Rademacher); *sufficiency* needs $C^1$ to build the quantizer.
- **[H2-2] $K$ compact.** *Why:* so $\sup_x$ in the expansion rates is *finite*. *If removed:* $r^\star$ could
  be infinite and the theorem vacuous — hence "restrict to a compact operating region."
- **[H2-3] $Q \subseteq K$ compact and invariant under ideal feedback.** *Why:* it is the "safe set"; "escape
  from $Q$" is the well-defined failure event.
- **[H2-4] $f$ expansive: $r^\star_{\mathrm{top}} > 0$.** *Why:* the problem is only non-trivial if *some*
  direction expands (otherwise any $p<1$ is fine). Note this is *weaker* than "every point unstable."
- **[H2-5] memoryless erasure channel, $p\in(0,1)$**, with or without acknowledgment (ACK). *Why:* the source
  of loss. *ACK note:* ACK can help the *achievability* (enables retransmission) but *not* the necessity —
  because channel capacity is feedback-invariant for memoryless channels, and bursts are unpredictable.
- **[H2-6] causal separation of observer/controller**, fixed information structure. *Why:* rules out
  non-causal cheating (seeing the future).
- **[H2-7] $m \ge 1$.** The moment order you want bounded.

## 4.3 The theorem's two conditions and the exact surface

**Condition (R) — rate (bible §2.3.1):** $\ R(1-p) \ge h_R(f|_Q)$, where $h_R \le r^\star_{\mathrm{vol}}$.
*Meaning:* your *effective* average rate (rate $R$ times delivery fraction $1-p$) must cover the system's
uncertainty-generation rate $h_R$. *Where it comes from:* the delivered-bit count is $R\cdot(\text{fraction
delivered}) \to R(1-p)$ by the law of large numbers, and volume-counting (Nair–Evans / Matveev–Pogromsky) says
you need $\ge h_R$ nats/step to keep the uncertainty volume bounded.

**Condition (A) — reliability (bible §2.3.1):** $\ p\,e^{m r^\star_{\mathrm{top}}} < 1 \iff \alpha_{\mathrm{ch}}
= \ln(1/p) > m\,r^\star_{\mathrm{top}}$. *Meaning:* the channel's burst-reliability exponent must exceed the
$m$-scaled top expansion rate. *Where it comes from:* the $m$-th moment gets a contribution $\sim p^b\,e^{m
r^\star b}$ from length-$b$ bursts; the geometric series converges iff $p\,e^{m r^\star} < 1$.

**The exact surface (bible §2.4.1, Theorem D2★★):**
$$ \gamma = (1-p)\,e^{m(h_R - R)/d^+} + p\,e^{m r^\star_{\mathrm{top}}} < 1. $$
(R) and (A) are its *two marginal projections*: as $R \to \infty$, the first term $\to 0$ and $\gamma < 1
\iff$ (A); as $p \to 0$, $\gamma < 1 \iff R > h_R$, which is (R). The full $\gamma < 1$ is stricter than either
marginal alone.

## 4.4 The concrete surrogates (where every number is exact)

The theory is tested on systems where $h_R = r^\star$ *exactly* (uniformly hyperbolic), so the threshold has no
estimation error. From `code/theory.py`:

- **Expanding circle map** $f(x) = kx \bmod 1$ on $[0,1)$, integer $k\ge 2$. Then $Df \equiv k$, so
  $r^\star_{\mathrm{top}} = r^\star_{\mathrm{vol}} = h_R = \ln k$. Reliability thresholds: $p_c(m) = k^{-m}$. For
  $k=2$: $p_c(1)=\tfrac12,\ p_c(2)=\tfrac14,\ p_c(4)=\tfrac1{16}$.
- **Arnold cat map** $f(\mathbf x) = A\mathbf x \bmod 1$ on the torus, $A = \begin{pmatrix} 1&1\\1&2\end{pmatrix}$.
  Eigenvalues $\lambda_u = \tfrac{3+\sqrt5}{2} \approx 2.618$ and $\lambda_s = 1/\lambda_u \approx 0.382$. Only
  one expanding direction, so $r^\star_{\mathrm{top}} = r^\star_{\mathrm{vol}} = h_R = \ln\lambda_u \approx
  0.962$. Predictions $p_c(m) = \lambda_u^{-m}$: $p_c(1)\approx0.382,\ p_c(2)\approx0.146,\ p_c(4)\approx0.021$.

**Why two surrogates with different $r^\star$?** So the law $p_c(m) = e^{-m r^\star}$ can be tested *across*
$r^\star$ values (the slope of $\ln p_c$ vs $m$ must equal $-r^\star$ for each).

**Stress-test systems (non-uniform, $h_R \ne r^\star$, used only to probe limits):** the Hénon map (2-D, chaotic,
non-uniform) and higher-dimensional / non-normal vector systems.

## 4.5 The Universal Zooming Quantizer (UZQ) in one paragraph (the achievability construction)

The controller and encoder both maintain the *same* uncertainty set $\Omega_t$, computed purely from the shared
*index history* (the sequence of quantizer cells transmitted), *not* from the unknown state — so they never
disagree (no "chicken-and-egg"). Each step: predict ($\Omega$ inflates by the map), then tile the predicted set
into $e^R$ cells (in the *optimal metric* $g^\star$ that uniformizes expansion, so no bits are wasted) and
transmit the true cell's index; a delivered index shrinks $\Omega$ by $e^{-R}$, an erased one leaves it stale
but still *containing* the true state (a valid over-bound, never a wrong commitment). The index stream is
carried by a Sahai–Mitter anytime code so it re-synchronizes after bursts *without ACK*. Because $g^\star$
uniformizes expansion, the rate threshold is *exactly* $h_R$ (no $\varepsilon$ slack), and the full $m$-th-moment
threshold is the exact $\gamma = 1$ surface.

---

# SECTION 5 — LITERATURE REVIEW (the evolution of the field)

Grounded in `D2_Research_Bible_v3.md` §2.2.

## 5.1 Data-rate theorems: Tatikonda–Mitter (2004), Nair–Evans (2004)

*What they solved:* the minimum bit rate to stabilize/observe an unstable system over a *perfect* (lossless)
finite-rate channel. Tatikonda–Mitter: a *linear* system is mean-square stabilizable iff $R > \sum_i \log^+
|\lambda_i(A)| = \log|\det A_+|$ (the sum of unstable log-eigenvalues). Nair–Evans: extended to *nonlinear*
systems, with the minimal rate being the **topological feedback entropy** $h_{\mathrm{top}}$. *Assumptions:* no
channel loss. *Where they stop:* the moment a packet can be *lost*, TFE fails — because a single drop can
magnify the initial error without bound (TFE has no *uniform/robust* margin). *How D2 extends:* D2 replaces the
lossless-channel TFE by the *lossy-channel restoration entropy* and adds the reliability condition; it recovers
Tatikonda–Mitter at $p=0$ (condition (R) $\to R \ge r^\star_{\mathrm{vol}}$).

## 5.2 Erasure-channel stability, linear: Sinopoli (2004), Elia (2005), You–Xie (2011)

*What they solved:* control/estimation of *linear* systems over *lossy* channels. Sinopoli: Kalman filtering
with intermittent observations has a critical arrival probability; for scalar unstable $|\lambda|$, mean-square
bounded iff $p < 1/\lambda^2$. Elia: scalar mean-square stabilizable iff $p\,|\lambda|^2 < 1$. You–Xie: Markov
(bursty) loss, spectral-radius conditions. *Assumptions:* linear plant. *Where they stop:* nonlinear systems.
*How D2 extends/recovers:* D2's condition (A) at $m=2$ for a scalar system is exactly $p\,|\lambda|^2 < 1$ —
Elia/Sinopoli recovered as a special case (the "linear sanity check"); You–Xie's Markov condition is the linear
shadow of the Gilbert–Elliott conjecture (D2-M3).

## 5.3 Anytime capacity: Sahai–Mitter (2006)

*What they solved:* stabilizing an unstable *linear* plant over a *noisy* link requires not just enough rate but
enough *anytime reliability* — the probability a bit sent $d$ ago is still wrong must decay as $e^{-\alpha d}$
with $\alpha > m\log|\lambda|$ for $m$-th-moment stability. *Assumptions:* linear (constant gain $\lambda$).
*Where they stop:* nonlinear systems have *state-dependent* Jacobians, so a single constant $\log|\lambda|$ is
ill-defined. *How D2 extends:* replace the constant $\log|\lambda|$ by the *uniform worst-case* rates
$r^\star_{\mathrm{top}}$ (reliability) and $r^\star_{\mathrm{vol}}$ (rate). D2's condition (A) *is* the
Sahai–Mitter anytime condition with $r^\star_{\mathrm{top}}$ in place of $\log|\lambda|$.

## 5.4 Restoration entropy: Matveev–Pogromsky (2016, 2019)

*What they solved:* the minimal data rate to *observe* a nonlinear system over a *perfect* finite-rate channel,
*robustly* (uniform over initial errors, robust to disturbances) — the **restoration entropy** $h_R$, with a
tight SVD/Lyapunov estimate $h_R \le \sup_x \sum_i \log^+\sigma_i = r^\star_{\mathrm{vol}}$ (equality for
uniformly quasi-conformal $f$), and a *constructive coder* (a zooming quantizer). *Assumptions:* no packet loss.
*Where they stop:* stochastic channels / moment stability under loss. *How D2 uses them:* $h_R$ *is* the rate
object in condition (R), and the Matveev–Pogromsky zooming quantizer is the backbone of the UZQ achievability
(D2★★). *Key correction (bible COR-4):* Matveev–Pogromsky demote Lorenz/Mackey–Glass from "primary examples" to
stress tests, because those are non-uniformly hyperbolic ($h_R \ne r^\star$) and would conflate the channel
limit with an entropy-estimation gap.

## 5.5 Quevedo–Nešić (2012), Liberzon–Nair, Baillieul

*Quevedo–Nešić:* packetized predictive control of *nonlinear* systems under *Markov* loss — ISS-type
*sufficient* conditions, but not a *tight necessity* in terms of an intrinsic entropy. *Liberzon–Nair /
Baillieul:* data-rate requirements for nonlinear quantized control, but largely *deterministic* channels — no
random erasure with moment guarantees. *How D2 differs:* D2 supplies the *tight* necessity and the *restoration-
entropy* invariant that these works lack.

## 5.6 The novelty in one table (bible §2.2, paraphrased)

| Prior work | nonlinear? | stochastic loss? | moment stability? | restoration entropy? | achievability? |
|---|:--:|:--:|:--:|:--:|:--:|
| Tatikonda–Mitter '04 | ✗ | ✗ | MS | — | ✓ |
| Nair–Evans '04 | ✓ | ✗ | set-inv | TFE (not $h_R$) | ✓ |
| Sinopoli '04 / Elia '05 | ✗ | ✓ | MS | — | ✓ |
| Sahai–Mitter '06 | ✗ | ✓ | $m$-th | — | ✓ |
| Matveev–Pogromsky '19 | ✓ | ✗ | set-inv | **restoration** | ✓ |
| **D2 (this work)** | **✓** | **✓** | **$m$-th** | **restoration** | **✓** |

The bottom row — all five features at once — is the contribution.

---

# SECTION 6 — OUR CONTRIBUTIONS (simple English and mathematics)

## 6.1 Contribution 1 — the exact two-condition / $\gamma<1$ threshold

*Simple English:* we found the exact minimum channel (rate *and* reliability) to keep an unstable nonlinear
system bounded, and it splits into two independent requirements: enough *average* rate ($R(1-p)\ge h_R$) *and*
enough *burst reliability* ($p\,e^{m r^\star} < 1$). *Mathematics:* the necessity (D2★) and achievability (D2★★)
meet at $\gamma = (1-p)e^{m(h_R-R)/d^+} + p\,e^{m r^\star_{\mathrm{top}}} = 1$, zero gap, for general $C^1$
expansive maps over i.i.d. erasure. *Why new:* first fusion of nonlinearity + stochastic loss + moment
stability + restoration entropy. *Main insight:* stability is a per-step tug-of-war captured by a single number
$\gamma$; the two classical conditions are its marginals.

## 6.2 Contribution 2 — two conditions are genuinely independent (rate ≠ reliability)

*Simple English:* running out of *average bandwidth* and running out of *burst reliability* are *different*
failures; you can have plenty of one and fail the other. *Evidence:* experiment D2-E2 shows, at a *fixed* rate,
the a.s. (drift) transition at $p_R = 0.126$ and a *cascade* of moment thresholds $p_A(m)$ *below* it
($0.087, 0.057, 0.0215$ for $m=1,2,4$) — distinct transitions from distinct mechanisms. *Why it matters:* it
proves classical throughput-only transport (TCP/IP) is *structurally* inadequate for expansive control loads.

## 6.3 Contribution 3 — restoration entropy (worst-case), not topological/Lyapunov (average), is the right rate

*Simple English:* you must survive the *worst* burst at the *worst* state from *any* error, so the governing
rate is a *worst-case supremum* (restoration entropy $h_R$), not an *average* (Lyapunov/topological entropy).
*Evidence:* experiment D2-E6 (Hénon, non-uniform) — the a.s./typical behavior follows the Lyapunov *average*
($0.517$ observed vs $0.552$ predicted) while the effective rate for higher moments rises toward the *worst-case*
($r_{\mathrm{eff}}(m)$ climbs from $0.725$ to $1.320$). *Why subtle:* on *uniform* systems the two coincide (why
circle/cat are the clean primary tests); only *non-uniform* systems separate them.

## 6.4 Contribution 4 — the two-rate structure for vector systems ($r^\star_{\mathrm{vol}} \ne r^\star_{\mathrm{top}}$)

*Simple English:* for a system that expands in several directions, the *rate* you need is set by the *total*
(volume) expansion, but the *reliability* you need is set by the *fastest single* (top) direction — two
different numbers for two different jobs. *Evidence:* experiment D2-M1 on a vector system with $r^\star_{\mathrm{
vol}} = 1.4 \ne r^\star_{\mathrm{top}} = 1.0$: the a.s./rate transition binds on $r^\star_{\mathrm{vol}}$ ($0.329$
observed vs $0.364$ predicted) while the moment/reliability threshold binds on $r^\star_{\mathrm{top}}$ ($p_c(2)
= 0.1352$ vs $e^{-2r^\star_{\mathrm{top}}} = 0.1353$). *Why new:* scalar surrogates cannot show this; it is the
first genuine confirmation of the two-rate (COR-3) structure.

## 6.5 Contribution 5 — the optimal-metric (spectral-radius) reliability rate

*Simple English:* for a skewed (non-normal) system, the reliability rate is the *long-run* growth (spectral
radius $\rho(A)$), not the *single-step* stretch (operator norm $\|A\|$) — because the dangerous long bursts
self-average to $\rho(A)$. *Evidence:* experiment D2-M4 on non-normal matrices — the moment threshold matches
$\rho(A)^{-m}$ to MAE $0.0087$, while the naive $\|A\|^{-m}$ is off by $35\times$ that error. *Why it matters:*
it confirms the bible's $\inf_g$ (optimal-metric) definition is the operationally correct one, on systems that
scalar/normal surrogates cannot probe.

## 6.6 Contribution 6 — the correlated-burst (Gilbert–Elliott) generalization

*Simple English:* real networks lose packets in *bursts*, which are far more damaging than i.i.d. loss at the
*same average rate*; the right threshold becomes a *spectral radius* of a modulated matrix. *Evidence:*
experiment D2-M3 — at $10\%$ mean loss (safe for i.i.d.), a mean-burst-length-50 channel escapes with
probability $1.0$; and the transfer-matrix growth rate matches $\ln\rho(M)$ to MAE $0.0009$. *Status:* the
i.i.d. threshold is thus a *necessary-but-optimistic* screen for real links; the spectral form is numerically
exact but a first-principles proof for nonlinear maps is *open* (honestly documented).

## 6.7 Contribution 7 — a rigorous rare-event validation methodology

*Simple English:* the moments that decide stability are dominated by *rare* long bursts that naive simulation
never sees, so we use *importance sampling* (with the analytically-optimal tilt) to measure them, and the
closed-form $\gamma$ as ground truth. *Why it matters:* it makes the empirical support believable; the naive
Monte-Carlo protocol in the bible would *underestimate* the moment by orders of magnitude (shown explicitly in
D2-E1).

---

# SECTION 7 — THEOREMS (statement, plain English, meaning, assumptions, consequences, intuition, reviewer bait)

## 7.1 Theorem D2★ — the Restoration–Anytime Necessity

**Formal statement (bible §2.3.1).** Under [H2-1]–[H2-7], $m$-th-moment controlled set-invariance *requires
both*:
$$ \textbf{(R)}\quad R(1-p) \ge h_R(f|_Q), \qquad \textbf{(A)}\quad p\,e^{m r^\star_{\mathrm{top}}} < 1. $$
If (A) fails, then for *every* causal coder/quantizer/controller, $\limsup_t \mathbb E[e_t^m] = \infty$ and the
probability of escaping any fixed neighborhood of $Q$ $\to 1$. *Almost-sure corollary:* (R) alone is necessary
for almost-sure boundedness; (A) is the extra *moment* refinement.

**Plain English.** To keep the $m$-th moment of the error bounded you *must* have both enough average rate (R)
and enough burst reliability (A). Violate either, and no controller — however clever, with or without
acknowledgments — can prevent the moment from blowing up and the system from escaping.

**Why it matters.** It is the *hard impossibility*: it tells you the minimum channel below which control is
*impossible*, and it proves the two requirements are *separate* (you must satisfy both).

**Assumptions' roles.** [H2-2] compactness $\to$ finite $r^\star$; [H2-4] expansiveness $\to$ non-trivial;
[H2-5] memoryless $\to$ bursts are geometric and ACK-invariant; [H2-7] $m$ $\to$ which moment.

**Consequences.** (i) Two independent conditions (Contribution 2). (ii) Recovers the classics: $p=0$ gives
Tatikonda–Mitter ($R \ge r^\star_{\mathrm{vol}}$); scalar $m=2$ gives Elia/Sinopoli ($p\lambda^2 < 1$); the
anytime form $\ln(1/p) > m r^\star$ is Sahai–Mitter. (iii) Scalar/uniform collapse:
$r^\star_{\mathrm{top}}=r^\star_{\mathrm{vol}}=r^\star$.

**Limitations.** i.i.d. erasure (bursty is the open Gilbert–Elliott extension); $h_R = r^\star$ needs uniform
hyperbolicity (non-uniform maps have $h_R$ without closed form).

**Intuition.** Two independent ways to lose. (R): if your *average* delivered rate $R(1-p)$ is below the rate
$h_R$ at which the system *makes* uncertainty, you fall behind forever (law of large numbers + volume counting).
(A): even with huge average rate, a *long enough* burst (probability $p^b$) lets the error grow by $e^{m
r^\star b}$; the $m$-th moment sums $p^b e^{m r^\star b}$, which diverges once $p\,e^{m r^\star} \ge 1$ — no
between-burst correction can fix a *divergent* series.

**Reviewer bait (answered in Section 12).** *"Doesn't ACK save you?"* No — bursts are unpredictable
(memoryless) and capacity is feedback-invariant. *"Isn't this just Sahai–Mitter?"* No — theirs is linear
(constant $\lambda$); we handle *state-dependent* Jacobians via the *uniform* $r^\star$, and add the restoration-
entropy rate condition.

## 7.2 Theorem D2★★ — the UZQ Achievability (exact threshold)

**Formal statement (bible §2.4.1).** For every $C^1$ expansive $f$ on compact $K$, the Universal Zooming
Quantizer + anytime code achieves $m$-th-moment controlled set-invariance *if and only if*
$$ \gamma = (1-p)\,e^{m(h_R - R)/d^+} + p\,e^{m r^\star_{\mathrm{top}}} < 1. $$
Necessity and achievability meet at $\gamma = 1$ with **zero gap**, *without* a quasi-conformality assumption.
As $p \to 0$, $\gamma < 1 \iff R > h_R$ — the rate threshold is *exactly* $h_R$, no $\varepsilon$ slack.

**Plain English.** There is an actual controller — the zooming quantizer that adapts its grid to the current
uncertainty and rides an anytime code through bursts without acknowledgments — that keeps the $m$-th moment
bounded *exactly* when $\gamma < 1$. So the necessity threshold is *reached*: the problem is solved exactly.

**Why it matters.** Converse + achievability = exact answer, not just a bound; and it gives the *recipe*.

**The three ingredients (each a lemma / verification in Section 8):**
- *Lemma A-D2 (the UZQ):* encoder and decoder maintain the *same* uncertainty set from the *shared index
  history* (not the unknown state), so they never desynchronize; the grid "zooms" to the local expansion in the
  optimal metric $g^\star$, wasting zero bits.
- *Lemma B-D2 (the drift):* the per-step $m$-th-moment multiplier is exactly $\gamma$; a geometric-drift
  (Meyn–Tweedie) argument gives bounded moment iff $\gamma < 1$.
- *Lemma C-D2 (cat-map verification):* the construction works even for the non-quasi-conformal cat map
  ($\sigma_1 \ne \sigma_2$), by zooming *only* along the unstable direction.

**Limitations / scope.** i.i.d. erasure; the explicit no-ACK *anytime tree code* is modeled by "the index
stream is eventually delivered" (its reliability exponent $\ln(1/p)$ is exactly the burst tail, which *is*
validated). Bursty channels are the open extension.

**Intuition.** The zooming quantizer spends bits *exactly* where the system creates uncertainty (the optimal
metric uniformizes expansion), so it hits the rate floor $h_R$ with no waste; the anytime code guarantees the
index stream survives bursts with the right reliability; and the drift of the error's $m$-th moment is exactly
$\gamma$, so it is bounded iff $\gamma < 1$.

## 7.3 The independence proposition (bible §2.3.5)

**Statement.** (R) and (A) are independent: there exist $(R,p)$ satisfying (R) but not (A) (unstable), and vice
versa. *Example (R holds, A fails):* scalar $\lambda=2$, $m=2$, $r^\star=\ln 2$; take $R=100$ (so $R(1-p)\ge
\ln2$ trivially) and $p=0.3 > 0.25 = p_c$ — (A) fails, moment diverges. *Example (A holds, R fails):* same
system, $p=10^{-3}$ (so $p\lambda^2 = 0.004 < 1$, (A) holds) but $R=0.1 < \ln 2$ — (R) fails, error grows a.s.
**Meaning:** neither condition implies the other; both are genuinely needed. This is the structural advance over
prior work, which had only *one* condition (rate-only in data-rate theorems; reliability-only in Sahai–Mitter).

## 7.4 The linear sanity check (bible §2.3.6)

**Statement.** For a scalar linear system $f(x)=\lambda x$: (R) at $p=0$ gives $R \ge \ln|\lambda|$ =
Tatikonda–Mitter/Nair–Evans; (A) at $m=2$ gives $p < 1/\lambda^2$ = Elia/Sinopoli; the anytime form $\ln(1/p) >
m\ln|\lambda|$ = Sahai–Mitter. **Meaning:** D2 recovers *every* classical result exactly as a special case — a
mandatory consistency check that the theorem passes. (The bible notes the *additive* form $h_R + \Delta(p)$ from
an earlier draft *fails* this check — it cannot reproduce $p\lambda^2 < 1$ — which is why the *multiplicative*
$\gamma$ form is correct.)

---

# SECTION 8 — PROOFS (every step, every inequality, every trick)

> **How to read.** For each proof: (0) goal; (1) strategy and why it works; (2) step-by-step with every
> inequality justified. External results are taught inline.

## 8.1 Necessity D2★ = Lemma C (burst expansion) + Lemma D (moment divergence) + Lemma R (rate)

**Overall strategy.** Two independent impossibility arguments. Lemma D proves the *reliability* necessity (A) by
showing a divergent series of burst contributions. Lemma R proves the *rate* necessity (R) by a law-of-large-
numbers + volume-counting argument. Lemma C is the shared engine: it quantifies how much a burst expands the
uncertainty.

### 8.1.1 Lemma C — Uniform Burst Expansion (every step)

**Goal.** During a length-$b$ erasure burst (no control delivered), the uncertainty set expands by at least
$e^{b r^\star_{\mathrm{top}}}$ in *diameter* and $e^{b r^\star_{\mathrm{vol}}}$ in *volume*, *uniformly* over
where the set sits in $K$.

**Strategy.** Track how the map inflates a set over $b$ steps, using the Jacobian's singular values, and — the
crucial move — bound the inflation by the *worst-case (sup over $K$)* rate, so it holds for *any* orbit, not
just typical ones.

**Step 1 (volume).** By the change-of-variables formula, $\mathrm{Vol}(f^b(\mathcal U)) = \int_{\mathcal U}
\prod_{s=0}^{b-1} |\det Df(x_s)|\,d\mathrm{Vol}$. Now $|\det Df(x)| = \prod_i \sigma_i(Df(x)) \ge \prod_i
\max(1,\sigma_i) = e^{\sum_i \log^+\sigma_i(Df(x))}$. Taking the optimal metric $g^\star$ that achieves the
$\inf_g$, the exponent is $\le r^\star_{\mathrm{vol}}$ with the $\sup_K$ attained, so $\prod_s |\det Df(x_s)| \ge
e^{b\,r^\star_{\mathrm{vol}}(1-o(1))}$ **regardless of the orbit** $\{x_s\}$. *The crux:* this uniformity holds
because $r^\star_{\mathrm{vol}}$ is a $\sup_K$, *not* an average — a Lyapunov/Pesin average would hold only for
*typical* orbits, but a *burst* can strike the *worst* orbit. *What would fail with an average:* you could not
guarantee expansion during the worst burst, and the necessity would not be uniform over all schemes.

**Step 2 (diameter).** The image $f^b(\mathcal U)$ contains a segment stretched along the most-expanding
direction by $\prod_s \sigma_1(Df(x_s)) \ge e^{b\,r^\star_{\mathrm{top}}(1-o(1))}$ (pick two points of $\mathcal
U$ separated along the top singular direction; their images separate by the product of top singular values).
Hence $\mathrm{diam}(f^b(\mathcal U)) \ge \mathrm{diam}(\mathcal U)\,e^{b r^\star_{\mathrm{top}}(1-o(1))}$.

**Step 3 (why $r^\star$, not $h_{\mathrm{top}}$).** For the *rate* branch use volume (Step 1) via the
isodiametric inequality; for the *moment* branch use diameter directly (Step 2). Topological entropy counts
distinguishable *orbits*, not Jacobian volume/length expansion — it is the *wrong* object here; the singular-
value rate $r^\star$ is exactly the volume/length expansion rate.

**Step 4 (the $o(1)$ is harmless).** For uniformly hyperbolic $f$, $o(1)=0$. For general $C^1$ there can be
sub-exponential corrections $e^{o(b)}$ per factor, but the series in Lemma D converges/diverges by the *ratio
test* at ratio $p\,e^{m r^\star}$, which is *unchanged* by sub-exponential factors (the ratio of consecutive
$o(b)$ terms $\to 1$). So the threshold is robust to the $o(1)$. $\blacksquare$

### 8.1.2 Lemma D — Renewal Moment Divergence (every step, proving condition (A) is necessary)

**Goal.** If $p\,e^{m r^\star_{\mathrm{top}}} \ge 1$ then $\limsup_t \mathbb E[e_t^m] = \infty$, for *every*
causal scheme, with or without ACK.

**Step 1 (burst law).** In i.i.d. erasure, runs of consecutive erasures are geometric: $\Pr[\text{run}=b] =
(1-p)p^b$. Such runs *recur infinitely often* almost surely (there is always another burst coming).

**Step 2 (post-burst error).** At a burst's start the error is at least the quantizer floor $\varepsilon_0 > 0$
(finite rate cannot give zero error). By Lemma C, after a length-$b$ burst the error is $\ge \varepsilon_0\,
e^{b r^\star_{\mathrm{top}}(1-o(1))}$ (the estimator cannot resolve within the uncertainty set, so error $\ge
\tfrac12$ diameter).

**Step 3 (moment contribution of a length-$b$ burst).** $\mathbb E[e^m \mid \text{burst } b]\cdot \Pr[\text{burst
} b] \ge \varepsilon_0^m\,e^{m r^\star_{\mathrm{top}} b(1-o(1))}\,(1-p)p^b$.

**Step 4 (the divergent series — the heart).** Summing over burst lengths,
$$ \mathbb E[e^m] \gtrsim \varepsilon_0^m (1-p) \sum_b \big(p\,e^{m r^\star_{\mathrm{top}}}\big)^b\,e^{-m
r^\star_{\mathrm{top}} o(b)}, $$
a geometric series in $b$ with ratio $p\,e^{m r^\star_{\mathrm{top}}}$. By the *ratio test*, it **diverges iff
$p\,e^{m r^\star_{\mathrm{top}}} \ge 1$**. *Intuition:* the moment is a sum over burst lengths of
(probability of the burst) $\times$ (error$^m$ it causes); the probability shrinks like $p^b$ but the error$^m$
grows like $e^{m r^\star b}$ — whichever wins the exponential race decides. *What would fail if the ratio test
were misapplied:* the sub-exponential $o(b)$ factors do not change the ratio (Step 4 of Lemma C), so the
threshold is exactly $p\,e^{m r^\star} = 1$.

**Step 5 (between-burst contraction cannot save it).** Each delivered slot conveys $\le R$ nats, contracting the
error by at most $e^{-R}$ (an information floor: you cannot reduce a $d$-nat uncertainty by more than the nats
you received). Between bursts there are $\sim 1/p$ delivered slots on average, a *finite* contraction per cycle.
A *fixed finite factor* multiplying a *divergent* geometric series in burst length cannot make it converge — the
divergence is driven by the *heavy tail* of *long* bursts, where no bounded between-burst contraction reaches.

**Step 6 (ACK / prediction cannot save it — the subtle part).** Suppose the controller learns each slot's
erasure indicator (causal ACK). Can it *pre-shrink* the error before a burst? *No:* (i) future erasures are
independent of the past (memoryless), so burst onset/length is *unpredictable* — you cannot allocate extra rate
before a burst you cannot foresee; (ii) even holding the error at the floor $\varepsilon_0$ between bursts, you
*enter* each burst at $\ge \varepsilon_0$, and Lemma C applies; (iii) by Borel–Cantelli, runs of length $\ge b_0$
occur infinitely often for any $b_0$, so the per-occurrence moment $\ge \varepsilon_0^m e^{m r^\star b_0}$ is
arbitrarily large infinitely often $\Rightarrow \limsup_t \mathbb E[e_t^m] = \infty$. ACK changes the achievable
*code* (enables retransmission) but not this *necessity*, because capacity is feedback-invariant for memoryless
channels and burst unpredictability is feedback-invariant. $\blacksquare$

### 8.1.3 Lemma R — Rate Condition Necessity (every step, proving condition (R) is necessary)

**Goal.** If $R(1-p) < h_R(f|_Q)$ then $\limsup_t \mathbb E[e_t^m] = \infty$ for every scheme (indeed almost-sure
escape).

**Step 1 (delivered-nat count, law of large numbers).** Over $n$ steps, the delivered nats total $D_n = R\sum_t
\mathbf 1\{\text{delivered}_t\}$. Since deliveries are i.i.d. Bernoulli$(1-p)$, by the Strong Law of Large
Numbers $D_n/n \to R(1-p)$ almost surely. *Intuition:* your long-run average received rate is $R(1-p)$, no more.

**Step 2 (volume counting).** By the Matveev–Pogromsky/Nair–Evans volume-counting necessity applied to the
*realized* delivery sequence: over $n$ steps the observer receives $\le D_n$ nats of state information, while the
uncertainty *volume* grows by $\ge e^{n r^\star_{\mathrm{vol}}(1-o(1))}$ (Lemma C, volume branch), which requires
$\ge n\,h_R(1-o(1))$ nats to keep bounded. If $D_n < n\,h_R(1-o(1))$, the volume is unbounded, so the error is
unbounded. *Intuition:* the system *creates* uncertainty at rate $h_R$; if you *receive* information slower than
that, the leftover uncertainty accumulates without bound.

**Step 3 (a.s. instability).** By Step 1, $D_n/n \to R(1-p) < h_R$, so for large $n$ (a.s.) $D_n < n h_R(1-
\epsilon)$; by Step 2 the volume grows unboundedly, giving $e_t \to \infty$ almost surely.

**Step 4 (a.s. to moment).** $e_t \to \infty$ a.s. $\Rightarrow \limsup_t \mathbb E[e_t^m] = \infty$ by Fatou's
lemma. $\blacksquare$ *Key subtlety (bible note):* the substitution $R \mapsto R(1-p)$ is *not an approximation*
but an exact almost-sure statement (SLLN); arrival *fluctuations* are a second-order effect governed by (A), not
(R).

## 8.2 Achievability D2★★ = Lemma A-D2 (UZQ) + Lemma B-D2 (drift) + Lemma C-D2 (cat verification)

**Overall strategy.** Build a controller whose error's $m$-th-moment drift is exactly $\gamma$, then apply a
geometric-drift stability criterion to conclude bounded moment iff $\gamma < 1$.

### 8.2.1 Lemma A-D2 — the Universal Zooming Quantizer (solving the state-dependent-grid problem)

**The obstacle.** For a *nonlinear* system the right quantizer grid depends on the *local* expansion, which
depends on the *state* — but the controller does not *know* the state (that is the whole problem). A naive
adaptive grid would need the encoder to use $Df(x)$ and the decoder to use $Df(\hat x)$, and they would
*disagree* (desynchronize).

**The fix (common-information partition).** Encoder and decoder both maintain the uncertainty set $\Omega_t$ as
a deterministic function of the *shared index history* $j_{1:t-1}$ and the map $f$ — *not* of the unknown $x_t$.
So they compute the *identical* grid: (1) *predict* $\Omega_t^- = f(\Omega_{t-1})$, radius inflated by the local
top expansion $\sigma_1(Df(c_t^-))$ at the *known center* $c_t^-$; (2) *tile* $\Omega_t^-$ into $\lceil e^R
\rceil$ congruent cells in the optimal metric $g^\star$, each of radius $\delta_t^- e^{-R/d^+}$ — the grid
"zooms" exactly to the local expansion; (3) *encode* the true cell's index $j_t$; (4) *update* $\Omega_t = $ the
chosen cell. Because both parties evaluate $Df$ at the *same* known centers, there is *no mismatch, no
chicken-and-egg*.

**Synchronization without ACK.** Feed the index stream to a Sahai–Mitter *anytime tree code* over the erasure
channel. During a burst the decoder holds a *stale but strictly containing* $\Omega_t$ (a valid over-bound — it
never commits to a *wrong* cell); when the anytime backlog is delivered (reliability $\ln(1/p)$), $\Omega_t$
re-synchronizes. The scale $\delta_t$ is a deterministic function of the indices, so embedding them in the
anytime stream transmits the scale automatically — *no side channel, no ACK*.

**Zero waste (why the rate floor is exactly $h_R$).** In the optimal metric $g^\star$ (Matveev–Pogromsky), the
predicted volume grows by exactly $e^{h_R}$ and the rate-$R$ tiling contracts by $e^{-R}$, so the per-step
radius factor on delivery is $\alpha = e^{(h_R - R)/d^+} < 1 \iff R > h_R$. Because $g^\star$ *uniformizes*
expansion, *no state wastes rate* — hence the threshold is *exactly* $h_R$, with *no* $+\varepsilon$ margin.

### 8.2.2 Lemma B-D2 — the drift (proving stable iff $\gamma < 1$)

**The recursion.** With the UZQ, the error radius obeys $\delta_{t+1} = \alpha\,\delta_t$ on a delivered slot
(prob $1-p$) and $\delta_{t+1} = \Lambda\,\delta_t$ on an erased slot (prob $p$), where $\alpha = e^{(h_R-R)/d^+}$
and $\Lambda = e^{r^\star_{\mathrm{top}}}$ (Lemma C, D2★).

**The drift.** Using the Lyapunov function $V(e) = e^m$,
$$ \mathbb E[V(e_{t+1}) \mid e_t] \le \big[(1-p)\alpha^m + p\Lambda^m\big] V(e_t) = \gamma\,V(e_t). $$
*This is exactly the $\gamma$ of the theorem.* Each term is a resource: $(1-p)\alpha^m$ = contraction bought by
delivered slots; $p\Lambda^m$ = expansion inflicted by erased slots.

**Sufficiency.** By the *geometric-drift criterion* (Meyn–Tweedie, *Markov Chains and Stochastic Stability*, Thm
15.0.1) with the bounded quantizer floor $b$, $\gamma < 1 \Rightarrow \limsup_t \mathbb E[e_t^m] \le b/(1-\gamma)
< \infty$. *Intuition:* a random walk with a per-step multiplier $\gamma < 1$ and a floor settles to a bounded
stationary moment; $\gamma \ge 1$ makes it grow without bound (Lemma D). $\blacksquare$

**Necessity of $\gamma < 1$ (tightness).** No rate-$R$ quantizer contracts faster than $\alpha$ (the rate/volume
floor), and bursts expand by $\ge \Lambda$ uniformly (Lemma C), so the optimal per-step $m$-th-moment multiplier
is $\ge \gamma$; hence $\gamma \ge 1 \Rightarrow$ divergence. So *stable $\iff \gamma < 1$* — zero gap.

### 8.2.3 Lemma C-D2 — the cat-map verification (no quasi-conformality needed)

**The worry.** The cat map has $\sigma_1 = \lambda_u \ne \sigma_2 = \lambda_s$ — it is *not* quasi-conformal (it
stretches unevenly). Does the UZQ still work?

**The answer.** Yes: use $d^+ = 1$ (one expanding direction), $h_R = r^\star_{\mathrm{top}} = \ln\lambda_u$, and
the optimal metric $g^\star$ = the eigenbasis metric (the Jacobian is constant). The UZQ zooms *only* along the
unstable eigendirection (cell size $\propto \lambda_u^{-1}$) and *ignores* the contracting direction (which
self-stabilizes). Then $\alpha = \lambda_u e^{-R}$, $\Lambda = \lambda_u$, so $\gamma = \lambda_u^m[(1-p)e^{-mR}
+ p]$. For $m=2$: stable iff $(1-p)e^{-2R} + p < \lambda_u^{-2} \approx 0.146$; as $R \to \infty$, $p_c(2) =
\lambda_u^{-2} \approx 0.146$; as $p \to 0$, the critical rate $\to \ln\lambda_u = h_R$. So the cat map is
stabilized at *exactly* $h_R$ with $\sigma_1 \ne \sigma_2$, *without* quasi-conformality. $\blacksquare$

### 8.2.4 Composition

Lemma A-D2 builds the mismatch-free, no-ACK UZQ; Lemma B-D2 proves stable $\iff \gamma < 1$ (sufficiency via
geometric drift; necessity via the rate-distortion contraction floor + Lemma C burst expansion); Lemma C-D2
verifies the non-quasi-conformal cat map. Hence for general $C^1$ expansive $f$ the closed-loop $m$-th-moment
threshold is the exact surface $\gamma = 1$, with (R) and (A) as marginals, infimal rate exactly $h_R$ as $p\to
0$, no $\varepsilon$ back-off. $\blacksquare$

## 8.3 The vector two-rate structure and the optimal-metric spectral radius (deriving the M-experiment numbers)

**Two rates for a diagonal vector system** $\mathrm{diag}(e^{a_1}, e^{a_2}, \dots)$ with $a_i > 0$: the *rate*
condition uses $r^\star_{\mathrm{vol}} = \sum_i a_i$ (you must encode *every* expanding mode); the *reliability*
condition uses $r^\star_{\mathrm{top}} = \max_i a_i$ (the *fastest* mode drives the moment's heavy tail). A coder
that provisions rate *proportional to each mode's expansion* keeps every mode at its a.s. boundary
simultaneously; a "top-only" coder starves the sub-dominant modes and they diverge. *(This is exactly D2-M1:
$r^\star_{\mathrm{vol}} = 1.4$, $r^\star_{\mathrm{top}} = 1.0$.)*

**Non-normal systems and Gelfand's formula.** For a non-normal $A$, a *single* step can stretch by $\|A\|$, but
a length-$b$ burst stretches by $\|A^b\|$, and $\|A^b\|^{1/b} \to \rho(A)$ (Gelfand). Since the moment's heavy
tail is dominated by *long* bursts, the effective per-step expansion is $\rho(A)$, so the moment threshold is
$p_c(m) = \rho(A)^{-m}$, *not* $\|A\|^{-m}$. The optimal metric $g^\star$ that achieves $r^\star_{\mathrm{top}} =
\inf_g \sup_x \log^+\sigma_1(Df;g)$ collapses the operator norm to the spectral radius; the metric affects the
*constant*, not the *exponent*. *(This is exactly D2-M4: threshold $\rho^{-m}$, not $\|A\|^{-m}$.)*

---

# SECTION 9 — EXPERIMENTS (scientific explanation, not code)

## 9.0 The measurement problem, and how it is solved (read before any experiment)

**The obstacle.** The stability threshold is decided by the $m$-th moment $\mathbb E[\delta^m]$, which is
*dominated by rare, erasure-heavy trajectories* (long bursts). A naive Monte-Carlo simulation almost never
generates a long burst, so it *systematically under-estimates* the moment — by 1–2 orders of magnitude — and
would falsely report stability where there is none. The naive protocol suggested in the bible is therefore
*infeasible* for these moments.

**The solution: importance sampling (IS).** Simulate the erasure process under a *tilted* probability $q > p$
(erasures made artificially common, so the rare heavy paths become typical), then *reweight* each trajectory by
the likelihood ratio to remove the bias. With the analytically-optimal tilt $q^\star = p\,e^{m r^\star}/\gamma$,
the estimator is essentially exact (zero variance for the i.i.d. multiplicative walk). The closed-form $\gamma =
(1-p)e^{m(r^\star-R)} + p\,e^{m r^\star}$ is the ground truth. Experiment D2-E1 shows the three side by side:
naive MC (fails), IS (matches), exact (the target).

**Two order parameters.** (i) The *a.s. / drift* transition (whether the error diverges *almost surely*) is
governed by *typical* paths and is measurable by *plain* Monte Carlo — its threshold is the drift condition (R),
$p_R = 1 - r^\star/R$. (ii) The *$m$-th-moment* transition is governed by *rare* paths and needs IS — its
threshold is condition (A), $\gamma(m) = 1$. Keeping these two straight is essential to reading the results.

## 9.1 Experiment D2-E1 — the exact threshold; naive MC fails, IS succeeds

**Purpose / theorem.** Validate the exact moment multiplier $\gamma(m)$ and the marginal $p_c(m) = e^{-m
r^\star} = k^{-m}$; and *demonstrate the methodological point* that naive MC cannot measure it.

**Hypothesis.** IS recovers the analytic $\gamma$ exactly; naive MC under-estimates; $\gamma(m)$ crosses 1 at
$p_c(m) = k^{-m}$.

**Model / parameters.** Circle map $k=2$ ($r^\star = \ln 2 = 0.6931$), large rate $R = r^\star + 4 = 4.6931$
(so the transition sits at the reliability marginal), moments $m \in \{1,2,4\}$, sweep $p$.

**Metric.** Measured $p_c(m)$ (where $\gamma_{\mathrm{IS}} = 1$) vs the parameter-free prediction $k^{-m}$.

**Observed (from `resultsD2.md`).** $p_c$: $m=1: 0.4954$ (pred $0.5$), $m=2: 0.2499$ (pred $0.25$), $m=4: 0.0625$
(pred $0.0625$) — essentially exact. Naive MC under-estimates $\gamma$ by $\sim 40\times$ near the threshold.

**Interpretation.** The parameter-free reliability law $p_c(m) = k^{-m}$ is confirmed to $\sim 10^{-3}$; and the
figure with naive MC (far below), IS (on the curve), and exact (the line) proves IS is *mandatory* — a
methodological contribution.

## 9.2 Experiment D2-E2 — the two conditions are independent (and a correction to the bible)

**Purpose / theorem.** Show conditions (R) and (A) are *distinct* transitions, and *correct* the bible's §2.7.1,
which wrongly located the circle $m=2$ transition at $p_c = 1/4$ for a *finite* rate.

**Hypothesis.** At a *fixed finite* rate, the a.s./drift transition is at $p_R = 1 - r^\star/R$, and the moment
transitions $p_A(m)$ are *below* it, forming a cascade (higher $m$ = lower threshold).

**Parameters.** Circle $k=2$, $R = \ln 2 + 0.1 = 0.7931$ (the bible's value). Compute $p_R$ and $p_A(m)$ for $m
\in \{1,2,4\}$.

**Observed.** $p_R = 1 - r^\star/R = 0.1261$. Moment thresholds $p_A(m)$: predicted *and measured*
$\{1: 0.0869,\ 2: 0.0570,\ 4: 0.0215\}$. **None equal $0.25$** — the value $1/4$ is the $R \to \infty$ marginal,
*not* the finite-rate threshold. The cascade $p_A(4) < p_A(2) < p_A(1) < p_R$ is confirmed.

**Interpretation.** Two genuinely independent transitions from two mechanisms. And a *correction*: at $R = \ln2
+ 0.1$ the exact $m=2$ threshold is $\approx 0.057$, not $0.25$; the bible conflated the finite-rate exact
threshold with the infinite-rate marginal. This is exactly the kind of scope-precision that strengthens the work.

## 9.3 Experiment D2-E3 — the parameter-free scaling law across surrogates

**Purpose / theorem.** Validate $p_c(m) = e^{-m r^\star}$ across systems with *different* $r^\star$ — the
discriminating fingerprint.

**Hypothesis.** $\ln p_c(m)$ is linear in $m$ with slope $-r^\star$, for each surrogate.

**Parameters.** Three surrogates: circle $k=2$ ($r^\star = \ln 2$), circle $k=3$ ($r^\star = \ln 3$), cat map
($r^\star = \ln\lambda_u \approx 0.962$); large rate $R = r^\star + 5$; $m \in \{1,2,3,4\}$; IS.

**Observed.** The law $\ln p_c(m) = -r^\star m$ holds across all three $r^\star$ values and all $m$.

**Interpretation.** A *single, zero-parameter* functional form predicts twelve thresholds across two map
families — the strongest kind of confirmation (no fitting).

## 9.4 Experiment D2-E4 — the full $(p, R)$ phase diagram

**Purpose / theorem.** Validate the *entire* threshold surface $\gamma(p,R,m) = 1$, not just its two marginals.

**Hypothesis.** The measured $\gamma = 1$ boundary in the $(p, R)$ plane coincides with the exact analytic curve
$R_c(p)$; it asymptotes to $R \to \infty$ as $p \to p_c(2) = 1/4$ and to $R \to h_R = \ln 2$ as $p \to 0$.

**Parameters.** Circle $k=2$, $m=2$; a 2-D grid over $(p, R)$; measure $\gamma$ by IS at each.

**Observed.** Measured vs exact boundary $R_c(p)$: mean absolute error $= 0.0036$ nats over 18 $p$-columns; both
marginals recovered (the $p_c(2)=1/4$ vertical asymptote and the $h_R = \ln 2$ floor).

**Interpretation.** The *whole* exact surface is validated, not just the two classical conditions — the complete
2-parameter law.

## 9.5 Experiment D2-E5 — achievability (UZQ) faithfulness and sufficiency

**Purpose / theorem.** Confirm (a) the UZQ reduction is *faithful* (a genuine 2-D cat-map observer matches the
reduced 1-D unstable-direction walk), and (b) the UZQ *achieves* bounded moment exactly when $\gamma < 1$.

**Hypothesis.** (a) The 2-D observer's escape curve equals the 1-D walk's. (b) $\mathbb E[\delta^2]$ saturates
(bounded) for $p < p_c$ and grows for $p > p_c$.

**Parameters.** Cat map, genuine 2-D observer vs reduced walk; and a sufficiency test at $R = h_R + 0.5$.

**Observed.** (a) Faithfulness MAE $= 0.0001$ (indistinguishable); both transition at $p_R = 0.094$. (b) At $R =
h_R + 0.5$, $p_c = 0.174$; $\ln \mathbb E[\delta^2]$ saturates for $p < p_c$ and grows linearly (slope $\ln
\gamma > 0$) for $p > p_c$.

**Interpretation.** The zooming-only-along-the-unstable-direction construction is *exactly right* (the 2-D
observer matches the 1-D reduction), and the UZQ genuinely stabilizes when $\gamma < 1$ — the achievability made
concrete.

## 9.6 Experiment D2-E6 — the Hénon stress test (why restoration, not Lyapunov)

**Purpose / theorem.** On a *non-uniformly* hyperbolic map (Hénon), show the a.s. behavior follows the *average*
(Lyapunov) rate while the higher-moment/uniform guarantee needs the *worst-case* (restoration) rate — the honest
demonstration of Contribution 3.

**Hypothesis.** The a.s. escape threshold matches the Lyapunov-average prediction, not the worst-case; the
effective moment rate $r_{\mathrm{eff}}(m) = \tfrac1m \ln \mathbb E[\sigma_1^m]$ rises from the Lyapunov exponent
toward the worst-case as $m$ grows.

**Parameters.** Hénon map (chaotic, non-uniform); measure the Lyapunov exponent and the worst-case log-expansion
on the attractor.

**Observed.** Lyapunov exponent $\lambda = 0.7255$; worst-case $\ln\sigma_{\max} = 1.3203$. $r_{\mathrm{eff}}(m)$
rises monotonically from $0.725$ toward $1.320$. Observed a.s. escape $p_c = 0.5171$; Lyapunov prediction $p_R =
0.5523$ (error $0.0352$); worst-case prediction $0.1851$ (far off for a.s.).

**Interpretation.** a.s./typical behavior *is* Lyapunov-governed (observed $0.517$ vs Lyapunov $0.552$), *not*
worst-case ($0.185$) — a subtle, honest point. But higher moments and *uniform* guarantees need the worst-case
(restoration) rate, which is why the bible uses $h_R$ (a sup) and why uniform surrogates (circle/cat, where the
two coincide) are the clean primary tests. This is a *mechanism* validation, not an exact threshold (Hénon's
$h_R$ has no closed form) — stated honestly.

## 9.7 Experiment D2-E7 — Gilbert–Elliott bursts (i.i.d. is optimistic)

**Purpose / theorem.** Show correlated bursts destabilize at a *lower average loss* than i.i.d. — so the i.i.d.
threshold is a necessary-but-optimistic screen.

**Hypothesis.** At matched *average* loss, a bursty channel escapes at a lower mean-$p$ than i.i.d.

**Parameters.** Circle map; i.i.d. vs Gilbert–Elliott with mean burst length 10.

**Observed.** i.i.d. escape midpoint $p_c = 0.3959$; Gilbert–Elliott $p_c = 0.0354$ — the bursty channel loses
track at *one-tenth* the average loss.

**Interpretation.** Burst correlation is drastically more damaging than i.i.d. at the same average rate — the
i.i.d. clean threshold is *optimistic* for real (bursty, incast-prone) links. Motivates the spectral-radius
generalization (D2-M3).

## 9.8 Experiment D2-M1 — the vector two-rate structure ($r^\star_{\mathrm{vol}} \ne r^\star_{\mathrm{top}}$)

**Purpose / theorem.** The first genuine test that the *rate* condition uses $r^\star_{\mathrm{vol}}$ while the
*reliability* condition uses $r^\star_{\mathrm{top}}$ — impossible on scalar surrogates.

**Hypothesis.** On a vector system with $r^\star_{\mathrm{vol}} = 1.4 \ne r^\star_{\mathrm{top}} = 1.0$: the
a.s./rate transition binds on $r^\star_{\mathrm{vol}}$; the moment/reliability threshold binds on
$r^\star_{\mathrm{top}}$; a "top-only" coder starves sub-dominant modes.

**Parameters.** Diagonal system $\mathrm{diag}(e^{1.0}, e^{0.4})$; proportional vs top-only rate allocation.

**Observed.** a.s. escape (proportional allocation) transitions at $p = 0.3286$, matching $p_R(r^\star_{\mathrm{
vol}}) = 0.3636$ (**not** $p_R(r^\star_{\mathrm{top}}) = 0.5455$). A top-only allocation escapes *much earlier*
(the sub-dominant mode blows up). The moment thresholds $p_c(m) = e^{-m r^\star_{\mathrm{top}}}$: measured
$\{1: 0.3613,\ 2: 0.1352,\ 4: 0.0183\}$ vs predicted $\{1: 0.3679,\ 2: 0.1353,\ 4: 0.0183\}$.

**Interpretation.** The two rates are *genuinely separated*: rate uses volume, reliability uses top. A single
scalar surrogate could never reveal this; it is the decisive confirmation of the two-rate (COR-3) structure.

## 9.9 Experiment D2-M2 — map universality

**Purpose / theorem.** Show the threshold depends *only* on $r^\star$, not on the map's other details —
universality.

**Parameters.** Five maps via genuine interval-quantizer observers, including the tent map ($s=2$) and the
doubling map (*both* with $r^\star = \ln 2$).

**Observed.** The a.s. escape threshold $p_R = 1 - r^\star/R$ holds (mean error $0.0339$); $p_c(m) = e^{-m
r^\star}$ collapses across all maps and $m \in \{1,2,4\}$ (mean log-error $0.0017$); crucially, the tent and
doubling maps — same $r^\star = \ln 2$ — give the *same* $p_c$, confirming $p_c$ depends only on $r^\star$.

**Interpretation.** Universality confirmed: two structurally different maps with equal $r^\star$ have equal
thresholds. The theory's *only* map-dependence is through $r^\star$.

## 9.10 Experiment D2-M3 — burst length and the spectral-radius conjecture

**Purpose / theorem.** Quantitatively test the Gilbert–Elliott generalization (Conjecture D2-Markov): stability
$\iff \rho(M) < 1$ for the modulated transfer matrix.

**Hypothesis.** (a) At a *safe* average loss for i.i.d., increasing burst length eventually destabilizes. (b)
The moment growth rate equals $\ln\rho(M)$.

**Parameters.** Fixed mean erasure $\bar p = 0.1$ (below the i.i.d. a.s. threshold $p_R = 0.419$); vary mean
burst length $L$; measure the transfer-matrix moment growth across a parameter grid.

**Observed.** (a) Escape probability rises from $0.000$ at $L=1$ (i.i.d.) to $1.000$ at $L=50$ — correlated
bursts destabilize even when the *average* loss is safe. (b) The measured moment growth rate matches $\ln\rho(M)$
to MAE $0.0009$; its zero crossing ($\rho = 1$) is the boundary.

**Interpretation.** The spectral-radius threshold is *numerically exact*. The i.i.d. clean threshold is thus a
necessary-but-optimistic screen. *Status:* a first-principles proof for nonlinear maps under Markov channels is
*open* (honestly documented as future work).

## 9.11 Experiment D2-M4 — the optimal-metric (spectral radius vs operator norm)

**Purpose / theorem.** On *non-normal* systems where $\|A\| \gg \rho(A)$, test whether the reliability rate is
$\rho(A)$ (optimal metric, the bible's claim) or the naive $\|A\|$ (operator norm).

**Hypothesis.** The moment threshold is $\rho(A)^{-m}$, *not* $\|A\|^{-m}$.

**Parameters.** Three non-normal matrices with $\|A\|/\rho(A)$ up to $4.2\times$ (including complex-eigenvalue
rotations).

**Observed.** The measured moment threshold matches the spectral-radius prediction $\rho(A)^{-m}$ to MAE
$0.0087$, while the naive operator-norm prediction $\|A\|^{-m}$ is off by MAE $0.3011$ — $35\times$ larger error.

**Interpretation.** The optimal-metric spectral-radius rate is confirmed as operationally correct, on systems
that scalar/normal surrogates cannot probe. The mechanism is Gelfand's formula: long bursts self-average to
$\rho(A)$. This closes the "is the metric optimization real?" reviewer concern.

---

# SECTION 10 — VALIDATION (proving vs validating; what experiments can and cannot do)

## 10.1 Proving vs validating

A *proof* (Section 8) establishes the threshold with certainty from the assumptions. An *experiment* checks the
proof's *predictions* on specific systems, catching implementation bugs, hidden-assumption violations, and
arithmetic errors, and building confidence that the assumptions hold in realizable systems. Experiments cannot
prove a theorem (finitely many cases) nor rescue a false one; disagreement signals a bug or a violated
assumption — which is how, e.g., the bible's §2.7.1 mis-statement ($p_c=1/4$ at finite rate) was caught.

## 10.2 What the D2 experiments validate

- **The exact threshold $\gamma = 1$:** the full $(p,R)$ surface to $0.0036$ nats (D2-E4); the reliability
  marginal $p_c(m) = e^{-m r^\star}$ to $\sim 10^{-3}$ across two map families and four moments (D2-E1/E3).
- **Two independent conditions:** distinct a.s. and moment transitions, with the correct cascade (D2-E2).
- **The two-rate structure:** rate uses $r^\star_{\mathrm{vol}}$, reliability uses $r^\star_{\mathrm{top}}$, on a
  genuine vector system (D2-M1).
- **The optimal-metric rate:** $\rho(A)^{-m}$, not $\|A\|^{-m}$, on non-normal systems (D2-M4).
- **Achievability (UZQ):** faithful reduction (MAE $10^{-4}$) and genuine stabilization for $\gamma < 1$ (D2-E5).
- **Universality:** threshold depends only on $r^\star$ (D2-M2).
- **The Gilbert–Elliott generalization:** the spectral-radius growth rate to MAE $0.0009$ (D2-M3).

## 10.3 What the experiments *cannot* validate (remaining assumptions / honest gaps)

- **A first-principles proof of the Gilbert–Elliott (spectral-radius) threshold for nonlinear maps.** Numerically
  exact, but proven only in spirit (You–Xie's linear analog + Furstenberg–Kesten products) — *open*.
- **An exact threshold for non-uniform maps (Hénon/Lorenz).** Their $h_R$ has no closed form, so D2-E6 is a
  *mechanism* validation (average vs worst-case), not an exact threshold.
- **An explicit symbol-level no-ACK anytime tree code.** The UZQ's anytime layer is *modeled* by "the index
  stream is eventually delivered." *However*, the reliability *claim* it must satisfy — $\alpha_{\mathrm{ch}} =
  \ln(1/p) > m r^\star$ — *is* validated, because the burst-tail mechanism $p^b$ that drives moment divergence
  (D2-E1/E2) is exactly this anytime exponent. So only the specific code *engineering* is future work, not the
  reliability *result*.

## 10.4 What the adversarial validation found and fixed (from `VALIDATION_AUDIT.md`)

- **G5 — the two-rate structure was never tested (critical).** Only scalar/quasi-conformal surrogates were used,
  where $r^\star_{\mathrm{vol}} = r^\star_{\mathrm{top}}$. **Fixed** by D2-M1 (vector system, rates $1.4$ vs
  $1.0$), the first genuine separation.
- **G6 — faithfulness only for the cat map.** **Fixed** by D2-M2 (five maps + universality).
- **G7 — Gilbert–Elliott only qualitative.** **Fixed** by D2-M3 (spectral radius to $0.0009$).
- **G10 — optimal metric never tested (only normal systems).** **Fixed** by D2-M4 (non-normal $\|A\| \gg
  \rho$; threshold is $\rho^{-m}$), upgrading D2★ (necessity) confidence to VERY HIGH.
- A *methodological* fix throughout: naive MC replaced by importance sampling (D2-E1), because the naive protocol
  under-estimates the rare-event moment.

## 10.5 Confidence levels (the audit's grading)

| Claim | Confidence | Basis |
|---|---|---|
| D2★ necessity (incl. two-rate) | **Very high** | exact surface + genuine $r^\star_{\mathrm{vol}} \ne r^\star_{\mathrm{top}}$ + non-normal $\rho$ vs $\|A\|$ |
| D2★★ UZQ achievability | **High** | faithful on 5 maps + universality; anytime code *modeled* (its reliability condition validated) |
| Conjecture D2-Markov (bursts) | **Medium-high** | spectral radius numerically exact ($0.0009$); proof open |
| Non-uniform exact $h_R$ | **Open** | mechanism only (Hénon has no closed-form $h_R$) |

## 10.6 Reproducibility

Fresh-seed certification (from `resultsD2.md`): $\gamma(2)$ at $p_c = 1/4$ over 12 fresh seeds $= 1.0003 \pm
0.0000$ (exact $= 1.0003$); the escape rate at $p_R = 0.126$ over 10 fresh seeds $= 0.837 \pm 0.003$. All
headline conclusions reproduce under never-before-used seeds.

---

# SECTION 11 — FIGURES (what each shows, how to read it, expected vs observed, conclusion)

In `results/d2/figures/` (PNG + PDF + SVG).

## 11.1 `D2-E1a_mc_vs_is`
- **Axes.** $x$: erasure probability $p$; $y$: moment multiplier $\gamma(2)$.
- **What is drawn.** The exact analytic $\gamma$ (line), the importance-sampling estimate (points on the line),
  and the naive Monte-Carlo estimate (points far below); a horizontal line at $\gamma=1$; a vertical line at
  $p_c(2)=1/4$.
- **Expected.** IS on the line crossing 1 at $1/4$; naive MC below.
- **Observed.** IS matches exactly; naive MC under-estimates by $\sim 40\times$.
- **Conclusion.** IS is mandatory; the marginal threshold is $p_c(2)=1/4$.

## 11.2 `D2-E1b_pc_scaling`
- **Axes.** $x$: $p$; $y$: $\gamma(m)$ for $m=1,2,4$.
- **Expected/Observed.** Each $\gamma(m)$ crosses 1 at $k^{-m} = \tfrac12, \tfrac14, \tfrac1{16}$.
- **Conclusion.** The $m$-scaling $p_c(m) = k^{-m}$ holds.

## 11.3 `D2-E2_two_conditions`
- **Axes.** $x$: $p$; two overlaid transitions — the a.s. escape rate (drift, condition R) and the moment
  multipliers $\gamma(m)$ (condition A).
- **Expected.** The a.s. transition at $p_R = 0.126$; the moment crossings *before* it, cascading with $m$.
- **Observed.** $p_R = 0.1261$; $p_A = \{0.087, 0.057, 0.0215\}$ for $m=1,2,4$ — a clear cascade, none at $0.25$.
- **Conclusion.** Two independent conditions; corrects the bible's §2.7.1.

## 11.4 `D2-E3_scaling_law`
- **Axes.** $x$: moment $m$; $y$: $\ln p_c(m)$; three lines for the three surrogates.
- **Expected.** Straight lines of slope $-r^\star$ ($-\ln2, -\ln3, -\ln\lambda_u$).
- **Observed.** Exactly; a single zero-parameter law across all.
- **Conclusion.** $p_c(m) = e^{-m r^\star}$, universal in form.

## 11.5 `D2-E4_phase_diagram`
- **Axes.** $x$: $p$; $y$: rate $R$; a 2-D region colored by stable/unstable, with the measured $\gamma=1$
  boundary and the exact $R_c(p)$ curve overlaid.
- **Expected.** Measured boundary on the exact curve; vertical asymptote at $p=1/4$; floor at $R=h_R=\ln2$.
- **Observed.** Boundary MAE $0.0036$ nats; both marginals visible.
- **Conclusion.** The *entire* exact surface is validated.

## 11.6 `D2-E5_achievability`
- **Axes.** (a) $p$ vs escape rate, two curves (genuine 2-D cat observer, reduced 1-D walk). (b) time $t$ vs
  $\ln \mathbb E[\delta^2]$ for $p$ below and above $p_c$.
- **Expected.** (a) the two curves coincide. (b) saturates below $p_c$, grows above.
- **Observed.** (a) MAE $0.0001$. (b) saturates for $p < 0.174$, grows for $p > 0.174$.
- **Conclusion.** The UZQ reduction is faithful and it stabilizes iff $\gamma < 1$.

## 11.7 `D2-E6_henon_stress`
- **Axes.** (a) moment $m$ vs $r_{\mathrm{eff}}(m)$ (rising from Lyapunov to worst-case). (b) $p$ vs a.s. escape,
  with the Lyapunov and worst-case predictions marked.
- **Expected/Observed.** (a) $r_{\mathrm{eff}}$ climbs $0.725 \to 1.320$. (b) the observed a.s. threshold
  ($0.517$) sits at the Lyapunov prediction ($0.552$), not the worst-case ($0.185$).
- **Conclusion.** a.s. is average-governed; moments/uniform need worst-case (restoration) — why circle/cat are
  the clean tests.

## 11.8 `D2-E7_gilbert_elliott`
- **Axes.** $x$: mean erasure $\bar p$; $y$: escape rate; two curves (i.i.d. vs Gilbert–Elliott burst-10).
- **Expected/Observed.** i.i.d. escapes at $0.396$; GE at $0.035$ — GE far worse.
- **Conclusion.** Bursts are drastically more damaging; i.i.d. is optimistic.

## 11.9 `D2-M1_vector_two_rates`
- **Axes.** $p$ vs escape / moment multiplier, showing the a.s. transition at $p_R(r^\star_{\mathrm{vol}})$ and
  the moment crossings at $e^{-m r^\star_{\mathrm{top}}}$; the top-only allocation escaping early.
- **Expected/Observed.** a.s. at $0.329 \approx p_R(r^\star_{\mathrm{vol}}) = 0.364$ (not $0.545$); moments at
  $\{0.361, 0.135, 0.018\}$.
- **Conclusion.** Rate uses volume, reliability uses top — genuinely separated.

## 11.10 `D2-M2_map_universality`
- **Axes.** thresholds across five maps; tent and doubling (same $r^\star$) overlaid.
- **Expected/Observed.** Same $r^\star$ $\Rightarrow$ same $p_c$; collapse to $e^{-m r^\star}$ (log-error
  $0.0017$).
- **Conclusion.** Universality — only $r^\star$ matters.

## 11.11 `D2-M3_bursts_spectral`
- **Axes.** (a) burst length $L$ vs escape at fixed $\bar p = 0.1$. (b) measured moment growth vs $\ln\rho(M)$.
- **Expected/Observed.** (a) escape $0 \to 1$ as $L: 1 \to 50$. (b) match to MAE $0.0009$.
- **Conclusion.** The spectral-radius conjecture is numerically exact; bursts destabilize a "safe" average.

## 11.12 `D2-M4_nonnormal_metric`
- **Axes.** $p$ vs moment multiplier for non-normal systems, with the $\rho^{-m}$ and $\|A\|^{-m}$ predictions
  marked.
- **Expected/Observed.** Threshold at $\rho^{-m}$ (MAE $0.0087$), far from $\|A\|^{-m}$ ($35\times$ off).
- **Conclusion.** The optimal-metric (spectral-radius) rate is correct.

---

# SECTION 12 — REVIEWER QUESTIONS (an extensive, hostile FAQ with full answers)

**Q1. Isn't this just Sahai–Mitter anytime capacity re-labeled?**
No. Sahai–Mitter is *linear* — a constant gain $\lambda$, so $\log|\lambda|$ is well-defined. A *nonlinear*
system has a *state-dependent* Jacobian, so the per-burst expansion varies and a single constant is ill-defined.
D2 replaces it with the *uniform worst-case* rates $r^\star_{\mathrm{top}}$ (reliability) and $r^\star_{\mathrm{
vol}}$ (rate), and *adds* the restoration-entropy rate condition (R) that Sahai–Mitter does not have. Our (A) *is*
the anytime condition with $r^\star_{\mathrm{top}}$ in place of $\log|\lambda|$; that generalization is the point.

**Q2. Does acknowledgment (ACK) break the necessity?**
No. Even with causal ACK, future erasures are independent of the past (memoryless), so bursts are *unpredictable*
— you cannot pre-shrink the error before a burst you cannot foresee. And by Borel–Cantelli, arbitrarily long
bursts occur infinitely often, each inflating the moment. ACK changes the achievable *code* (enables
retransmission) but not the *necessity*, because capacity is feedback-invariant for memoryless channels
(Section 8.1.2, Step 6).

**Q3. Why restoration entropy $h_R$ and not topological/Lyapunov entropy $h_{\mathrm{top}}$?**
Because a controller must give a *uniform* guarantee: survive the *worst* burst at the *worst* state, from *any*
initial error. That is a *supremum* over the region (restoration entropy), not an *average* along typical orbits
(topological/Lyapunov). For uniform systems they coincide; for non-uniform ones $h_R > h_{\mathrm{top}}$, and
D2-E6 (Hénon) shows *typical/a.s.* behavior follows the average while *moment/uniform* guarantees need the
worst-case. Using the average would *under-provision* the channel.

**Q4. Your naive-Monte-Carlo would say the system is stable when it isn't. How do you trust your numbers?**
Exactly why we do *not* use naive MC. The $m$-th moment is dominated by rare long bursts that naive MC never
samples, so it under-estimates by $\sim 40\times$ (D2-E1). We use *importance sampling* with the analytically-
optimal tilt (essentially zero variance), validated against the closed-form $\gamma$. The naive-vs-IS-vs-exact
figure (D2-E1a) is the proof.

**Q5. The clean threshold $p_c = e^{-m r^\star}$ needs infinite rate. Isn't the finite-rate case different?**
Yes — and we say so. At finite rate the exact threshold is the *full* $\gamma < 1$ surface, whose two *marginals*
are $p_c = e^{-m r^\star}$ (as $R \to \infty$) and $R \ge h_R$ (as $p \to 0$). We validate the *entire* surface
(D2-E4, boundary MAE $0.0036$), and we explicitly *corrected* the bible's §2.7.1, which mistakenly put the
finite-rate transition at the infinite-rate marginal $1/4$ (D2-E2).

**Q6. You claim a two-rate structure but only test scalar/quasi-conformal maps where they coincide.**
That was a real gap (audit G5), now *fixed* by D2-M1: a vector system with $r^\star_{\mathrm{vol}} = 1.4 \ne
r^\star_{\mathrm{top}} = 1.0$, where the a.s./rate transition binds on $r^\star_{\mathrm{vol}}$ ($0.329$ vs
$0.364$) and the moment/reliability threshold binds on $r^\star_{\mathrm{top}}$ ($p_c(2) = 0.1352$ vs $0.1353$).
The two rates are genuinely separated.

**Q7. Is the "optimal metric" ($\rho$ vs $\|A\|$) a real distinction or an artifact of normal systems?**
Real, and now tested (audit G10): on *non-normal* matrices with $\|A\|/\rho$ up to $4.2\times$, the moment
threshold is $\rho(A)^{-m}$ (MAE $0.0087$), not $\|A\|^{-m}$ ($35\times$ off). The mechanism is Gelfand's
formula: long bursts self-average to $\rho(A)$. Scalar/normal surrogates cannot show this; non-normal systems
do.

**Q8. Real networks lose packets in bursts, not i.i.d. Does your result even apply?**
The clean i.i.d. result is a *necessary-but-optimistic screen* — we say this explicitly. For bursts we give the
Gilbert–Elliott generalization: stability $\iff \rho(M) < 1$ for the modulated transfer matrix, confirmed
numerically to MAE $0.0009$ (D2-M3), and we show a "safe" 10% average loss can escape with probability 1 at
burst length 50 (D2-E7). The *proof* for nonlinear maps under Markov channels is open — honestly future work.

**Q9. Does the theorem recover the classical linear results?**
Yes — the mandatory sanity check (Section 7.4). Scalar linear $f=\lambda x$: (R) at $p=0$ gives $R \ge
\ln|\lambda|$ (Tatikonda–Mitter/Nair–Evans); (A) at $m=2$ gives $p < 1/\lambda^2$ (Elia/Sinopoli); the anytime
form gives Sahai–Mitter. The *additive* form from an earlier draft *fails* this check, which is why the
*multiplicative* $\gamma$ form is the correct one.

**Q10. Is the UZQ construction actually implementable, or is it hand-waving?**
The encoder and decoder maintain the *same* uncertainty set from the *shared index history* (not the unknown
state), so there is no desynchronization — the "chicken-and-egg" of state-dependent grids is solved. D2-E5 shows
a genuine 2-D cat-map observer matching the reduced 1-D walk to MAE $10^{-4}$, and the moment saturating for
$\gamma < 1$. The only *modeled* piece is the anytime tree code's delivery; its reliability exponent $\ln(1/p)$
is the burst tail we validate directly.

**Q11. Why does higher moment $m$ need a more reliable channel?**
Because high moments weight *large* errors, which come from *rare long bursts*. The moment $\sum_b p^b e^{m
r^\star b}$ diverges once $p e^{m r^\star} \ge 1$; larger $m$ makes the expansion term grow faster, so a smaller
$p$ is needed — $p_c(m) = e^{-m r^\star}$ decreases in $m$. Bounding the mean tolerates more loss than bounding
the variance.

**Q12. What exactly is open / not claimed?**
(i) A first-principles proof of the Gilbert–Elliott spectral-radius threshold for nonlinear maps. (ii) An exact
threshold for non-uniform maps (their $h_R$ has no closed form). (iii) An explicit symbol-level no-ACK anytime
tree code (its *reliability condition* is validated; the *code engineering* is future work). All are documented
in `VALIDATION_AUDIT.md`.

---

# SECTION 13 — ORAL DEFENSE GUIDE (how to answer live)

**Golden rule.** Three beats: intuition, mechanism, evidence. Never lead with the formula.

**"State the result in one breath."**
"To keep an unstable nonlinear system bounded over a lossy link you need two independent things: enough *average*
rate to cover the uncertainty the system creates ($R(1-p) \ge h_R$), and enough *burst reliability* to survive
runs of dropped packets ($p\,e^{m r^\star} < 1$). We proved these are exactly necessary *and* sufficient — they
meet at a single number $\gamma < 1$, zero gap."

**"Explain $\gamma$."**
"(1) It's the per-step multiplier of the error's $m$-th moment. (2) On a delivered slot the error shrinks by
$e^{r^\star - R}$, on an erased slot it grows by $e^{r^\star}$; averaging over the coin flip gives $\gamma =
(1-p)e^{m(r^\star-R)} + p e^{m r^\star}$, so the moment is $\delta_0^m \gamma^t$ — bounded iff $\gamma < 1$. (3)
D2-E4 validates the whole $\gamma=1$ surface to 0.0036 nats."

**"Explain restoration entropy."**
"It's the minimum bit rate to *robustly* observe a nonlinear system — the *worst-case* rate at which it creates
uncertainty (a sup over the state space, sum of positive log-singular-values). Not the *average* (Lyapunov) —
because a burst can hit the worst state from any error. For uniform maps it equals the expansion rate; that's why
we test on circle/cat maps."

**"Explain condition (A) at the board."**
"Draw the error over a burst: it grows by $e^{r^\star}$ each erased step, so a length-$b$ burst gives $e^{r^\star
b}$. The moment weights it $e^{m r^\star b}$, and the burst has probability $p^b$. Sum over $b$: $\sum p^b e^{m
r^\star b}$ — a geometric series, diverges iff $p e^{m r^\star} \ge 1$. That's the reliability threshold. No
between-burst correction fixes a divergent series."

**"Why can't ACK save you?"**
"Bursts are unpredictable — memoryless channel. You can't pre-shrink the error before a burst you can't foresee,
and arbitrarily long bursts happen infinitely often. ACK helps the code, not the fundamental limit."

**"Why spectral radius, not operator norm, for a vector system?"**
"A single step can stretch by the operator norm, but a long burst stretches by $\|A^b\|^{1/b}$, which tends to
the spectral radius (Gelfand). The moment is driven by long bursts, so the threshold is $\rho^{-m}$. D2-M4:
matches $\rho^{-m}$ to 0.009, misses $\|A\|^{-m}$ by $35\times$."

**"Most convincing experiment?"**
"D2-M1. A vector system where the two rates *differ* ($r^\star_{\mathrm{vol}}=1.4$, $r^\star_{\mathrm{top}}=1.0$):
the rate condition binds on $1.4$, the reliability condition binds on $1.0$ — you literally see the two different
numbers govern the two different failures. No scalar system can show that."

**"What would falsify it?"**
"A controller keeping the $m$-th moment bounded at $p > e^{-m r^\star}$ (with large rate), or at $R(1-p) < h_R$.
We searched — circle, cat, five maps, vector, non-normal, bursty — every threshold matches."

---

# SECTION 14 — COMMON MISUNDERSTANDINGS (and why they are wrong)

1. **"Enough average bandwidth is enough."** No — that is *only* condition (R). You *also* need burst reliability
   (A). A high-throughput but bursty link can fail (D2-E7: GE escapes at 10% average loss).
2. **"The threshold is $p_c = e^{-m r^\star}$ at any rate."** No — that is the *infinite-rate marginal*. At finite
   rate the threshold is the full $\gamma < 1$ surface, which is *stricter* (D2-E2/E4). The bible's §2.7.1 made
   this exact mistake.
3. **"Restoration entropy = Lyapunov/topological entropy."** No — restoration is a *worst-case sup*, Lyapunov is
   an *average*. They coincide only for uniform maps. Using the average under-provisions (D2-E6).
4. **"For a vector system, one rate governs everything."** No — *rate* uses the *volume* rate (sum of expanding
   directions), *reliability* uses the *top* rate (fastest direction). Different numbers (D2-M1).
5. **"The reliability rate is the operator norm $\|A\|$."** No — it is the spectral radius $\rho(A)$ (long-burst
   self-averaging, Gelfand). For non-normal systems these differ a lot (D2-M4).
6. **"Higher moments and lower moments have the same threshold."** No — $p_c(m) = e^{-m r^\star}$ *decreases* with
   $m$; the variance needs a better channel than the mean.
7. **"i.i.d. and bursty loss are equivalent at equal average rate."** No — bursts are *far* more damaging
   (D2-E7/M3); the i.i.d. threshold is optimistic.
8. **"ACK/feedback raises the fundamental limit."** No — it helps the *code*, not the *necessity* (memoryless
   capacity is feedback-invariant; bursts are unpredictable).
9. **"Naive Monte Carlo can measure the moment threshold."** No — the moment is rare-event dominated; naive MC
   under-estimates by orders of magnitude. Importance sampling is required (D2-E1).
10. **"The whole thing is proven for real (bursty) networks."** No — the *closed* result is i.i.d. + uniform. The
    bursty (Gilbert–Elliott) and non-uniform cases are honestly flagged as conjectured/mechanism-only.

---

# SECTION 15 — MENTAL MODEL (the whole paper at five zoom levels)

## 15.1 The 5-minute explanation
You are controlling an unstable system (a balancing broomstick) over a thin, lossy internet link. Errors grow on
their own; you must keep correcting. Two ways the link can fail you: too little *average* bandwidth to keep up
with the uncertainty the system makes, or too many *consecutive* dropped packets (a burst) during which the
error grows beyond recovery. We proved the *exact* minimum link (rate *and* reliability) to stay safe: a single
number $\gamma$ must be below 1, and it splits into "enough average rate" and "enough burst reliability." The
punchline: classical networking optimizes average throughput only, so it is *structurally inadequate* for
controlling unstable systems.

## 15.2 The 15-minute explanation
Add the mechanism. The system creates uncertainty at rate $h_R$ (restoration entropy, a *worst-case*
expansion), and its error grows at rate $r^\star$ per step. Your effective average rate is $R(1-p)$ (loss $p$).
Rate condition: $R(1-p) \ge h_R$. Reliability condition: a length-$b$ burst inflates the error's $m$-th moment by
$e^{m r^\star b}$ with probability $p^b$; the sum diverges iff $p e^{m r^\star} \ge 1$. Both conditions are the
marginals of the exact per-step moment multiplier $\gamma = (1-p)e^{m(h_R-R)/d^+} + p e^{m r^\star}$; stable iff
$\gamma < 1$. Necessity (no controller beats it) + achievability (the zooming quantizer reaches it) = exact.

## 15.3 The 30-minute explanation
Add the proofs' skeletons (Section 8): Lemma C (bursts expand uniformly by the *sup* rate, not the average);
Lemma D (the divergent series $\sum p^b e^{m r^\star b}$ gives condition A, and ACK cannot help because bursts
are unpredictable); Lemma R (law of large numbers + volume counting gives condition R). Achievability: the UZQ
maintains a shared uncertainty set from the index history (no state-dependence mismatch), zooms in the optimal
metric (zero waste, floor exactly $h_R$), rides an anytime code through bursts; the drift is exactly $\gamma$
(Meyn–Tweedie gives bounded moment iff $\gamma < 1$). Then the surrogates (circle $r^\star=\ln k$, cat
$r^\star=\ln\lambda_u$) and the two-rate/optimal-metric refinements.

## 15.4 The 1-hour lecture
All of the above plus: the literature (Tatikonda–Mitter/Nair–Evans data rate $\to$ Sinopoli/Elia lossy linear
$\to$ Sahai–Mitter anytime $\to$ Matveev–Pogromsky restoration entropy $\to$ the D2 fusion); the measurement
methodology (importance sampling; why naive MC fails; the two order parameters); the seven core experiments (E1
exact/IS, E2 two conditions, E3 scaling law, E4 phase diagram, E5 achievability, E6 Hénon, E7 bursts); and the
four adversarial additions (M1 two rates, M2 universality, M3 spectral radius, M4 optimal metric).

## 15.5 The 3-hour lecture
Everything from Section 2's prerequisites up: dynamical systems, Jacobians/singular values, the two expansion
rates, spectral radius vs operator norm, chaos and restoration vs topological entropy, erasure channels (i.i.d.
and Gilbert–Elliott), moments and $m$-th-moment stability, the observer/zooming-quantizer recursion, anytime
reliability, importance sampling; then the full formulation with every assumption; the complete proofs of Lemmas
C, D, R, A-D2, B-D2, C-D2 with every inequality justified (Section 8); the surrogate derivations; all twelve
experiments with exact numbers; the figure walk-through; the full FAQ and defense guide. End with the honest
scope (i.i.d. + uniform closed; bursty + non-uniform open) and the open problems.

---

# SECTION 16 — LEARNING PATH (the exact order to study, with a dependency graph)

## 16.1 Dependency graph (textual)
```
Dynamical systems / maps (2.1)
        ↓
Stability / instability / expansion (2.2)
        ↓
Jacobians, singular values, two rates (2.3) ──→ Spectral radius vs operator norm (2.4)
        ↓                                             ↓
Chaos; restoration vs topological entropy (2.5)       │
        ↓                                             │
Erasure channels: i.i.d. + Gilbert–Elliott (2.6)      │
        ↓                                             │
Moments / m-th-moment stability (2.7)                 │
        ↓                                             ↓
Observer / zooming quantizer / recursion (2.8) ──→ Moment multiplier γ (2.9)
        ↓                                             ↓
Anytime reliability (2.10)                    Spectral radius of modulated matrix (2.12)
        ↓                                             │
Importance sampling (2.11)                            │
        ↓                                             │
   ┌──────────────────────────────────────────────────┘
   ↓
Problem formulation + surrogates (Section 4)
   ↓
Theorem D2★ necessity (7.1) ← proof: Lemma C (8.1.1) + Lemma D (8.1.2) + Lemma R (8.1.3)
   ↓
Theorem D2★★ achievability (7.2) ← proof: Lemmas A-D2/B-D2/C-D2 (8.2)
   ↓
Core experiments E1–E7 (9.1–9.7)
   ↓
Adversarial experiments M1–M4 (9.8–9.11)  ← need two-rates (2.3), spectral radius (2.4/2.12), IS (2.11)
   ↓
Validation + audit (Section 10)
```

## 16.2 Recommended study order (with "why this before that")
1. **2.1–2.3 (maps $\to$ Jacobians / two rates).** Everything is about how errors expand; internalize
   $r^\star_{\mathrm{top}}$ (max direction) vs $r^\star_{\mathrm{vol}}$ (sum of directions) before anything else.
2. **2.4–2.5 (spectral radius; restoration vs topological entropy).** The two subtle "which rate?" points that
   reviewers probe. Do not skip: they are the M4 and E6 experiments.
3. **2.6–2.7 (erasure channels; moments).** The channel and the stability notion. Note $p_c(m)$ *decreases* in
   $m$.
4. **2.8–2.9 (observer recursion; $\gamma$).** The recursion $\delta_{t+1}=G_t\delta_t$ *is* the whole system;
   $\gamma = \mathbb E[G^m]$ *is* the threshold. Make this feel like arithmetic.
5. **2.10–2.11 (anytime; importance sampling).** Anytime = the reliability condition's meaning; IS = how the
   moments are measured.
6. **Section 4 (formulation + surrogates).** Now the two conditions and the $\gamma$ surface will read plainly.
7. **Section 7 then 8 (theorems, then proofs).** Statement/intuition first (7), then step-by-step (8). Do Lemma
   D's divergent series and the $\gamma$ drift by hand.
8. **Section 9 (experiments), starting with 9.0 (measurement).** Understand *why IS* before any specific
   experiment; then E1 (the methodological one), then the rest.
9. **Sections 10, 12–14 (validation, FAQ, misunderstandings).** Cement by defending; especially the "two
   conditions," "restoration vs Lyapunov," and "spectral radius vs operator norm" distinctions.
10. **Section 15.** Re-tell at increasing depth until the 5-minute version is effortless.

## 16.3 Milestones (you understand D2 when you can…)
- derive $\gamma = (1-p)e^{m(r^\star-R)} + p e^{m r^\star}$ from one step of the error recursion, unaided;
- prove condition (A) at a board via the divergent series $\sum p^b e^{m r^\star b}$;
- explain *why* (R) and (A) are independent (rate = keeping up on average; reliability = surviving bursts);
- explain *why* restoration entropy (worst-case) not Lyapunov (average) is the rate;
- explain *why* the reliability rate is $\rho(A)$ not $\|A\|$ (Gelfand, long bursts);
- explain *why* naive Monte Carlo fails and importance sampling is required;
- state precisely what is closed (i.i.d. + uniform, exact $\gamma$) vs open (bursty spectral-radius proof,
  non-uniform $h_R$, symbol-level anytime code).

---

*End of MASTER_D2_HANDBOOK.md. Everything above is grounded in `D2_Research_Bible_v3.md`, `code/theory.py`,
`code/d2_sim.py`, `resultsD2.md`, and `VALIDATION_AUDIT.md`. Numbers such as $p_c(2)=0.2499$ vs $0.25$, $p_R =
0.1261$, $p_A = \{0.087,0.057,0.0215\}$, boundary MAE $0.0036$, faithfulness MAE $0.0001$, Hénon $\lambda=0.7255$
vs worst $1.3203$, i.i.d. $0.396$ vs GE $0.035$, vector $r^\star_{\mathrm{vol}}=1.4$/$r^\star_{\mathrm{top}}=1.0$
with a.s. $0.329$ and moments $\{0.361,0.135,0.018\}$, spectral MAE $0.0009$, and non-normal $\rho^{-m}$ MAE
$0.0087$ vs $\|A\|^{-m}$ MAE $0.3011$ are quoted directly from `resultsD2.md`.*
