# Reproducibility

Three levels are listed separately, each with its inputs, environment, outputs and **tested status**. That the original R2 command succeeded on the author's machine does not mean the path-projected public copy has been run. It has not.

## Level 1 — saved results → tables and figures (tested)

| | |
|---|---|
| Input | `results/primary_results.json` (included; SHA-256 pinned in the scripts); figures also read the pinned `code/r2/candidate/config/RUN_CONFIG_v1.json` for the non-inferiority margin |
| Environment | Tables: Python ≥ 3.9, standard library only. Figures: additionally Matplotlib |
| Commands | `python scripts/make_result_tables.py --check` (verify) · `python scripts/make_result_tables.py` (rewrite CSVs) · `python scripts/plot_participant_results.py` (both figures) |
| Outputs | `results/group_estimates.csv`, `results/participant_results.csv`, `results/decision_criteria.csv`, the tables embedded in `README.md` and `results/README.md`, `results/figures/r2_participant_results.png`, `results/figures/r2_loss_difference.png` |
| Status | Run for this showcase on 2026-10-27: the table script with Python 3.14.7, and the figure script with Matplotlib 3.11.2 from the R2 environment. No statistic is recomputed; the scripts only project and format saved fields. |
| Visual update check | 2026-10-27 (Asia/Taipei): both PNGs generated with existing CPython 3.14.7, Matplotlib 3.11.2 and DejaVu Sans; the table check also passed. Only saved values and the frozen margin were read, with no new statistics or research execution. The original showcase record above is retained. |

```bash
python scripts/make_result_tables.py --check
```

## Level 2 — data and fitted states → predictions (not available)

The fitted source models and adapted states (network weights, heads, temperatures) are **not published**. The candidate has no separate inference entry point: predictions are produced only inside the full run (Level 3), by `ModelAdapter.predict` after an adaptation. Prediction from saved states is therefore not possible with this repository, and no command is offered for it.

## Level 3 — raw data → full re-run (code provided; public copy not run)

**What ran.** On 2026-10-27, R2 was executed once on the author's machine with the command below, shown here with the local project path replaced by `<PROJECT_ROOT>`. The supervisor returned 0 after a process envelope of about 448 s.

```text
<PROJECT_ROOT>/.venv_mi_ops_e1_v1_1/bin/python -B \
  <CANDIDATE_PARENT>/candidate/supervise.py \
  --identity <CANDIDATE_PARENT>/CANDIDATE_IDENTITY_v2.json \
  --approval <path to the local approval record> \
  --run-root <PROJECT_ROOT>/validation_runs/drec01_core_validation_r2
```

`<CANDIDATE_PARENT>` was a directory inside the author's project; in this repository it corresponds to `code/r2/`. The working directory was `<CANDIDATE_PARENT>`.

**Requirements, as enforced by the code.** The entry points are deliberately strict and fail closed.

1. **Platform**: macOS. The resource guard calls `/usr/bin/vm_stat`, `/usr/sbin/sysctl -n kern.memorystatus_vm_pressure_level` and `/bin/ps` and parses their macOS output. It requires memory-pressure level 1, at least 16 GiB of available memory at start, and at least 15 GiB of free disk.
2. **Environment**: `config/ENVIRONMENT_METADATA_v1.json` must match `sys.executable`, `sys.version` and `sys.prefix` exactly. It must also match the five package versions in [environment/requirements-r2-core.txt](../environment/requirements-r2-core.txt) (CPython 3.14.7, NumPy 2.5.3, SciPy 1.18.1, PyTorch 2.14.1, pyRiemann 0.12, scikit-learn 1.9.1). The other packages of the original environment are listed in [environment/venv-freeze-2026-10-27.txt](../environment/venv-freeze-2026-10-27.txt).
3. **Data**: the 18 MAT files listed in [data/README.md](../data/README.md), at the paths in `config/DATA_MANIFEST_v1.json`. Each must match its expected size and SHA-256, or loading stops.
4. **Bootstrap matrix**: `protocol/participant_resamples.npy`, at the path in `config/RUN_CONFIG_v1.json` (`bootstrap.path`), with the pinned size and hash.
5. **Paths**: every `<PROJECT_ROOT>` in the three configuration files must be replaced by a real directory. The run root must not exist beforehand and must equal `run_root` exactly. The resource guard also measures the directories listed under `controlled_roots` and `retained_accounted_roots`, which describe the author's machine and need adapting.
6. **Code identity**: the launcher refuses to start unless a manifest lists every file under `candidate/` (paths relative to the candidate's parent directory, with byte sizes and SHA-256). Because step 5 changes the configuration files, a new manifest must be written. The resulting code identity is new and differs from R2's.
7. **Approval record**: both entry points require a local JSON approval record. It must name the run ID, the manifest's SHA-256, the resource policy `FORMAL_NORMAL_REQUIRED` and the exact list of authorized operations in `RUN_CONFIG_v1.json`. It must also carry an `approved_by` value, which `launch.py` and `supervise.py` compare with the original author's name. This is an administrative gate of the author's own workflow, not a scientific step. No approval record is published, and none of R2's authorization carries over to any other run. **Do not write an approval record in the author's name for your own run.** Instead, in your own copy, change that comparison in both files to your own name. Like the path edits in step 5, this changes the code identity (step 6), and the outputs are a new run, not R2.

**Steps.** (1) Obtain the data and place the files. (2) Create an environment with the pinned versions. (3) Edit the paths in `config/`. (4) In your own copy, set the `approved_by` comparison to your own name (item 7), then write the identity manifest and a local approval record for your own run. (5) Start `supervise.py` with `--identity`, `--approval` and a new `--run-root`. The supervisor starts `launch.py` itself; do not start `launch.py` directly. Outputs (ledgers, states, predictions, seal, `scoring/primary_results.json`) are written only under the run root.

**Tested status.** The public copy was *not* run end to end, and its dependencies were not installed for this showcase. The steps above are derived from the code, not from a completed public re-run. Cross-platform runs are not supported as written. For this showcase, the launcher was run only in its refusal modes, which stop before reading any data:

```bash
python -B code/r2/candidate/launch.py --check-unapproved   # stops: EXECUTION_NOT_APPROVED: PREP_BLOCKED (exit 2)
python -B code/r2/candidate/launch.py                      # stops: EXECUTION_NOT_APPROVED: EXACT_GRANT_REQUIRED (exit 2)
```

`--help` prints the options and then also exits with status 2, because the entry point's catch-all error handler intercepts the normal help exit.

**Engineering tests.** `code/r2/candidate/tests/` contains the synthetic boundary, integration and start-up tests used while preparing the code. They need the original directory layout, environment and bootstrap path, and they write to a scratch directory beside the candidate. They were not run for this showcase.
