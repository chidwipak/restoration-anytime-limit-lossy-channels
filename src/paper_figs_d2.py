"""
paper_figs_d2.py — Regenerate the D2 paper figures (title-less, print-tuned)
from the saved experiment data in results/d2/data/. Output: Publication/D2/Figures/.

Only the five experimental figures selected for the manuscript are produced here;
the system-model figure is drawn in TikZ inside the LaTeX source.
All quantities in nats. Numbers are read from the frozen .npz/.json data.
"""
from __future__ import annotations

import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

DATA = "results/d2/data"
OUT = "Publication/D2/Figures"
os.makedirs(OUT, exist_ok=True)

W = {
    "blue": "#0072B2", "orange": "#E69F00", "green": "#009E73",
    "red": "#D55E00", "purple": "#CC79A7", "sky": "#56B4E9", "grey": "#7F7F7F",
}


def set_style():
    plt.rcParams.update({
        "figure.dpi": 140, "savefig.dpi": 600, "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02, "font.size": 9, "font.family": "serif",
        "mathtext.fontset": "cm", "axes.titlesize": 9, "axes.labelsize": 9,
        "axes.linewidth": 0.8, "axes.grid": True, "grid.alpha": 0.30,
        "grid.linewidth": 0.5, "legend.fontsize": 7.4, "legend.frameon": True,
        "legend.framealpha": 0.92, "legend.edgecolor": "0.8", "legend.handlelength": 1.8,
        "lines.linewidth": 1.7, "lines.markersize": 4.2, "xtick.labelsize": 8,
        "ytick.labelsize": 8, "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    })


def save(fig, name):
    for fmt in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, f"{name}.{fmt}"), format=fmt)
    plt.close(fig)
    print("wrote", name)


def npz(e):
    return np.load(os.path.join(DATA, f"{e}.npz"), allow_pickle=True)


def js(e):
    with open(os.path.join(DATA, f"{e}.json")) as f:
        return json.load(f)


# ---------------------------------------------------------- E4 phase diagram
def fig_e4():
    d = npz("D2-E4")
    j = js("D2-E4")
    ps, Rs = d["ps"], d["Rs"]
    G, Gex = d["gamma_grid"], d["gamma_exact_grid"]
    ln2 = np.log(2.0)
    fig, ax = plt.subplots(figsize=(3.5, 2.75))
    # stable region gamma < 1
    ax.contourf(ps, Rs, G, levels=[0.0, 1.0], colors=[W["sky"]], alpha=0.30)
    cm = ax.contour(ps, Rs, G, levels=[1.0], colors=[W["blue"]], linewidths=1.8)
    ce = ax.contour(ps, Rs, Gex, levels=[1.0], colors=[W["green"]],
                    linewidths=1.3, linestyles="--")
    ax.axvline(0.25, color=W["red"], ls=":", lw=1.2)
    ax.axhline(ln2, color=W["grey"], ls=":", lw=1.2)
    ax.text(0.252, Rs.min() + 0.15, r"$p_c(2)=\frac{1}{4}$", color=W["red"],
            fontsize=7.4, rotation=90, va="bottom")
    ax.text(0.30, ln2 + 0.05, r"$h_R=\ln 2$", color="black", fontsize=7.4)
    ax.text(0.06, Rs.min() + 0.3, "stable\n" r"$(\gamma<1)$", fontsize=8, color=W["blue"])
    # proxy legend
    from matplotlib.lines import Line2D
    ax.legend([Line2D([0], [0], color=W["blue"], lw=1.8),
               Line2D([0], [0], color=W["green"], lw=1.3, ls="--")],
              [r"measured $\gamma=1$", r"exact $\gamma=1$"], loc="upper right")
    ax.set_xlabel(r"erasure probability $p$")
    ax.set_ylabel(r"rate $R$ (nats/use)")
    ax.set_title(rf"boundary MAE $=\,{j['boundary_mae']:.4f}$ nats", fontsize=8)
    fig.tight_layout()
    save(fig, "fig_e4_phase")


