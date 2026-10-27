#!/usr/bin/env python3
"""Draw the saved R2 participant-level results (display only, no new analysis).

Reads results/primary_results.json (SHA-256 pinned) and plots, for each of the
nine participants, the saved seed-averaged decision loss J and coverage C of
T (temperature recalibration) and H (classification-head update), with the
fixed individual thresholds J <= 0.20 and C >= 0.50. No value is re-estimated;
the plotted numbers are the fields under /summary/participants.

Requires matplotlib (the R2 environment had matplotlib 3.11.2 installed as a
dependency of pyriemann). From the repository root:
    python scripts/plot_participant_results.py
writes results/figures/r2_participant_results.png.
"""
import hashlib
import json
import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results" / "primary_results.json"
SOURCE_SHA256 = "55fdcec96d44fd73411f7c23b183cad7799a5fb5bbbd125cce8dc7224dde3152"
OUT = ROOT / "results" / "figures" / "r2_participant_results.png"

J_MAX, C_MIN = 0.20, 0.50
INK, INK_2, GRID, SURFACE, BAND = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb", "#f0efeb"
SERIES = {"T": ("#2a78d6", "o", "T  temperature recalibration"),
          "H": ("#eb6834", "s", "H  classification-head update")}


def main():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        sys.exit("refusing: results/primary_results.json is not the saved R2 result")
    rows = json.loads(raw)["summary"]["participants"]
    people = [r["participant"] for r in rows]
    meets = {m: [r[f"{m}_J"] <= J_MAX and r[f"{m}_C"] >= C_MIN for r in rows] for m in SERIES}

    plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK_2,
                         "xtick.color": INK_2, "ytick.color": INK_2, "text.color": INK})
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), facecolor=SURFACE)
    panels = [("J", "Decision loss J (lower is better)", J_MAX, f"individual threshold J ≤ {J_MAX:.2f}", (0, 0.36)),
              ("C", "Coverage C (higher is better)", C_MIN, f"individual threshold C ≥ {C_MIN:.2f}", (0, 1.02))]
    for ax, (metric, label, thr, thr_label, ylim) in zip(axes, panels):
        ax.set_facecolor(SURFACE)
        for i, p in enumerate(people):
            if meets["T"][i] and meets["H"][i]:
                ax.axvspan(p - 0.45, p + 0.45, color=BAND, zorder=0, lw=0)
        ax.axhline(thr, color=INK_2, lw=1, zorder=1)
        # Label placement avoids the plotted points: above the line on the left for J, below it on the right for C.
        if metric == "J":
            ax.text(0.55, thr + 0.006, thr_label, ha="left", va="bottom", color=INK_2, fontsize=9)
        else:
            ax.text(9.45, thr - 0.02, thr_label, ha="right", va="top", color=INK_2, fontsize=9)
        for m, offset in (("T", -0.14), ("H", 0.14)):
            color, marker, name = SERIES[m]
            ax.scatter([p + offset for p in people], [r[f"{m}_{metric}"] for r in rows], s=46, color=color,
                       marker=marker, edgecolors=SURFACE, linewidths=2, zorder=3, label=name)
        ax.set_xticks(people)
        ax.set_xticklabels([str(p) for p in people])
        ax.set_xlim(0.4, 9.6)
        ax.set_ylim(*ylim)
        ax.set_xlabel("Participant (BCI Competition IV 2b, physical session 3 → 4)")
        ax.set_title(label, loc="left", fontsize=11, color=INK)
        ax.grid(axis="y", color=GRID, lw=1)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    handles, labels = axes[0].get_legend_handles_labels()
    handles.append(plt.Rectangle((0, 0), 1, 1, color=BAND))
    labels.append("shaded: meets J ≤ 0.20 and C ≥ 0.50 for both T and H")
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.99))
    fig.text(0.01, 0.01, "Saved R2 values (DREC01_CORE_VALIDATION_R2): each point is one participant's mean over 3 seeds; "
             "10 permitted labels per update; display only, no new analysis.", fontsize=8, color=INK_2)
    fig.tight_layout(rect=(0, 0.04, 1, 0.92))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=160, facecolor=SURFACE, metadata={"Software": None})
    print("wrote", OUT.relative_to(ROOT), f"(T meets: {sum(meets['T'])}/9, H meets: {sum(meets['H'])}/9)")


if __name__ == "__main__":
    main()
