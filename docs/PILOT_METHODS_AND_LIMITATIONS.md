# Pilot methods and limitations

This document describes the bounded DREC01 analysis from saved summaries and the reviewed interpretation dated 4 October 2026. It does not certify execution order or reproduce the experiment. Source aliases are defined in the [code and evidence map](CODE_AND_EVIDENCE_MAP.md).

## Three distinct layers

| Layer | What exists | What it establishes here |
|---|---|---|
| Legacy V1 | Earlier descriptive, multiple-dataset benchmark with budget-dependent evaluation complements | Historical context only; its scores are not DREC01 results and do not establish decoder superiority |
| Historical Protocol v2 | Fixed-tail specification, implementation, and engineering records | A design and engineering history; synthetic prechecks are not formal empirical experiments |
| DREC01 | Saved nine-participant pilot analysis, later qualified in E4 and the master note | The limited results described below; not a reproduced end-to-end chain |

Some modules originated in earlier engineering stages and were reused in DREC01. Their inclusion is supported by DREC01 manifest identities, not merely by their directory or filename. Old comments and authorization flags remain unchanged as historical source text.

## Data, sessions, and analysis unit

The dataset is **BCI Competition IV-2b**, recorded left/right-hand motor imagery. The comparison uses physical session **3 → 4 within each participant**, for nine independent participants. The fixed target prefix contains 40 trial opportunities (ordinals 0–39); evaluation set Q starts at ordinal 40 and continues to the target-session end. Invalid opportunities are not replaced. The reviewed summary reports Q=80 for participant 2 and Q=120 for each other participant. These are saved documentary counts, not newly verified trial inventories.

The three neural seed bases are 1103, 2207, and 3301. Neural seeds are equally averaged within each participant, then participants are equally weighted. EA contributes a single deterministic branch per participant. Flows, seed instances, aliases, and result rows do not increase n beyond nine. Nothing in this snapshot was aggregated again from person-level or seed-level values.

## Operations and nominal feedback budget

| Operation | Definition | Qualification |
|---|---|---|
| T | Scalar-temperature recalibration using a positive scalar | Rescales confidence; a positive scalar preserves binary class ordering |
| H | Regularized classification-head update | Updates the classification head |
| K | Unchanged decoder | Makes no target update and does not fit on target labels; it still sees target features to predict |
| N | Normalization-statistics update | Intended no-label control; the actual label-access account is incomplete |
| EA-U | Alignment-based covariance control without target labels | Intended no-label control; the actual label-access account is incomplete |
| EA-L | Alignment-based covariance control with target labels | Saved composite result remains inconclusive |

The primary nominal label budget is **d=10**, within the fixed 40-trial prefix. A nominal entitlement is not evidence of ten labels actually received or used. A recipient is a receiving method instance or declared use endpoint. Unique acquisition, first use, reuse, and close events must be distinguished; repeated use across seeds or purposes does not create more independently acquired labels. Complete received/used/close accounts remain unverified.

Method names and saved active-fit indicators do not establish every solver, stopping condition, selected state, or data-use rule. Intended fit/freeze/seal/decode ordering is distinct from independently confirmed execution timing.

## Outcomes, direction, and missingness

At the primary cost c_D=0.25, accept a prediction when its top-class probability is at least 0.75; otherwise defer. The protocol defines:

- **J (decision loss):** (accepted wrong predictions + c_D × deferred opportunities) / all Q opportunities. Lower is better under this artificial rule.
- **C (coverage):** accepted opportunities / all Q opportunities. Higher means more availability under this rule, not automatically better decisions.
- **R (risk among accepted predictions):** accepted wrong predictions / accepted opportunities. If no predictions are accepted, R remains null.

Technical-invalid opportunities count as deferrals and stay in the Q denominator. Saved accuracy, balanced accuracy, kappa, NLL, and Brier use their valid-prediction definitions; they do not inherit a different denominator from J or C. None is a measure of human effort, clinical harm, neural purity, or robot benefit. J and C are dimensionless. Counts of qualifying participants have people as their interpretation, even though the original generic table labels its fields dimensionless.

