# Primary saved results

[primary_saved_results.csv](primary_saved_results.csv) contains **seven records**: five saved point estimates with their original ordinary 95% t intervals, and two saved participant counts. It is a selected, path-sanitized projection of `S-FACTORS`, interpreted with `S-E4` §3 and `S-MASTER` §4. These source aliases and their identities are documented in the [evidence map](../docs/CODE_AND_EVIDENCE_MAP.md).

| Quantity | Saved value | Ordinary 95% t interval |
|---|---:|---|
| T−H decision loss J | −0.000694444444444447 | [−0.00522386433735302, 0.0038349754484641252] |
| T decision loss J | 0.1838348765432099 | [0.10688411998237957, 0.26078563310404024] |
| T coverage C | 0.576388888888889 | [0.32398574895703375, 0.8287920288207442] |
| H decision loss J | 0.18452932098765432 | [0.10629624892673273, 0.2627623930485759] |
| H coverage C | 0.5995370370370371 | [0.3512736787514252, 0.847800395322649] |
| T participants meeting both individual thresholds | 5 of 9 | Not provided |
| H participants meeting both individual thresholds | 5 of 9 | Not provided |

All records concern the primary nominal budget **10**, fixed target prefix **40**, deferral cost **0.25**, and top-class acceptance probability **≥0.75**. Actual labels received and used are not established by the nominal budget. T is scalar-temperature recalibration; H is a regularized classification-head update.

## How to read the table

J is accepted errors plus deferral cost times deferrals, divided by **all evaluation opportunities**. C is the accepted share of those same opportunities. Technical-invalid opportunities remain in the denominator as deferrals. Q has 80 opportunities for participant 2 and 120 for each other participant in the reviewed record. Neural seeds are averaged within person, and people receive equal weight; this is not a pooled-trial estimate. The participant is the independent unit, n=9. Lower J is better under this proxy rule; higher C means more coverage. A negative T−H value favors T on J alone.

The five intervals are the saved ordinary two-sided **95% t intervals** (df=8, tail alpha=0.025). They are not bootstrap or candidate-adjusted intervals. No mean, bound, guard count, or other statistic was recalculated. Original reported decimal strings are retained in the CSV, including all digits; this does not imply equally precise scientific certainty.

The CSV keeps exact source field keys and source pointers for the point value and interval endpoints. `source_file_sha256_as_recorded` is the historical result-file identity reported by the supplied table, not a fresh hash of trial-level results. The source's private absolute filename is replaced by the safe alias `S-RESULT`. The reference table's own identity is `reference_table_sha256`. Original units, denominator annotation, transform, and missingness are retained in separate source columns; the more specific interpretation comes from `S-E4` §3. In particular, the source's generic “bootstrap bounds already saved” annotation does not make these selected t endpoints bootstrap intervals. The public projection is not byte-identical to the original CSV.

`NOT_PROVIDED` denotes an interval or interval metadata not supplied for the participant-count rows. A literal source `null` would remain missing, never zero; the seven selected point values contain no null. The supplied source documents report missing D_use, non-primary intervals, and other evidence gaps. This small table does not fill them or represent all saved results.

## Interpretation beside the numbers

The upper T−H bound is below the prespecified non-inferiority margin **0.02**, supporting that single component at the saved-summary and rule level. It does not establish equivalence. Practical usefulness additionally required group upper J<0.20, group lower C>0.50, and at least 7/9 participants with individual J≤0.20 and C≥0.50. T and H each fail both group bounds and the participant guard. Complete H-P1 is unsupported; H's useful-reference qualification is also unestablished and is not a fourth H-P1 condition.

The compact table focuses on T/H. The broader reviewed result excludes only their specified H-P2 composite meaningful-gain claim against K, N, and EA-U. EA-L is inconclusive; the two no-label subclaims remain `NOT_EVALUABLE`. Complete numerical control comparisons and bootstrap results are not displayed, and no conclusion of universal label uselessness or method equivalence follows. [Methods and limitations](../docs/PILOT_METHODS_AND_LIMITATIONS.md) explain the remaining qualifications.

These are artificial decision proxies, not human or clinical outcomes. Incomplete actual label-use and event-chain evidence, offline preprocessing, prior data contact, and the absence of a reproduced chain constrain all interpretations. Scientific status remains `REVIEWED_WITH_UNRESOLVED_GAPS`; `publishable_as_pilot_results=false`.
