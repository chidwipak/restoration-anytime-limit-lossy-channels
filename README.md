# Restoration–Anytime Limit over Lossy Channels (D2)

Reproducible codebase and theoretical research repository for **Direction 2 (D2): Controlled Set-Invariance and Anytime Restoration of Expansive Dynamical Systems over Lossy Channels**.

## Abstract & Key Theoretical Results

This repository contains the mathematical proofs, importance-sampling Monte-Carlo engines, and paper publication assets for state estimation and stabilization of expansive dynamical systems over erasure/lossy communication channels.

### Core Theorems

- **Theorem D2★ (Necessity Condition)**:
  For a $C^1$ expansive map with expansion rate $h_R$ and top Lyapunov exponent $r^\star_{\mathrm{top}}$ operating over an erasure channel with packet drop probability $p$ and bit-rate $R$, $m$-th-moment controlled set-invariance holds **if and only if**:
  $$\gamma(m) = (1-p) e^{\frac{m(h_R - R)}{d^+}} + p e^{m r^\star_{\mathrm{top}}} < 1$$

- **Theorem D2★★ (Universal Zooming Quantizer Achievability)**:
  Establishes that the Universal Zooming Quantizer scheme guarantees anytime stability and bounded $m$-th-moment error over memoryless erasure and Gilbert-Elliott bursty channels whenever $\gamma(m) < 1$.

---

## Directory Structure

```
.
├── README.md                              # Main documentation & usage guide
├── requirements.txt                       # Python dependencies
├── .gitignore                             # Git ignore rules
├── docs/                                  # Theoretical research bibles & audits
│   ├── D2_Research_Bible_v3.md            # Primary D2 research bible
│   ├── MASTER_D2_HANDBOOK.md              # Master handbook with complete proofs
│   ├── D2_Research_Bible_Restoration...v1.md
│   ├── D2_Research_Bible_Restoration...v2.md
│   ├── PAPER_D2_experimental_section.md   # Manuscript experimental section draft
│   ├── resultsD2.md                       # Comprehensive experiment execution logs
│   └── VALIDATION_AUDIT.md                # Adversarial review gap analysis
├── src/                                   # Core Python simulation engine
│   ├── d2_sim.py                          # Zooming quantizer simulator & IS gamma estimator
│   ├── theory.py                          # Closed-form gamma(m) and critical p_c curves
│   ├── topology.py                        # Network graph & channel topology helpers
│   ├── stats_utils.py                     # Importance sampling & phase-transition fit
│   ├── plotting.py                        # Publication-quality plotting utilities
│   ├── runlog.py                          # Experiment logging engine
│   └── paper_figs_d2.py                   # Paper figure generator
├── experiments/                           # Experiment runners
│   ├── d2_experiments.py                  # Full experiment suite (D2-E1 .. D2-E7)
│   ├── d2_stress.py                       # Stress testing suite (D2-M1 .. D2-M4)
│   └── reproducibility.py                 # Reproducibility validator
├── publication/                           # Publication manuscript assets
│   ├── Latex/                             # main.tex LaTeX source
│   ├── Figures/                           # Vector & raster publication graphics
│   ├── Build/                             # Compilation outputs (PDF, log)
│   ├── Outline/                           # Paper structure outline
│   ├── References/                        # BibTeX citations & literature survey
│   └── Review/                            # Peer review responses
├── configs/                               # JSON experiment snapshots
└── results/                               # Generated experimental data & plots
    ├── data/                              # Array data (.npz) & metadata (.json)
    └── figures/                           # Publication figure outputs (PNG, PDF, SVG)
```

---

## Environment Setup & Reproduction

### Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running Experiments

```bash
# Run full D2 experiment suite (parallel execution across cores)
NJOBS=8 python experiments/d2_experiments.py

# Run quick verification smoke test
python experiments/d2_experiments.py --quick

# Run specific experiment subset
python experiments/d2_experiments.py --only E1,E4

# Run reviewer stress testing suite
python experiments/d2_stress.py
```

---

## License & Citation

Private research repository. All rights reserved.
