# D2 Literature Freeze — Restoration–Anytime Limit over Lossy Channels

Target venue: IEEE Transactions on Automatic Control. Goal: an exhaustive prior-art survey so that no reviewer
can reasonably claim an important omission. For each work we record what it solved, its assumptions, its
limitations, and how the present paper differs. Every entry corresponds to a real, verifiable publication in
`refs.bib`. All rates are in nats per channel use.

The problem settled in this paper is the exact m-th-moment threshold for controlled set-invariance of a general
C1 expansive map over an i.i.d. erasure channel. The result is the single surface gamma = (1-p) e^{m(h_R-R)/d+}
+ p e^{m r*_top} = 1, whose two marginals are a rate condition R(1-p) >= h_R governed by the restoration entropy
and a reliability condition p e^{m r*_top} < 1 governed by the top expansion rate. The literature is organized
into six strands that jointly bound this contribution.

## Strand 1 — Data-rate theorems for deterministic channels
- Wong-Brockett 1997/1999; Nair-Evans 2000; Brockett-Liberzon 2000; Delchamps 1990; Fu-Xie 2005. Solved: the
  minimum bit rate and the quantizer designs for stabilizing a linear plant over a noiseless finite-rate link.
  Assumptions: no packet loss, linear plant. Limitation: deterministic channel. Difference: this paper adds
  random erasure and the moment refinement.
- Tatikonda-Mitter 2004. Solved: LTI mean-square stabilization over a noiseless rate-R channel holds iff R
  exceeds the sum of the unstable log-eigenvalues. Recovered here as the p=0 marginal of the rate condition.
- Nair-Evans 2004; Nair-Evans-Mareels-Moran 2004. Solved: the minimal rate for set-invariance of a nonlinear map
  equals the topological feedback entropy. Limitation: a packet drop inflates the initial estimation error
  without a uniform margin, so topological feedback entropy is not robust to erasure. Difference: this paper uses
  the restoration entropy, a uniform supremum, and it reuses the volume-counting technique with a supremum over
  the region in place of the orbit average.
- Nair-Fagnani-Zampieri-Evans 2007; Matveev-Savkin 2009; Yuksel-Basar 2013. Surveys and monographs that frame
  the data-rate program and the networked-control setting the present paper extends.

## Strand 2 — Estimation and control under packet loss (linear)
- Sinopoli et al. 2004. Solved: a critical arrival probability for bounded expected error covariance in Kalman
  filtering with intermittent observations; for a scalar unstable mode the second-moment erasure threshold is p
  below the inverse square of the gain. Recovered here as the scalar m=2 case.
- Elia 2005; Gupta-Hassibi-Murray 2007. Solved: scalar and vector mean-square stabilization over erasure and
  fading links, with the most unstable mode dominating the second-moment threshold. Recovered as the reliability
  condition at m=2 with the spectral radius.
- You-Xie 2010; Minero-Franceschetti-Dey-Nair 2009; Coviello-Minero-Franceschetti 2013. Solved: minimum data
  rate for mean-square stabilization over lossy and Markov feedback channels, expressed as a spectral-radius
  condition on a modulated matrix combined with a rate condition. The i.i.d. case is the rank-one specialization
  used here, and the nonlinear analog is stated as the Gilbert-Elliott conjecture.
- Schenato et al. 2007; Hespanha-Naghshtabrizi-Xu 2007. Surveys of control and estimation over lossy networks
  that position the erasure-channel stability question.

## Strand 3 — Anytime capacity and reliability
- Sahai-Mitter 2006. Solved: stabilizing an unstable linear plant over a noisy link requires anytime capacity at
  a rate above the log-gain and reliability above m times the log-gain for m-th-moment stability. Limitation: the
  exponential tail bound assumes a constant gain, so the linear anytime exponent is ill-defined for
  state-dependent Jacobians. Difference: this paper replaces the constant log-gain by the uniform top rate for
  reliability and the volume rate for bandwidth, and shows the two are governed separately.
