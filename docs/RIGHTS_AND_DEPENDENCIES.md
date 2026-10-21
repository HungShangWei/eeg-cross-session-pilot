# Rights and dependencies

## Existing source notice

The seven Python modules under [code/mi_ops_fixed_tail_v1_1](../code/mi_ops_fixed_tail_v1_1/) are unchanged copies of selected local research source files. The originating repository contains an MIT License with `Copyright (c) 2026 Shang-Wei Hung`. Its complete text is retained, byte for byte, as [code/LICENSE](../code/LICENSE) for the copied source material. Original file headers and comments are preserved.

This preparation does not choose a new license for the entire showcase, replace an existing license, or extend a software license to the EEG dataset. The candidate's overall licensing and any necessary third-party rights remain subject to review before a separately authorized publication. Existing applicable rights and notices remain in force. No dependency source, dependency binary, raw EEG, model weight, figure, or third-party document is bundled. The historical internal reference documents are not redistributed here.

## Dependency declarations retained in source

Static inspection of the copied import statements identifies **NumPy** and **SciPy** (`scipy.stats.t`, `scipy.special.expit`), plus Python standard-library modules. Imports of local modules retain their original names and sibling layout. All local import targets appearing in this selected seven-file subset are present. The files originally used flat sibling imports; this is not a newly packaged Python distribution.

No package was installed, imported, upgraded, or executed for this preparation. Runtime versions and compatibility of this subset were not tested. A DREC01 environment lockfile is not included, and no version pins have been invented or borrowed from the legacy V1 requirements. The historical dependency manifest notes separate NumPy/SciPy environment metadata; this snapshot does not claim that environment has been reconstructed. External packages retain their own terms when obtained separately.

## Execution boundary

This is source for reading, not a complete runnable experiment. The modules contain scoring, statistical, and bootstrap functions, but none was called during preparation. No new runner or reproduction command has been added. Data loaders, model training, adaptation execution, orchestration, runtime capabilities, saved trial inputs, and complete execution records are absent. The preserved `score_synthetic` name and historical engineering comments do not mean that synthetic checks reproduced the DREC01 empirical chain; the [evidence map](CODE_AND_EVIDENCE_MAP.md) explains the limited static linkage.

The public `.gitignore` is a convenience only. It cannot remove prior Git history or authorize sharing files. Any later publication should use a separately approved clean snapshot of the fixed file whitelist, rather than the original research repository and its history.