Missing values are not zeros. The public CSV preserves the original decimal strings and original missingness annotation. `NOT_PROVIDED` marks an interval not supplied for a count; it is distinct from a saved `null` and from zero. Non-primary intervals, the prespecified D_use endpoint, and equal-coverage curves are absent from the supplied evidence and were not reconstructed. D_use was prespecified as the first tested budget meeting the individual J/C thresholds at that and all larger tested budgets; its absence is not a post hoc reason to redefine the endpoint.

## Saved primary result and usefulness

The [primary result table](../results/README.md) reports ordinary two-sided 95% t intervals, with n=9, df=8, and tail alpha=0.025. No alternative interval was selected to strengthen the result. T−H means T loss minus H loss; negative values favor T on J alone.

At the saved-summary and prespecified-rule level, the upper T−H J bound is below the non-inferiority margin 0.02. This is **non-inferiority, not equivalence**. Full H-P1 required this component, T usefulness, and T active fitting. T active fitting required at least six participants with at least two of three fixed seeds active. Saved active counts for T and H are both 9/9, but active fitting is not usefulness.

Usefulness requires all of the following: a group upper J bound below 0.20; a group lower C bound above 0.50; and at least seven of nine participants individually satisfying J≤0.20 and C≥0.50. T and H each failed both group bounds and had only five qualifying participants. Thus complete H-P1 is unsupported. H's useful fitted-reference qualification is a separate assessment, not a fourth H-P1 condition. Its qualification is also unestablished. The result cannot be explained solely as wide intervals: the participant guard also failed. Failure to establish usefulness does not prove that usefulness is impossible.

## Other comparisons and interval qualifications

H-P2 required more than 0.02 lower J than **each** of K, N, and EA-U, together with usefulness and active fitting. The candidate-adjusted rule uses alpha=0.025/3 and the specified intersection–union logic. The saved result excludes this **joint meaningful-gain claim** for T and H; it does not exclude every individual comparison or all value of labels. EA-L remains inconclusive. The two descriptive no-label comparisons, N versus H and EA-U versus H, remain `NOT_EVALUABLE` because of incomplete label-access accounts; their missing statistics were not filled.

The complete nine contrasts and saved bootstrap intervals are not displayed in this compact snapshot. Ordinary t, ordinary bootstrap, and candidate-adjusted bounds are different quantities and must not be substituted for one another. The historical `no_bootstrap_upgrade` label does not certify a new robustness result. Other costs are descriptive: the reviewed source reports sign reversals at cost 0.40 relative to 0.10/0.25 for selected contrasts, so the primary result does not establish cost-invariant superiority.

## What remains unverified or untested

The available evidence includes saved summaries, source text, and selected manifests. Complete label-use accounts, fit/freeze/seal/decode event binding, and some method/state records remain unresolved. The included code can show intended rules; it cannot prove their complete historical execution. K's unchanged state does not imply no contact with target features.

Preprocessing was offline within completed buffers, including a zero-phase path; causal streaming was not demonstrated. Seven ineligible fits, fallback/missingness records, the original `STOPPED_D` and later `D_RECOVERED` history, and earlier complete-container data contact remain part of the interpretation. This was not a fresh blind test. Historical failures and partial records are not erased by the later recovery. Saved summaries do not establish an artifact-free or purely neural signal.

No multimodal fusion, second modality, neural supervision, neural-versus-non-neural increment, free intention, human-time efficiency, or live human/robot benefit was tested. Two models reading the same EEG do not constitute two modalities. Future work may test these questions after feedback-use and execution evidence are made accountable; they are not completed achievements.

The inherited scientific status is **`REVIEWED_WITH_UNRESOLVED_GAPS`** and **`publishable_as_pilot_results=false`**. Later administrative adoption and targeted wording review do not remove these limitations or authorize publication of this candidate.