- Tatikonda-Sahai-Mitter 2004; Simsek-Jain-Varaiya 2004; Sukhavasi-Hassibi 2016; Como-Fagnani-Zampieri 2010;
  Martins-Dahleh-Elia 2006; Freudenberg-Middleton-Solo 2010. Solved: constructions and limits for anytime and
  real-valued reliable transmission over noisy channels, and stabilization in the presence of a direct link.
  Use here: the anytime tree code is the transport layer of the achievability, and its reliability exponent is
  exactly the erasure-burst tail that drives the moment divergence.

## Strand 4 — Entropy notions for nonlinear control
- Colonius-Kawan 2009; Colonius 2012; Kawan 2013; Kawan 2018; Savkin 2006. Solved: invariance entropy and its
  relatives as the minimal rate for set-invariance and exponential stabilization of nonlinear systems.
  Difference: these are deterministic-channel notions; the present restoration-entropy rate is the robust
  supremum needed under erasure, and it is paired with the reliability condition they do not have.
- Matveev-Pogromsky 2016; Matveev-Pogromsky 2019. Solved: constructive data-rate limits for observing nonlinear
  systems over finite-capacity channels, and tight restoration-entropy estimates through the singular values of
  the Jacobian in an optimal Riemannian metric, with equality under uniform quasi-conformality. Use here: the
  restoration entropy defines the rate condition and the optimal metric drives the zooming quantizer of the
  achievability.
- Diwadkar-Vaidya 2013; Nair 2013. Solved: fundamental limits for nonlinear observation over an erasure channel,
  and a nonstochastic information theory for state estimation. Difference: this paper gives the exact m-th-moment
  threshold surface and a matching zooming-quantizer achievability without quasi-conformality.

## Strand 5 — Nonlinear and predictive control under loss
- Liberzon-Hespanha 2005; Baillieul 2004; Liberzon-Nair 2007. Solved: data-rate conditions for nonlinear
  quantized stabilization on deterministic channels. Difference: no random erasure with a moment guarantee.
- Quevedo-Nesic 2012. Solved: input-to-state stability of packetized predictive control of nonlinear plants
  under Markov drops. Difference: this gives sufficient input-to-state conditions rather than a tight
  rate-and-reliability necessity in terms of an intrinsic entropy, which the present paper supplies.

## Strand 6 — Mathematical foundations
- Katok-Hasselblatt 1995; Walters 1982; Pesin 1977; Oseledets 1968. Provide the singular-value and volume-growth
  machinery and the distinction between orbit-average (Lyapunov and topological) and worst-case (restoration)
  expansion that motivates the choice of rate.
- Furstenberg-Kesten 1960; Costa-Fragoso-Marques 2005; Fang-Loparo 2002. Products of random matrices and Markov
  jump linear systems, the tools behind the Gilbert-Elliott conjecture.
- Gilbert 1960; Elliott 1963. The burst-noise channel model used in the correlated-loss experiments.
- Meyn-Tweedie 2009. The geometric-drift criterion that closes the achievability sufficiency.
- Shannon 1948; Cover-Thomas 2006. The channel-capacity and feedback-invariance facts used in the necessity
  argument.

## Novelty statement (the row no prior work occupies)
No prior work gives the exact m-th-moment threshold for a general C1 expansive nonlinear map over a random
erasure channel, together with a matching achievability that reaches it without a quasi-conformality assumption.
The data-rate and invariance-entropy lines solve the deterministic-channel case, the linear packet-loss line
solves the linear stochastic case, and the anytime line solves the linear noisy-channel case. The present paper
occupies the intersection, separates the volume rate for bandwidth from the top rate for reliability, and
confirms both with rare-event importance sampling on uniformly hyperbolic surrogates and on non-normal and
non-uniform stress systems.

## Reference count
The accompanying `refs.bib` contains 55 entries spanning all six strands, above the 50-reference floor, with
priority on IEEE Transactions on Automatic Control, Automatica, SIAM Journal on Control and Optimization, and the
directly competing data-rate, packet-loss, anytime, and restoration-entropy lines.