# ------------------------------------------------------- E1 reliability / IS
def fig_e1():
    d = npz("D2-E1")
    j = js("D2-E1")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.6))
    # (a) m=2 : IS on exact, naive MC biased low
    p = d["m2_ps"]
    a1.plot(p, d["m2_g_exact"], color="black", lw=1.6, label=r"exact $\gamma(2)$")
    a1.fill_between(p, d["m2_g_lo"], d["m2_g_hi"], color=W["blue"], alpha=0.25)
    a1.plot(p, d["m2_g_is"], color=W["blue"], lw=1.3, label="importance sampling")
    a1.plot(p, d["m2_g_mc"], color=W["red"], ls="--", lw=1.3, label="naive Monte Carlo")
    a1.axhline(1.0, color=W["grey"], ls=":", lw=1.0)
    a1.axvline(0.25, color=W["green"], ls=":", lw=1.1)
    a1.set_xlabel(r"erasure probability $p$")
    a1.set_ylabel(r"moment multiplier $\gamma(2)$")
    a1.set_ylim(0, 2.2)
    a1.legend(loc="upper left")
    a1.text(-0.16, 1.02, "(a)", transform=a1.transAxes, fontweight="bold", fontsize=10)
    # (b) crossings at p_c(m)=k^{-m}
    for mm, col, lab in [("m1", W["green"], "1"), ("m2", W["blue"], "2"),
                         ("m4", W["orange"], "4")]:
        a2.plot(d[f"{mm}_ps"], d[f"{mm}_g_is"], color=col, label=rf"$m={lab}$")
    a2.axhline(1.0, color=W["grey"], ls=":", lw=1.0)
    for pc, col in [(0.5, W["green"]), (0.25, W["blue"]), (0.0625, W["orange"])]:
        a2.axvline(pc, color=col, ls=":", lw=1.0)
    a2.set_xlabel(r"erasure probability $p$")
    a2.set_ylabel(r"$\gamma(m)$ (importance sampling)")
    a2.set_ylim(0, 2.2)
    a2.set_title(r"$p_c(m)=k^{-m}=\{\frac{1}{2},\frac{1}{4},\frac{1}{16}\}$", fontsize=8)
    a2.legend(loc="upper right")
    a2.text(-0.16, 1.02, "(b)", transform=a2.transAxes, fontweight="bold", fontsize=10)
    fig.tight_layout()
    save(fig, "fig_e1_reliability")


# ------------------------------------------------------- E2 two conditions
def fig_e2():
    d = npz("D2-E2")
    j = js("D2-E2")
    p = d["ps"]
    pR = j["p_R"]
    fig, ax = plt.subplots(figsize=(3.5, 2.75))
    ax.plot(p, d["escape"], color="black", lw=1.7, label=r"escape rate (cond. R)")
    ax.axvline(pR, color=W["grey"], ls="--", lw=1.2)
    ax.text(pR + 0.004, 0.5, rf"$p_R={pR:.3f}$", fontsize=7.2, rotation=90, va="center")
    ax.set_xlabel(r"erasure probability $p$")
    ax.set_ylabel("a.s. escape rate")
    ax.set_ylim(-0.03, 1.05)
    ax2 = ax.twinx()
    for g, col, lab in [("gamma_m1", W["green"], "1"), ("gamma_m2", W["blue"], "2"),
                        ("gamma_m4", W["orange"], "4")]:
        ax2.plot(p, d[g], color=col, lw=1.2, ls="-", label=rf"$\gamma({lab})$ (cond. A)")
    ax2.axhline(1.0, color=W["red"], ls=":", lw=1.0)
    ax2.set_ylabel(r"moment multiplier $\gamma(m)$")
    ax2.set_ylim(0, 3.0)
    ax.set_xlim(0, 0.16)
    l1, la1 = ax.get_legend_handles_labels()
    l2, la2 = ax2.get_legend_handles_labels()
    ax.legend(l1 + l2, la1 + la2, loc="upper left", fontsize=6.6)
    fig.tight_layout()
    save(fig, "fig_e2_two_conditions")


