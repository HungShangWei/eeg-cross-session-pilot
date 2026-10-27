# Code and evidence map (R2)

[`code/r2/candidate/`](../code/r2/candidate/) holds the source files of the exact code identity that ran as `DREC01_CORE_VALIDATION_R2`. That identity is a manifest of 45 objects, SHA-256 `bdc2c4cd778b0c601ea7ff08b20c6272fd27187421cc2850bf32f62ac1353b4c`. The launcher checked it before the run started, and a close-out check after the run found all 45 objects unchanged ([VALIDATION_SCOPE.md](VALIDATION_SCOPE.md)). The candidate layout is unchanged; only its parent directory differs from the author's machine.

- **39 Python files are byte-identical** to the executed files.
- **3 configuration files** are copies in which only the author's absolute project path was replaced by `<PROJECT_ROOT>`. No other value changed, but their hashes differ from the executed files (listed below).
- **3 identity objects are not included**: the execution-command record (a pre-run administrative record holding local paths), and two internal planning records (`SOURCE_REUSE_DECISION_v1.json`, `WORKLOAD_AND_FEASIBILITY_v1.json`) that hold local paths and are not read by the code.

A machine-readable list of every file with its original and public hash is in [`R2_PROVENANCE.json`](R2_PROVENANCE.json).

## How the import path works

The launcher sets the import path to `runtime_modules/`, then `frozen/`, then the candidate root. Six modules exist in both folders; for those, the `runtime_modules/` copy is the one that ran. The `frozen/` copies are kept because they are part of the bound identity and show what was changed for R2:

| Module | Effective copy | What the R2 copy changes relative to `frozen/` |
|---|---|---|
| `composition_r2.py` | `runtime_modules/` | records a `schema_validation` label use before T/H adaptation |
| `contracts_r1.py` | `runtime_modules/` | the source freeze requires only the T, H and checkpoint choices (the frozen copy also required N and EA choices) |
| `numeric_dependencies_r2.py` | `runtime_modules/` | records `class_gate` and `optimizer` label uses during target fitting |
| `source_recipe_e3prep.py` | `runtime_modules/` | develops only T and H on the source session (no N or EA branches) |
| `statistics_recipe.py` | `runtime_modules/` | refuses to generate a new bootstrap matrix; only the existing matrix may be used |
| `trusted_ingress_r1b.py` | `runtime_modules/` | adds audit records around source preprocessing |

## What each file does

**Entry and run control (candidate root)**

| File | Role |
|---|---|
| `supervise.py` | Formal entry point. Checks the code identity, the local approval record, the Python environment and a new run directory. Starts `launch.py` as a child process, enforces a time cap and keeps a separate supervisor ledger. |
| `launch.py` | Worker entry. Repeats the identity, approval and environment checks, and requires the supervisor's handoff record. Installs an audit hook that blocks writes outside the run directory and all network access. Sets the import path and runs `flow.execute_core`. |
| `resource_guard.py`, `native_helper_dr1m.py` | Resource checks during the run (memory pressure, available memory, process memory, free disk, allocated bytes), using three allow-listed macOS tools (`vm_stat`, `sysctl`, `ps`). |
| `flow.py` | Orchestration. Qualifies all nine participants before any fitting, prepares the sources, loops over 54 instances (request → receipt → adaptation → state saved → Q prediction → end of label access), then seals, releases Q labels to scoring and scores. |
| `data_service.py` | Trusted data service. Verifies and loads the MAT files and partitions trials; applies the frozen preprocessing; enforces the source freeze and the one-time S-cal release; serves the 10-position target prefix view and the label-free Q view; returns Q labels only after the seal is verified. |
| `model_adapter.py` | T/H adapter. Builds source states, copies them per instance, binds the receipted labels during adaptation, saves states and predictions, then scores sealed outputs and writes `primary_results.json`. |
| `audit_core.py` | Hash-chained event ledger; `Feedback` (request, receive, use, end); allowed-state-change check; `Cohort` (seal and post-seal label release). |
| `account.py`, `content_identity.py` | Call accounting and checks of label digests against the receipted view; content hashing, state fingerprints, artifact storage. |
| `scorer.py` | Per-instance J and C; aggregation (3 seeds, then 9 participants); call to the primary inference. |
| `independent_statistics.py` | Second, pure-Python implementation of the inferential outputs, compared with the primary one at tolerance 1e-10. |

**Science recipe (`frozen/`, effective unless shadowed above)**

| File | Role |
|---|---|
| `science_contract.py` | Constants (prefix 40, budgets, primary budget 10, seed bases) and the source and target partitions |
| `signal_recipe.py` | Preprocessing: 8–32 Hz zero-phase band-pass, EOG regression, resampling to 128 Hz, crop, standardization |
| `neural_recipe_r2.py` | EEGNet-style network, deterministic setup, feature extraction, batch-normalization moment recomputation |
| `source_selection.py` | Checkpoint and T/H setting grids with their tie rules |
| `solvers_recipe_r1.py`, `operations_r1.py` | Temperature grid search, regularized head refit (L-BFGS-B), grid construction, candidate checks |
| `inference_contract.py` | Composite primary-hypothesis logic (non-inferiority, usefulness, active guard, bootstrap robustness) |
| `accounting_r2.py` | Array fingerprints used by the numerical wrappers |
| `inference_r1.py`, `ea_recipe_r2.py`, `array_edges_r1.py` | Part of the bound identity. Code for comparisons outside R2 (H-P2 checks, alignment-based features); not called on the T/H path |

