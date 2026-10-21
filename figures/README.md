# Visualizations of saved primary results

These four independent figures display seven existing scalar summaries and the ten endpoints of their five existing intervals. They are **visualizations of saved summaries, not a new analysis**. No mean, interval, participant count, p value, or other statistic is estimated here.

T means **scalar-temperature recalibration**. H means **regularized classification-head update**. The figures use nine people as the independent unit; neural seeds were averaged within each person in the saved analysis. The figures do not increase that sample size or reconstruct participant-level observations.

## Figures and exact input records

| Figure | Files | CSV record_id | Display and interpretation |
|---|---|---|---|
| 01 — Saved loss difference | [SVG](01_saved_loss_difference.svg) · [PNG](01_saved_loss_difference.png) | `T_minus_H_J` | Saved T-minus-H mean and ordinary two-sided 95% t interval; zero and the 0.02 non-inferiority margin are shown. Negative values indicate lower proxy loss for T only. The non-inferiority component was supported at the saved-summary and prespecified-rule level; this is not equivalence, superiority, or practical success. |
| 02 — Participant usefulness | [SVG](02_participant_usefulness.svg) · [PNG](02_participant_usefulness.png) | `T_guard`, `H_guard` | Each saved count is 5 of 9; the required count is 7 of 9. The count axis runs from zero to nine. No count intervals were supplied, so none is drawn. The counts alone identify neither the participants nor overlap between the methods. |
| 03 — Saved decision loss | [SVG](03_saved_decision_loss.svg) · [PNG](03_saved_decision_loss.png) | `T_J`, `H_J` | Saved means and ordinary two-sided 95% t intervals. The group criterion requires the **interval upper endpoint strictly below 0.20**, not a mean below 0.20. Both methods failed. No new method-difference test is inferred from interval overlap. |
| 04 — Saved coverage | [SVG](04_saved_coverage.svg) · [PNG](04_saved_coverage.png) | `T_C`, `H_C` | Saved means and ordinary two-sided 95% t intervals, on the original zero-to-one scale. The group criterion requires the **interval lower endpoint strictly above 0.50**, not a mean above 0.50. Both methods failed. Coverage is an acceptance share, not classification accuracy or human success. |

For Figure 02, each qualifying participant must meet **J≤0.20 and C≥0.50 simultaneously**. Both methods fell short of the required participant count, and both also failed the group interval criteria. These summaries do not establish that the same five people qualified for both methods.

## Source fields and threshold provenance

The sole numeric-results input is [results/primary_saved_results.csv](../results/primary_saved_results.csv), 7129 bytes, SHA-256 `29e4e3ab5eeeff2f2443b62395fdb7ffe90f2106febb4ed02b49fc7a96f9c341`. The script selects records by exact `record_id`; points use `estimate`, and the five interval pairs use `interval_lower` and `interval_upper` directly. It also checks the supplied interval type, confidence level, independent sample size, nominal budget, prefix, deferral cost, and acceptance threshold. Count rows retain `NOT_PROVIDED` for intervals.

The fixed 0.02 non-inferiority margin, strict upper-J<0.20 and lower-C>0.50 group rules, and 7-of-9 participant requirement are transcribed from the existing [results interpretation](../results/README.md#interpretation-beside-the-numbers) and [methods: saved primary result and usefulness](../docs/PILOT_METHODS_AND_LIMITATIONS.md#saved-primary-result-and-usefulness). The individual criteria are inclusive J≤0.20 and C≥0.50. These are existing rules, not thresholds selected from the plotted values.

All figures concern **primary nominal budget 10**, **fixed target prefix 40**, **deferral cost 0.25**, and **acceptance probability at least 0.75**. The nominal budget does not establish actual labels received or used.

J is (accepted errors + deferral cost × deferrals) divided by **all evaluation opportunities**. C is the accepted share of those opportunities. Technical-invalid opportunities remain in the denominator as deferrals. The saved denominators are Q=80 for participant 2 and Q=120 for each other participant; people are equally weighted after within-person neural-seed averaging. No pooled-trial or participant-level statistic is calculated here.

The five intervals are **ordinary two-sided 95% t intervals**, not bootstrap intervals, standard deviations, standard errors, or candidate-adjusted intervals. Plotting uses the full source decimal strings through decimal coordinate arithmetic. Figure 01 displays five decimal places; Figures 03 and 04 display four. Rounding affects labels only. SVG and PNG use the same drawing scene; the vector SVG description retains the exact input strings. Linear coordinate conversion, line lengths, and raster antialiasing are display operations, not statistical estimation.

## Redraw only these figures

From the root of this showcase copy, with Python and Pillow already available:

```sh
python3 scripts/plot_saved_results.py
```

The script reads only the public CSV as numeric evidence and the explicitly listed threshold constants. It uses an installed font for rendering, writes these four SVG/PNG pairs under `figures/`, and prints a JSON rendering record to standard output. It does not import or execute anything under `code/`, read original study data, train, score, sample, test hypotheses, or reproduce the experiment. It refuses a CSV with a different fingerprint. No installation commands or new environment lockfile are supplied.

The actual visualization environment used Python **3.14.7**, Pillow **12.3.0**, and the installed **Arial** font. SVG markup was generated with the Python standard library; PNGs were rendered at twice the output resolution and reduced to **1600 × 1200 pixels** for antialiasing. These versions describe this visualization only, not the original research environment. Matplotlib was unavailable in the two inspected installed Python environments; no package was installed or changed.

## Limits and rights

Visualization of saved summaries, not a new analysis. The non-inferiority component was supported at the saved-summary and prespecified-rule level, but neither method met the prespecified usefulness criteria. Incomplete label-use and event-chain evidence still qualify interpretation.

The original H-P1/H-P2 qualifications, offline preprocessing, earlier data contact, missing evidence, partial source-code scope, and absence of full reproduction remain unchanged. No individual distributions, overlap between qualifying participant sets, across-budget trajectories, or calibration curves can be recovered from these seven records. No new clinical, human, robot, or multimodal claim is made.

The scientific status remains **`REVIEWED_WITH_UNRESOLVED_GAPS`** and **`publishable_as_pilot_results=false`**. This is a local visualization candidate; the previous publication authorization for the fixed 16-file v1 does not publish these additions.

The original [rights and dependencies document](../docs/RIGHTS_AND_DEPENDENCIES.md), source-code notice, and evidence map are retained byte for byte as v1 records; their descriptions of the earlier preparation are historical. This addition introduces no new showcase-wide license, changes no existing source-code rights, and grants no EEG redistribution rights. The plot script is a figure-redrawing entry point, not a complete experiment-reproduction entry point.
