# R2 source code

`candidate/` contains the source files of the exact code identity that ran as `DREC01_CORE_VALIDATION_R2` on 2026-10-27. The 39 Python files are byte-identical to the executed files. In the three files under `candidate/config/`, the author's local project path was replaced by `<PROJECT_ROOT>`.

- What each file does, which copies were effective at run time, and the original versus public hashes: [docs/CODE_AND_EVIDENCE_MAP.md](../../docs/CODE_AND_EVIDENCE_MAP.md)
- How the code was run, and what a re-run would require: [docs/REPRODUCIBILITY.md](../../docs/REPRODUCIBILITY.md)
- Licence: MIT ([LICENSE](LICENSE)), covering the software, configuration files and this README in `code/r2/`; scope and exclusions: [docs/RIGHTS_AND_DEPENDENCIES.md](../../docs/RIGHTS_AND_DEPENDENCIES.md)

The code is kept as it ran. It is not a packaged library, and its entry points refuse to start without the original environment, paths, identity manifest and a local approval record. Some docstrings and constants (for example "no real dataset has been scored" or `publishable_as_pilot_results=False`) were written during code preparation and were left unchanged so that the files stay byte-identical; they do not describe R2, which ran this code on real data. Internal labels such as `PREP`, `grant` and `B2R` are explained in the [code map](../../docs/CODE_AND_EVIDENCE_MAP.md#internal-labels-you-will-meet-in-the-code).
