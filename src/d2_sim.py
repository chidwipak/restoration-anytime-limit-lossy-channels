"""
d2_sim.py — Simulation engine for Direction 2 (Restoration-Anytime limit over lossy channels).

The observer/zooming-quantizer tracks the actual dynamical map over an erasure channel.
For uniformly hyperbolic surrogates (circle, cat) the uncertainty half-width delta obeys
an exact multiplicative recursion:
    delta_{t+1} = G_t * delta_t,   G_t = e^{r*-R} (delivered, prob 1-p) or e^{r*} (erased, prob p).

Two distinct phase transitions (bible 2.3.5 — two independent conditions):
  * Condition (R): a.s./drift boundedness.  E[log G] < 0  <=>  R(1-p) > r*  <=>  p < p_R = 1 - r*/R.
    Governed by TYPICAL paths -> plain Monte Carlo measures it well (escape-rate order parameter).
  * Condition (A): m-th moment boundedness.  gamma(m) = (1-p)e^{m(r*-R)} + p e^{m r*} < 1.
    Governed by RARE erasure-heavy paths (heavy upper tail) -> naive MC UNDERESTIMATES the moment;
    importance sampling (exponential tilt of the erasure process) is required.

METHODOLOGICAL NOTE: because E[delta^m] = delta_0^m * gamma(m)^t factorizes exactly for the
i.i.d. multiplicative walk, gamma(m) is analytically exact (= E[G^m]); we nonetheless *measure* it
by simulation to (a) demonstrate plain MC fails on the heavy tail, (b) show IS recovers the truth,
(c) provide a validated estimator for the non-uniform / correlated cases where no closed form exists.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from scipy.special import logsumexp


# =====================================================================================
# Channels
# =====================================================================================
def iid_erased(p: float, shape, rng: np.random.Generator):
    """Boolean array: True = ERASED (prob p)."""
    return rng.random(shape) < p


class GilbertElliott:
    """2-state Gilbert-Elliott burst-erasure channel (bible 2.5.1)."""

    def __init__(self, p_gb: float, p_bg: float, eps_G: float = 0.0, eps_B: float = 1.0):
        self.p_gb, self.p_bg, self.eps_G, self.eps_B = p_gb, p_bg, eps_G, eps_B

    @property
    def pi_B(self):
        return self.p_gb / (self.p_gb + self.p_bg)

    @property
    def mean_erasure(self):
        return (1 - self.pi_B) * self.eps_G + self.pi_B * self.eps_B

    @property
    def mean_burst_length(self):
        return 1.0 / self.p_bg

    def simulate_erased(self, T: int, n_trials: int, rng: np.random.Generator):
        """Boolean (T, n_trials): True = erased."""
        state = (rng.random(n_trials) < self.pi_B).astype(np.int8)
        erased = np.empty((T, n_trials), dtype=bool)
        for t in range(T):
            eps = np.where(state == 1, self.eps_B, self.eps_G)
            erased[t] = rng.random(n_trials) < eps
            u = rng.random(n_trials)
            to_bad = (state == 0) & (u < self.p_gb)
            to_good = (state == 1) & (u < self.p_bg)
            state[to_bad] = 1
            state[to_good] = 0
        return erased


# =====================================================================================
# Exact analytic threshold
# =====================================================================================
def gamma_exact(p: float, R: float, m: float, r_star: float) -> float:
    """gamma(m) = (1-p) e^{m(r*-R)} + p e^{m r*}  (bible 2.4.1, d+=1, h_R=r*)."""
    return (1 - p) * np.exp(m * (r_star - R)) + p * np.exp(m * r_star)


def optimal_tilt(p: float, R: float, m: float, r_star: float) -> float:
    """Zero-variance IS erasure prob q* = p e^{m r*} / gamma(m)."""
    num = p * np.exp(m * r_star)
    return float(num / gamma_exact(p, R, m, r_star))


# =====================================================================================
# gamma measurement: naive MC (fails on tail) and importance sampling (correct)
# =====================================================================================
@dataclass
class GammaMeasurement:
    p: float
    R: float
    m: float
    r_star: float
    gamma_exact: float
    gamma_mc: float           # naive Monte Carlo (biased low on heavy tail)
    gamma_is: float           # importance sampling estimate
    gamma_is_lo: float
    gamma_is_hi: float
    n_trials: int
    T_slope: int


def measure_gamma(p: float, R: float, m: float, r_star: float, rng: np.random.Generator,
                  n_trials: int = 20000, T_slope: int = 60, n_batches: int = 20,
                  q_tilt: float | None = None) -> GammaMeasurement:
    """Measure the per-step m-th-moment multiplier gamma(m) two ways (naive MC and IS)."""
    g_exact = gamma_exact(p, R, m, r_star)
    a = r_star - R      # log delivered multiplier
    L = r_star          # log erased multiplier
    tt = np.arange(T_slope + 1, dtype=float)
    A = np.column_stack([np.ones_like(tt), tt])

    # ---- naive MC ----
    y = np.zeros(n_trials)
    logE = np.empty(T_slope + 1)
    logE[0] = logsumexp(m * y) - np.log(n_trials)
    for t in range(T_slope):
        er = iid_erased(p, n_trials, rng)
        y = y + np.where(er, L, a)
        logE[t + 1] = logsumexp(m * y) - np.log(n_trials)
    slope_mc = np.linalg.lstsq(A, logE, rcond=None)[0][1]
    gamma_mc = float(np.exp(slope_mc))

    # ---- importance sampling (batched for CI) ----
    q = q_tilt if q_tilt is not None else optimal_tilt(p, R, m, r_star)
    q = min(max(q, 1e-6), 1 - 1e-6)
    lr_er = np.log(p / q)            # log LR contribution of an erased step
    lr_de = np.log((1 - p) / (1 - q))
    per_batch = max(200, n_trials // n_batches)
    gammas = []
    for _b in range(n_batches):
        y = np.zeros(per_batch)
        logw = np.zeros(per_batch)   # log importance weight
        logE_is = np.empty(T_slope + 1)
        logE_is[0] = logsumexp(m * y + logw) - np.log(per_batch)
        for t in range(T_slope):
            er = iid_erased(q, per_batch, rng)   # sample under tilted q
            y = y + np.where(er, L, a)
            logw = logw + np.where(er, lr_er, lr_de)
            logE_is[t + 1] = logsumexp(m * y + logw) - np.log(per_batch)
        s = np.linalg.lstsq(A, logE_is, rcond=None)[0][1]
        gammas.append(np.exp(s))
    gammas = np.array(gammas)
    gamma_is = float(gammas.mean())
    lo, hi = np.quantile(gammas, [0.025, 0.975])

    return GammaMeasurement(p, R, m, r_star, float(g_exact), gamma_mc,
                            gamma_is, float(lo), float(hi), n_trials, T_slope)


# =====================================================================================
# Physical observer (condition R / escape) on the actual maps
# =====================================================================================
@dataclass
class ObserverResult:
    p: float
    R: float
    m: float
    r_star: float
    p_R: float               # drift threshold 1 - r*/R
    escape_rate: float
    escape_lo: float
    escape_hi: float
    mean_log_delta_rate: float   # analytic per-step drift E[log G]
    log_moment_final: float
    n_trials: int
    T: int


def run_physical_observer(p: float, R: float, m: float, r_star: float, T: int, n_trials: int,
                          rng: np.random.Generator, delta_init: float = 1e-6,
                          delta_min: float = 1e-12, escape_thresh: float = 0.5) -> ObserverResult:
    """Physical uncertainty process with reflecting floor and 'lost-track' ceiling.
    Escape (loses track) occurs when delta reaches the domain half-diameter escape_thresh.
    Order parameter tracks the a.s./drift threshold p_R = 1 - r*/R (condition R).
    Works for circle (r*=ln k) and cat (r*=ln lambda_u) via the unstable-direction reduction."""
    a = np.exp(r_star - R)
    Lexp = np.exp(r_star)
    delta = np.full(n_trials, delta_init)
    escaped = np.zeros(n_trials, dtype=bool)
    for t in range(T):
        er = iid_erased(p, n_trials, rng)
        delta = np.where(er, delta * Lexp, delta * a)   # erased: expand; delivered: expand*zoom
        delta = np.maximum(delta, delta_min)
        escaped |= delta >= escape_thresh
        delta = np.minimum(delta, escape_thresh)
    drift = (1 - p) * (r_star - R) + p * r_star
    log_moment_final = float(logsumexp(m * np.log(delta)) - np.log(n_trials))
    from stats_utils import wilson_ci
    _, lo, hi = wilson_ci(int(escaped.sum()), n_trials)
    return ObserverResult(p, R, m, r_star, 1 - r_star / R,
                          float(escaped.mean()), lo, hi, drift,
                          log_moment_final, n_trials, T)


# =====================================================================================
# Genuine VECTOR-system observer (r*_vol != r*_top) — tests bible COR-3 two-rate structure
# =====================================================================================
def run_vector_observer(p: float, R: float, m: float, eigvals, T: int, n_trials: int,
                        rng: np.random.Generator, delta_init: float = 1e-6,
                        delta_min: float = 1e-12, escape_thresh: float = 0.5,
                        alloc: str = "proportional"):
    """Genuine observer for a diagonal linear system x_{t+1}=diag(eigvals) x on a compact region.
    Tracks per-eigendirection uncertainty; the SHARED erasure channel expands ALL directions on an
    erased slot; a delivered slot splits total rate R across directions.

    Two intrinsic rates (bible 2.0, COR-3):
      r*_vol = sum_i log^+ |lambda_i|  (rate/volume, condition R) ; r*_top = log^+ max|lambda_i| (reliability).
    'proportional' allocation R_i = R * ln|lambda_i| / r*_vol makes every unstable direction hit its a.s.
    boundary at the SAME R(1-p)=r*_vol; the m-th moment of the norm is governed by the TOP direction.

    Returns dict with a.s. escape rate and per-direction final log-moments.
    """
    lam = np.asarray([abs(float(l)) for l in eigvals], dtype=float)
    logl = np.log(lam)
    unstable = logl > 0
    r_vol = float(np.sum(np.maximum(logl, 0.0)))
    r_top = float(np.max(np.maximum(logl, 0.0)))
    d_plus = int(np.sum(unstable))
    # rate allocation across unstable directions
    R_i = np.zeros_like(lam)
    if alloc == "proportional" and r_vol > 0:
        R_i[unstable] = R * (logl[unstable] / r_vol)
    elif alloc == "uniform":
        R_i[unstable] = R / max(d_plus, 1)
    else:  # top-only (deliberately wrong: starves the sub-dominant modes)
        top = int(np.argmax(logl)); R_i[top] = R
    a_i = np.exp(logl - R_i)     # delivered per-dir multiplier
    L_i = np.exp(logl)           # erased per-dir multiplier

    d = int(len(lam))
    delta = np.full((n_trials, d), delta_init)
    escaped = np.zeros(n_trials, dtype=bool)
    for t in range(T):
        er = iid_erased(p, n_trials, rng)                 # shared channel across directions
        mult = np.where(er[:, None], L_i[None, :], a_i[None, :])
        delta = delta * mult
        delta = np.maximum(delta, delta_min)
        escaped |= (delta >= escape_thresh).any(axis=1)   # box escapes if ANY direction blows up
        delta = np.minimum(delta, escape_thresh)
    top_dir = int(np.argmax(logl))
    from stats_utils import wilson_ci
    _, lo, hi = wilson_ci(int(escaped.sum()), n_trials)
    log_moment_top = float(logsumexp(m * np.log(delta[:, top_dir])) - np.log(n_trials))
    return dict(p=p, R=R, m=m, r_vol=r_vol, r_top=r_top, d_plus=d_plus,
                p_R_vol=1 - r_vol / R, p_R_top=1 - r_top / R,
                escape_rate=float(escaped.mean()), escape_lo=lo, escape_hi=hi,
                log_moment_top=log_moment_top, R_alloc=R_i.tolist(), T=T, n_trials=n_trials)


def measure_matrix_moment_growth(A, p: float, R: float, m: float, rng: np.random.Generator,
                                 n_trials: int = 8000, T_slope: int = 50, n_batches: int = 8,
                                 q_tilt: float | None = None):
    """Moment growth rate of a NON-NORMAL random matrix product (Furstenberg/Kesten setting).

    Uncertainty vector evolves delta_{t+1} = G_t delta_t with G_t = A (erased, prob p) or e^{-R} A
    (delivered, prob 1-p). Because A is non-normal, per-burst growth is ||A^b|| (spectral norm of the
    POWER), and ||A^b||^{1/b} -> rho(A) (Gelfand): long bursts — which dominate the m-th moment's heavy
    tail — grow at the SPECTRAL RADIUS, not the operator norm. We estimate the moment growth rate
    Lambda(m) = lim (1/t) ln E||delta_t||^m by importance sampling on the erasure sequence while tracking
    the ACTUAL vector product. Threshold Lambda(m)=0 locates p_c(m). Returns gamma_m = e^{Lambda(m)}.

    Predictions: at large R, p_c(m) = rho(A)^{-m} (optimal-metric / spectral radius, bible 2.3.7),
    NOT ||A||^{-m} (Euclidean operator norm — too pessimistic).
    """
    A = np.asarray(A, dtype=float)
    rho = float(max(abs(np.linalg.eigvals(A))))
    opnorm = float(np.linalg.svd(A, compute_uv=False)[0])
    contract = np.exp(-R)
    if q_tilt is None:
        # tilt toward the spectral-radius-dominant regime
        gden = (1 - p) * np.exp(m * (np.log(rho) - R)) + p * np.exp(m * np.log(rho))
        q_tilt = p * np.exp(m * np.log(rho)) / gden
    q = min(max(q_tilt, 1e-6), 1 - 1e-6)
    lr_er = np.log(p / q); lr_de = np.log((1 - p) / (1 - q))
    tt = np.arange(T_slope + 1, dtype=float)
    Amat = np.column_stack([np.ones_like(tt), tt])
    per = max(200, n_trials // n_batches)
    gammas = []
    for _b in range(n_batches):
        v = rng.standard_normal((per, A.shape[0]))
        v /= np.linalg.norm(v, axis=1, keepdims=True)
        lognorm = np.zeros(per)               # accumulated log||delta|| (start unit norm)
        logw = np.zeros(per)
        logE = np.empty(T_slope + 1)
        logE[0] = logsumexp(m * lognorm + logw) - np.log(per)
        for t in range(T_slope):
            er = iid_erased(q, per, rng)
            v = v @ A.T                        # apply A to every vector (row-vec convention)
            fac = np.where(er, 1.0, contract)  # delivered multiplies by e^{-R}
            v = v * fac[:, None]
            nrm = np.linalg.norm(v, axis=1)
            lognorm = lognorm + np.log(nrm)
            v = v / nrm[:, None]               # renormalize (track log-norm separately) for stability
            logw = logw + np.where(er, lr_er, lr_de)
            logE[t + 1] = logsumexp(m * lognorm + logw) - np.log(per)
        slope = np.linalg.lstsq(Amat, logE, rcond=None)[0][1]
        gammas.append(np.exp(slope))
    gammas = np.array(gammas)
    return dict(p=p, R=R, m=m, rho=rho, op_norm=opnorm,
                gamma_m=float(gammas.mean()), gamma_lo=float(np.quantile(gammas, 0.025)),
                gamma_hi=float(np.quantile(gammas, 0.975)),
                pc_spectral=float(rho**(-m)), pc_opnorm=float(opnorm**(-m)))


# =====================================================================================
# Genuine 2-D cat-map observer (faithfulness check)
# =====================================================================================
CAT_A = np.array([[1.0, 1.0], [1.0, 2.0]])

def cat_eigsystem():
    w, V = np.linalg.eigh(CAT_A)
    order = np.argsort(w)[::-1]
    return float(w[order[0]]), float(w[order[1]]), V[:, order[0]], V[:, order[1]]


def run_cat_faithful(p: float, R: float, m: float, T: int, n_trials: int,
                     rng: np.random.Generator, delta_init: float = 1e-6,
                     delta_min: float = 1e-12, escape_thresh: float = 0.5) -> ObserverResult:
    """Genuine 2-D cat map: iterate true state on the torus; track uncertainty in the eigenbasis.
    Rate zooms the unstable direction only (d+=1); stable direction self-contracts.
    Confirms reduction to the r*=ln(lambda_u) 1-D walk (faithfulness of the surrogate)."""
    lam_u, lam_s, vu, vs = cat_eigsystem()
    r_star = float(np.log(lam_u))
    a = np.exp(-R)
    X = rng.random((n_trials, 2))
    du = np.full(n_trials, delta_init)
    ds = np.full(n_trials, delta_init)
    escaped = np.zeros(n_trials, dtype=bool)
    for t in range(T):
        X = (X @ CAT_A.T) % 1.0
        du = du * lam_u
        ds = ds * lam_s
        er = iid_erased(p, n_trials, rng)
        du = np.where(er, du, du * a)
        du = np.maximum(du, delta_min)
        escaped |= du >= escape_thresh
        du = np.minimum(du, escape_thresh)
    log_moment_final = float(logsumexp(m * np.log(du)) - np.log(n_trials))
    from stats_utils import wilson_ci
    _, lo, hi = wilson_ci(int(escaped.sum()), n_trials)
    drift = (1 - p) * (r_star - R) + p * r_star
    return ObserverResult(p, R, m, r_star, 1 - r_star / R,
                          float(escaped.mean()), lo, hi, drift, log_moment_final, n_trials, T)


# =====================================================================================
# Non-linear stress-test observer (Henon) — state-dependent Jacobian
# =====================================================================================
def henon_step(X, a=1.4, b=0.3):
    x, y = X[:, 0], X[:, 1]
    return np.column_stack([1 - a * x**2 + y, b * x])


def henon_top_sv(X, a=1.4, b=0.3):
    """Top singular value of Henon Jacobian J=[[-2 a x,1],[b,0]] for each row of X (vectorized).
    JJ^T has trace tr=J11^2+1+b^2 and det = det(J)^2 = b^2; smax^2=(tr+sqrt(tr^2-4 b^2))/2."""
    x = X[:, 0]
    J11 = -2 * a * x
    tr = J11**2 + 1 + b**2
    disc = np.sqrt(np.maximum(tr**2 - 4 * b**2, 0.0))
    return np.sqrt((tr + disc) / 2)


def run_henon_stress(p: float, R: float, m: float, T: int, n_trials: int,
                     rng: np.random.Generator, a: float = 1.4, b: float = 0.3,
                     delta_init: float = 1e-6, delta_min: float = 1e-12,
                     escape_thresh: float = 1.0):
    """Non-linear Henon stress test: STATE-DEPENDENT expansion sigma_1(J(x_t)). Effective
    threshold uses trajectory expansion (Lyapunov / restoration), NOT constant r* -> deviates
    from the naive constant-r* prediction (h_R != r*_top)."""
    X = rng.uniform(-0.1, 0.1, (n_trials, 2))
    for _ in range(300):
        X = henon_step(X, a, b)
    a_c = np.exp(-R)
    delta = np.full(n_trials, delta_init)
    escaped = np.zeros(n_trials, dtype=bool)
    log_exp = np.zeros(n_trials)
    for t in range(T):
        sv = np.maximum(henon_top_sv(X, a, b), 1e-12)
        log_exp += np.log(np.maximum(sv, 1.0))
        X = henon_step(X, a, b)
        delta = delta * sv
        er = iid_erased(p, n_trials, rng)
        delta = np.where(er, delta, delta * a_c)
        delta = np.maximum(delta, delta_min)
        escaped |= delta >= escape_thresh
        delta = np.minimum(delta, escape_thresh)
    from stats_utils import wilson_ci
    _, lo, hi = wilson_ci(int(escaped.sum()), n_trials)
    return dict(p=p, R=R, m=m, mean_top_lyap=float(log_exp.mean() / T),
                escape_rate=float(escaped.mean()), escape_lo=lo, escape_hi=hi,
                T=T, n_trials=n_trials)


def henon_expansion_samples(n: int, rng: np.random.Generator, a: float = 1.4, b: float = 0.3,
                            burn: int = 500):
    """Sample the top singular value sigma_1(J(x)) over the Henon attractor (invariant measure)."""
    X = rng.uniform(-0.1, 0.1, (n, 2))
    for _ in range(burn):
        X = henon_step(X, a, b)
    return henon_top_sv(X, a, b)


def r_eff_of_m(sv_samples, m: float) -> float:
    """Annealed effective expansion rate r_eff(m) = (1/m) ln E[sigma_1^m].
    m->0: Lyapunov exponent E[ln sigma_1]; m->inf: ln max sigma_1 (worst-case/restoration)."""
    ls = np.log(np.maximum(sv_samples, 1e-12))
    if m < 1e-6:
        return float(np.mean(ls))
    return float((logsumexp(m * ls) - np.log(len(ls))) / m)


def measure_henon_gamma(p: float, R: float, m: float, rng: np.random.Generator,
                        n_trials: int = 8000, T_slope: int = 40, n_batches: int = 8,
                        a: float = 1.4, b: float = 0.3, q_tilt: float = 0.5):
    """Measure the actual per-step m-th-moment multiplier gamma_H(m) of the Henon observer via
    importance sampling on the erasure process (the chaotic trajectory is simulated exactly).
    Returns (gamma_measured, ci_lo, ci_hi)."""
    a_c = R  # log contraction magnitude when delivered
    tt = np.arange(T_slope + 1, dtype=float)
    A = np.column_stack([np.ones_like(tt), tt])
    q = min(max(q_tilt, 1e-6), 1 - 1e-6)
    lr_er = np.log(p / q); lr_de = np.log((1 - p) / (1 - q))
    per = max(200, n_trials // n_batches)
    gammas = []
    for _bidx in range(n_batches):
        X = rng.uniform(-0.1, 0.1, (per, 2))
        for _ in range(300):
            X = henon_step(X, a, b)
        y = np.zeros(per); logw = np.zeros(per)
        logE = np.empty(T_slope + 1)
        logE[0] = logsumexp(m * y + logw) - np.log(per)
        for t in range(T_slope):
            sv = np.maximum(henon_top_sv(X, a, b), 1e-12)
            X = henon_step(X, a, b)
            er = iid_erased(q, per, rng)
            y = y + np.log(sv) - np.where(er, 0.0, a_c)
            logw = logw + np.where(er, lr_er, lr_de)
            logE[t + 1] = logsumexp(m * y + logw) - np.log(per)
        s = np.linalg.lstsq(A, logE, rcond=None)[0][1]
        gammas.append(np.exp(s))
    gammas = np.array(gammas)
    return float(gammas.mean()), float(np.quantile(gammas, 0.025)), float(np.quantile(gammas, 0.975))