# ------------------------------------------------------- E5 achievability
def fig_e5():
    d = npz("D2-E5")
    j = js("D2-E5")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.55))
    # (a) faithfulness: 2-D cat observer vs 1-D reduction
    p = d["ps"]
    a1.plot(p, d["esc_2d"], color=W["blue"], lw=1.6, label="genuine 2-D cat observer")
    a1.plot(p, d["esc_1d"], color=W["orange"], ls="--", lw=1.4, label="1-D reduction")
    a1.set_xlabel(r"erasure probability $p$")
    a1.set_ylabel("escape rate")
    a1.set_title(rf"faithfulness MAE $=\,{j['faithfulness_mae']:.1e}$", fontsize=8)
    a1.legend(loc="upper left")
    a1.text(-0.17, 1.02, "(a)", transform=a1.transAxes, fontweight="bold", fontsize=10)
    # (b) sufficiency: log second moment over time, stable vs unstable
    t = np.arange(len(d["traj_stable"]))
    a2.plot(t, d["traj_stable"], color=W["blue"],
            label=r"$p<p_c$ ($\gamma=0.75$): bounded")
    a2.plot(t, d["traj_unstable"], color=W["red"], ls="--",
            label=r"$p>p_c$ ($\gamma=1.24$): grows")
    a2.set_xlabel("step $t$")
    a2.set_ylabel(r"$\ln \mathbb{E}[\delta_t^2]$")
    a2.legend(loc="upper left")
    a2.text(-0.17, 1.02, "(b)", transform=a2.transAxes, fontweight="bold", fontsize=10)
    fig.tight_layout()
    save(fig, "fig_e5_achievability")


# ------------------------------------------------------- M1 two rates
def fig_m1():
    d = npz("D2-M1")
    j = js("D2-M1")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.6))
    # (a) a.s. escape: volume rate binds
    p = d["ps"]
    a1.plot(p, d["esc_prop"], color=W["blue"], lw=1.6,
            label="proportional (all modes)")
    a1.plot(p, d["esc_top"], color=W["orange"], ls="--", lw=1.4,
            label="top-only allocation")
    a1.axvline(j["p_R_vol"], color=W["green"], ls=":", lw=1.3)
    a1.axvline(j["p_R_top"], color=W["grey"], ls=":", lw=1.3)
    a1.text(j["p_R_vol"] + 0.006, 0.35, rf"$p_R(r^\star_{{\mathrm{{vol}}}})={j['p_R_vol']:.3f}$",
            fontsize=6.8, rotation=90, va="center")
    a1.text(j["p_R_top"] + 0.006, 0.35, rf"$p_R(r^\star_{{\mathrm{{top}}}})={j['p_R_top']:.3f}$",
            fontsize=6.8, rotation=90, va="center", color=W["grey"])
    a1.set_xlabel(r"erasure probability $p$")
    a1.set_ylabel("a.s. escape rate")
    a1.set_ylim(-0.03, 1.05)
    a1.legend(loc="upper left", fontsize=6.8)
    a1.text(-0.17, 1.02, "(a)", transform=a1.transAxes, fontweight="bold", fontsize=10)
    # (b) moment thresholds at r_top
    pm = d["ps_m"]
    pc = j["pc_moment"]
    for g, col, lab, key in [("gamma_m1", W["green"], "1", "1"),
                             ("gamma_m2", W["blue"], "2", "2"),
                             ("gamma_m4", W["orange"], "4", "4")]:
        a2.plot(pm, d[g], color=col, label=rf"$\gamma({lab})$")
        a2.axvline(pc[key], color=col, ls=":", lw=1.0)
    a2.axhline(1.0, color=W["grey"], ls=":", lw=1.0)
    a2.set_xlabel(r"erasure probability $p$")
    a2.set_ylabel(r"moment multiplier $\gamma(m)$")
    a2.set_ylim(0, 2.4)
    a2.set_title(r"$p_c(m)=e^{-m r^\star_{\mathrm{top}}}$", fontsize=8)
    a2.legend(loc="upper right")
    a2.text(-0.17, 1.02, "(b)", transform=a2.transAxes, fontweight="bold", fontsize=10)
    fig.tight_layout()
    save(fig, "fig_m1_two_rates")


if __name__ == "__main__":
    set_style()
    fig_e4()
    fig_e1()
    fig_e2()
    fig_e5()
    fig_m1()
    print("D2 paper figures written to", OUT)
