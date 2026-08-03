# D2 Internal Review Record

Manuscript: `Publication/D2/Latex/main.tex`; compiled `Publication/D2/Build/main.pdf` (9 pages, IEEEtran journal
class). Reviewer role: hostile IEEE Transactions on Automatic Control referee. Every item was checked against the
repository, which is the sole source of truth. Passes are recorded; fixes made during the review are noted.

## Pass 1 — compilation and formatting
The paper compiles with `tectonic` to a 9-page PDF in the official IEEEtran two-column journal format. After
fixes there are no error messages and no overfull or underfull horizontal boxes beyond the accepted tolerance.
The residual Times font-shape notices are a property of tectonic's XeTeX engine and do not appear in the standard
pdflatex build a referee uses. The five experimental figures were regenerated title-less at print resolution with
one consistent palette, and the system model is a TikZ drawing with a single clean feedback loop and no
overlapping objects.

## Pass 2 — scientific correctness
The headline result, the exact threshold gamma = (1-p) e^{m(h_R-R)/d+} + p e^{m r_top} < 1, matches
`D2_Research_Bible_v3.md`. The necessity rests on uniform burst expansion, renewal moment divergence including the
acknowledgment argument, and rate necessity by the law of large numbers and volume counting, exactly as in the
bible. The achievability rests on the universal zooming quantizer driven by the common index history, the
geometric-drift criterion, and the cat-map verification without quasi-conformality. The independence of the two
conditions, the linear sanity check, and the vector two-rate structure are stated correctly.

## Pass 3 — numbers traceable to the repository
Every quantitative claim was cross-checked against `resultsD2.md` and `PAPER_D2_experimental_section.md`. The
boundary error 0.0036, the reliability thresholds 0.4954, 0.2499, 0.0625, the two-condition values p_R = 0.126
and the cascade 0.0215, 0.057, 0.087, the faithfulness error 0.0001, the drift values gamma 0.75 and 1.24, the
two-rate values 1.4 and 1.0 with escape 0.329 against 0.364 and p_c(2) 0.1352 against 0.1353, the scaling mean
logarithmic error 0.0017, the non-normal errors 0.0087 and 0.3011 with factor 4.2 and 35, the Henon values 0.7255
and 1.3203 with escape 0.5171 against 0.5523, and the Gilbert-Elliott values 0.0354 against 0.3959 with spectral
error 0.0009 all appear verbatim in the logs.

## Pass 4 — writing rules
The manuscript body contains no itemized or bulleted lists. No hyphen or dash is used as a sentence connector.
The English is plain, the story flows from motivation to model to results to proofs to experiments to discussion,
and each figure and table is referenced and explained. Existing theory is attributed by citation and the
contributions are marked as the necessity, the achievability, the two-rate structure, and the validation.

## Pass 5 — figures, tables, captions, references
Six figures, the maximum allowed, each carrying one idea: the system model, the phase diagram, the reliability
law with importance sampling, the two conditions, the zooming-quantizer achievability, and the vector two-rate
separation. Five tables: notation, the novelty matrix, the scaling law, the non-normal comparison, and the
results summary. All 55 references are both defined and cited, so none is dropped and none is undefined. The
captions are self-contained.

## Residual open items (honestly scoped, not defects)
The correlated Gilbert-Elliott threshold is a conjecture with strong numerical support, the anytime tree code is
modelled by eventual delivery with its reliability requirement validated, the non-uniform stress systems are
mechanism validations, and delay is future work. These match the bible and `VALIDATION_AUDIT.md`.

## Verdict
The paper is internally consistent, correctly grounded, and formatted to the target journal. It is ready for
author names, affiliations, and a final human proofread.
