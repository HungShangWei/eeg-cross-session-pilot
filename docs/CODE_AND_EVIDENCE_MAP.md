# Code and evidence map

This is a **partial-source showcase**, prepared from the specified reference package and selected local source files. **Code/results linkage is incomplete.** Static identities and source calls are not end-to-end reproduction. No claim is made that the current repository HEAD is the historical run version; Git HEAD was not used as evidence.

## Public entry points

| Relative path | Purpose | Source and verification level |
|---|---|---|
| [README.md](../README.md) | Neutral introduction and contribution | New summary of S-E4, S-MASTER, and S-ROLE; no new scientific result |
| [Methods and limitations](PILOT_METHODS_AND_LIMITATIONS.md) | Definitions, design, qualifications | S-E4 §§1–5, 7–8, 10 and S-MASTER §§4–5; documentary interpretation |
| [Primary saved results](../results/primary_saved_results.csv) | Seven selected records | S-FACTORS exact decimal strings and source pointers; path-sanitized projection, not a byte-identical table copy |
| [Results guide](../results/README.md) | Intervals, denominators, and interpretation | S-E4 §3; static transcription check only |
| [Data provenance](../data/README.md) | Dataset citation and redistribution boundary | S-MASTER reference [13], carried forward without current web verification |
| [Rights and dependencies](RIGHTS_AND_DEPENDENCIES.md) | Existing notice, imports, and omissions | Current selected source text and S-LICENSE; no runtime verification |
| [Existing source license](../code/LICENSE) | Preserve applicable source notice | S-LICENSE copied byte for byte; no new showcase-wide license selected |
| [.gitignore](../.gitignore) | Convenience exclusions | Newly written; not a publication whitelist or history cleanup |

## Selected source modules

Every module below is copied without edits. Original headers and flat sibling import names are retained. Each SHA-256 matches its entry in S-DEP, the historical DREC01 active dependency manifest. S-OUT records the same scoring code-set identifier as S-DEP and the same result-file identity reported by S-FACTORS. These are documentary links: the entire code set, execution records, and original result content were not revalidated.

| Public module | Purpose | SHA-256 |
|---|---|---|
| [contracts_r1.py](../code/mi_ops_fixed_tail_v1_1/contracts_r1.py) | Indexed data, ordinal joins, access-account contracts, and guards | `2965cd4beaeedc081e18021f372fa4fdb49500f290efd0655199a8696b350361` |
| [evaluator_r2.py](../code/mi_ops_fixed_tail_v1_1/evaluator_r2.py) | Post-seal scoring orchestration and participant summaries; shows calls into the inference modules | `39a135a9cc71b9969635b737a44a890edb572ce09825f82bb6ad5f2a3d0e422e` |
| [inference_contract.py](../code/mi_ops_fixed_tail_v1_1/inference_contract.py) | H-P1, H-P2, and descriptive numerical rules | `3eecd3eb19b5b20df27cfbd8c450366f366e5893d73b4543aea10fd491450351` |
| [inference_r1.py](../code/mi_ops_fixed_tail_v1_1/inference_r1.py) | Audit wrappers that preserve unavailable statistics and gate no-label interpretations | `c8e75d0aeacf8efb1e9111cb1c6012d0862433143acc332a0ed247a8d082b1fd` |
| [magnitude_r1b.py](../code/mi_ops_fixed_tail_v1_1/magnitude_r1b.py) | Saved-change diagnostic definitions; no new diagnostics are produced here | `faafbeda80080b43224492f5fb0da1767d67a79f63d92a30680bf8861ae94ee6` |
| [row_identity_r2.py](../code/mi_ops_fixed_tail_v1_1/row_identity_r2.py) | Shared canonical row identifier used by the evaluator | `b63d914955904f31aade513c1f5f5abfe3bd46d496552e7f8f984686d7c75251` |
| [statistics_recipe.py](../code/mi_ops_fixed_tail_v1_1/statistics_recipe.py) | Proxy scoring, intervals, usefulness, and bootstrap definitions; none executed here | `f1aeb0f66fb79f2d77732b24a4bc492cd78a1eaec127d5a7dccdc55181aa3585` |

The evaluator source visibly calls `score_synthetic`, `hp1`, `hp2_checked`, and `audited_descriptive`. The historical `score_synthetic` name is preserved; its presence and the manifest match do not make synthetic engineering checks empirical verification. The lower-level descriptive function is not an audited no-label result on its own: the wrapper checks label-access accounts and can return `NOT_EVALUABLE`.