**Tests (`tests/`)**: synthetic engineering tests of the boundaries, the integration path and the start-up guards. They need the original directory layout, the original environment and a local scratch directory, and **were not run for this showcase**.

**Configuration (`config/`)**: `RUN_CONFIG_v1.json` (protocol hash, design constants, recipe, decision rule, resource policy), `DATA_MANIFEST_v1.json` (MAT files and their sessions, sizes and hashes), `ENVIRONMENT_METADATA_v1.json` (interpreter and five package versions). Two fields record the pre-run administrative state: `preparation_status` is checked by the entry points, and `formal_execution_authorized` (false) is not read by them (only an engineering test reads it). Both are kept unchanged.

**Stale comments in executed files.** Some docstrings and module constants were written while the code was being prepared and were not updated afterwards, because every file must stay byte-identical to what ran. Examples: `scorer.py` says no real dataset has been scored; `supervise.py` says it was not executed during preparation; `runtime_modules/source_recipe_e3prep.py` says its body has not been run; and several modules (`frozen/science_contract.py`, `contracts_r1.py`, `source_recipe_e3prep.py`, `frozen/accounting_r2.py`) carry flags such as `publishable_as_pilot_results=False` or `non_formal=True`. These describe the preparation stage, not R2, which did execute this code on real data on 2026-10-27.

| Config file | Executed SHA-256 | Public copy SHA-256 |
|---|---|---|
| `RUN_CONFIG_v1.json` | `388e2172e0ae8a803451dd7e50dee8af2b5d3a1aecac7154eb6317744c7d6bed` | `e65f6088e193414274ffcff7fda46ececd6dc9177bce0d8fb5d96df6d017ead1` |
| `DATA_MANIFEST_v1.json` | `d547ea29c8f64363aa68c0e43178e5c3609155fae43cbb224224bf85c12d80e3` | `8cf7112a2bb38255c0cc82caa2b5852fcb4089972ff6930aeb7a054014501538` |
| `ENVIRONMENT_METADATA_v1.json` | `6a16b2bcf0571a16e2a6df925b974805c530b9a5376ce5d3bc0c358897436511` | `42970ac30f9d42448783decc304a6f357e714274218172bb645b0d1aeb24c492` |

## Internal labels you will meet in the code

| Label | Meaning |
|---|---|
| `DREC01` | the project's internal name for this cross-session T-versus-H study (the earlier snapshot used the same name; see [HISTORY.md](HISTORY.md)) |
| `R1`, `R2` | first and second validation launches of the fixed pipeline; R1 stopped at start-up before reading data, R2 is the run reported here |
| `candidate` | the frozen code folder whose exact bytes were bound and executed |
| `B2R`, `B2_R` | internal name of the code revision used for R2 (appears in schema names, error codes and local folder names) |
| `PREP`, `prep_root`, `parent_prep_root` | the code-preparation stage before the run and its local folders; at run time the disk guard only measures their size |
| `grant`, `approval` | the author's own pre-run sign-off record that the entry points require (not an ethics, institutional or external approval) |
| `E1`, `E2`, `E3`, `OPS01`, `H-P1`, `H-P2` | stage and hypothesis labels from earlier protocol documents; in R2 only the H-P1 logic (T substitutes for H) is evaluated |
| `K`, `N`, `EA`, `EA_source`, `EA_L` | comparators of the earlier, broader analysis; present in shadowed or unused code, not run in R2 |

## Relation to the earlier public code

The earlier snapshot of this repository published seven modules under `code/mi_ops_fixed_tail_v1_1/` ([HISTORY.md](HISTORY.md)). Four of them are byte-identical to R2's `frozen/contracts_r1.py`, `frozen/inference_contract.py`, `frozen/inference_r1.py` and `frozen/statistics_recipe.py`. For `contracts_r1.py` and `statistics_recipe.py`, the copies that actually ran in R2 are the modified `runtime_modules/` versions described above. The other three earlier modules (`evaluator_r2.py`, `magnitude_r1b.py`, `row_identity_r2.py`) are not part of R2.

## Where each claim is supported

| Claim | Code | Saved evidence (public) |
|---|---|---|
| Each update received and used only valid pairs from positions 0–9 of session 4 | `data_service.py` (prefix), `audit_core.py` (Feedback), `account.py`, `runtime_modules/numeric_dependencies_r2.py`, `runtime_modules/composition_r2.py` | aggregate feedback counts in [R2_PROVENANCE.json](R2_PROVENANCE.json) (`feedback`) |
| Only the temperature (T) or the head (H) changed | `audit_core.state_change`, `content_identity.py` | `state_changes` in R2_PROVENANCE.json |
| Predictions were sealed before the scorer obtained Q labels | `audit_core.Cohort`, `data_service.scoring_labels`, `flow.py` | `ordering` in R2_PROVENANCE.json |
| J, C, intervals and decisions | `scorer.py`, `runtime_modules/statistics_recipe.py`, `frozen/inference_contract.py`, `independent_statistics.py` | [results/primary_results.json](../results/primary_results.json) |
| Preprocessing and models fitted on source data only | `frozen/signal_recipe.py`, `runtime_modules/trusted_ingress_r1b.py`, `runtime_modules/source_recipe_e3prep.py` | code only (no fitted parameters are published) |

The event ledger itself (about 79 MB, which includes label values), the seal file, the saved states and the per-trial predictions are **not** published. The public evidence is limited to aggregate counts and ordering facts taken from the run's own summaries. See [VALIDATION_SCOPE.md](VALIDATION_SCOPE.md).