The selected subset includes every local module it imports, but lacks the original loaders, learning/adaptation implementation, seal/capability producers, trial inputs, orchestration, and complete runtime environment. It is therefore not a one-command reproduction package. No runner has been written.

## Private source aliases

These records are **not included in the public snapshot** unless explicitly linked above. The aliases below are descriptive provenance identifiers, not links to private filesystem locations. Full internal documents, reference archives, and local absolute paths remain in the private review record.

| Alias | Version or identity | Use and boundary |
|---|---|---|
| S-REFERENCE | Supplied pilot-showcase reference package, 2026-10-19 v1; SHA-256 `3017bc7af098b21179cddf8281bc04d62d6bdcca322cc8a5f5772daa4346fcae` | Its eight listed documents matched size and SHA-256; this checks identity, not research correctness |
| S-E4 | Reviewed bounded DREC01 results, 2026-10-04 v1; SHA-256 `679b9325dc9716117a3f86fdbecd88a84ce61c8b05198b7d5de8b224dcef96f5` | Scientific interpretation and unresolved gaps |
| S-MASTER | Internal master research note v2; SHA-256 `4e3f1e7f68037babfbef65aaabd5e0b39a60b2cebc9fe2bd40b158bde2479876` | Pilot/future-work distinction and later administrative adoption; not a public manuscript |
| S-ROLE | Targeted wording confirmation, v1; SHA-256 `dbb4a7b59efc27d9702345fb67a6b2637ed9a3cb4898d30588ce9b86591c5ff1` | Confirmed contribution and definition of feedback recipients; not independent implementation or publication clearance |
| S-FACTORS | Original saved primary factors table, 167736 bytes; SHA-256 `36b2305029cec76e8226f34442d786ee6ae8605d9dc6989fc69e2085d6799efe` | Only selected saved scalar strings projected; original contains private paths |
| S-TABLE-GUIDE | Original table README; SHA-256 `4f2335ffaa98c7d3b51ce7788dafeedda47718a3b55b264da4070108454fba4d` | Source-pointer and missingness semantics; historical draft wording retained privately |
| S-E4-MANIFEST | Original scientific archive content manifest; SHA-256 `1f8a704c2a52628c4741a79e454961ad6c0b5283b94415d131725ae9fa6639b3` | Only the selected table and table-guide entries checked; remaining historical members were not requested |
| S-RESULT | Historical saved DREC01 scoring result; recorded SHA-256 `696c6308fd3dd35651acebafe5d47c400a25dafd0fc5c69ec25519077825da6d` | Identity carried by S-FACTORS and S-OUT; original result body was not opened for this preparation |
| S-DEP | DREC01 historical manifest; SHA-256 `55a7f534246534e7b0d700139885948457ddfcdc6bee2e1bf683c127d1505c34` | Selected code identity and conservative dependency closure |
| S-OUT | DREC01 historical manifest; SHA-256 `e0c61b3fe59ee6f2a63eb6b1ca6ef52ad52ae620d6353edacd2eb24f1f2d96ef` | Historical closeout identity record; selected metadata only |
| S-LICENSE | Existing repository license; SHA-256 `dda6c1138e19e0b0c6ff5598b25b954225dae4e172c183b61591298aff5b3ca3` | Preserved as code/LICENSE; existing terms are not replaced |

The historical scoring code-set identifier is `bc7a05dbfaf3937bf9b625834e4deff22c9745c426cb277c512fce03f1d81085`. It was read from matching manifest fields, not recomputed from the full dependency set. The earlier training code-set identity is a separate record and does not establish that all training source or state is included here.

Later adoption of bounded results and targeted wording review supersede earlier administrative pending labels for that limited purpose. They do not change `science_status=REVIEWED_WITH_UNRESOLVED_GAPS`, `publishable_as_pilot_results=false`, or authorize this candidate for publication.

## Scope of this preparation

Only file identity, selected value transcription, static source/import structure, local links, privacy exclusions, and packaging were checked. No research module was imported, no test or preflight was run, and no mean, confidence interval, bootstrap, D_use, or figure was computed. No raw data or trial-level output was read. No images were selected. External references were inherited rather than freshly verified.
