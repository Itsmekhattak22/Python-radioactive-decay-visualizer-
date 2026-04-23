# ============================================================
#  visualizer.py  –  All matplotlib rendering
#  Uses persistent artists → no full ax.clear() per frame.
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
from config import FIGURE_SIZE, GRIDSPEC_ARGS, MAX_GRID_DISPLAY, get_theme


class DecayVisualizer:
    """
    Owns the figure and four sub-panels.
    Call `setup(fig, axes)` once, then `update(sim)` every frame.
    """

    def __init__(self) -> None:
        self.T = get_theme()

        # persistent line artists
        self._line_active  = None
        self._line_decayed = None
        self._bars         = None
        self._stats_text   = None
        self._atom_patches: list[Rectangle] = []
        self._grid_cols    = 0
        self._grid_n       = 0

    # ── one-time setup ───────────────────────────────────────

    def setup(self, fig, ax_timeline, ax_stats, ax_atoms, ax_bar) -> None:
        T = self.T
        self.fig        = fig
        self.ax_timeline = ax_timeline
        self.ax_stats   = ax_stats
        self.ax_atoms   = ax_atoms
        self.ax_bar     = ax_bar

        for ax in (ax_timeline, ax_stats, ax_atoms, ax_bar):
            ax.set_facecolor(T["axes_bg"])

        # ── Timeline ──────────────────────────────────────────
        ax_timeline.set_title("Decay Timeline", color=T["title_color"],
                               fontsize=9, pad=4)
        ax_timeline.tick_params(colors=T["text_color"], labelsize=7)
        ax_timeline.grid(True, alpha=T["grid_alpha"], color=T["text_color"])
        ax_timeline.set_xlabel("Step", color=T["text_color"], fontsize=7)
        ax_timeline.set_ylabel("Atoms", color=T["text_color"], fontsize=7)
        for spine in ax_timeline.spines.values():
            spine.set_edgecolor(T["accent_color"])
            spine.set_linewidth(0.6)

        self._line_active, = ax_timeline.plot(
            [], [], color=T["active_color"], lw=1.4, label="Active")
        self._line_decayed, = ax_timeline.plot(
            [], [], color=T["decay_color"],  lw=1.4, label="Decayed")
        ax_timeline.legend(loc="upper right", fontsize=6,
                           facecolor=T["stats_face"], labelcolor=T["text_color"],
                           edgecolor=T["accent_color"])

        # ── Stats ─────────────────────────────────────────────
        ax_stats.axis("off")
        self._stats_text = ax_stats.text(
            0.5, 0.5, "", ha="center", va="center",
            fontsize=9, color=T["active_color"],
            fontfamily="monospace", transform=ax_stats.transAxes,
            bbox=dict(facecolor=T["stats_face"], edgecolor=T["stats_edge"],
                      boxstyle="round,pad=0.7", linewidth=1.2),
        )

        # ── Atom grid ─────────────────────────────────────────
        ax_atoms.axis("off")
        ax_atoms.set_title("Atom Grid", color=T["title_color"],
                            fontsize=9, pad=4)

        # ── Bar chart ─────────────────────────────────────────
        self._bars = ax_bar.bar(
            ["Active", "Decayed"], [0, 0],
            color=[T["bar_active"], T["bar_decay"]], width=0.5,
        )
        ax_bar.set_title("Current Ratio", color=T["title_color"],
                          fontsize=9, pad=4)
        ax_bar.tick_params(colors=T["text_color"], labelsize=7)
        ax_bar.set_ylim(0, 1)          # will be rescaled on first update
        for spine in ax_bar.spines.values():
            spine.set_edgecolor(T["accent_color"])
            spine.set_linewidth(0.6)
        ax_bar.set_facecolor(T["axes_bg"])

    # ── per-frame update (NO ax.clear) ───────────────────────

    def update(self, sim) -> None:
        T   = self.T
        tl  = sim.timeline
        rem = sim.remaining
        dec = sim.decayed
        n   = sim.initial_atoms

        # 1. Timeline lines
        xs = tl["steps"]
        self._line_active.set_data(xs, tl["remaining"])
        self._line_decayed.set_data(xs, tl["decayed"])
        self.ax_timeline.set_xlim(0, max(sim.duration, 1))
        self.ax_timeline.set_ylim(0, n * 1.05)

        # 2. Stats text
        pct = (dec / n * 100) if n else 0
        self._stats_text.set_text(
            f"STEP  {sim.current_step:>4} / {sim.duration}\n\n"
            f"ACTIVE   {rem:>6}\n"
            f"DECAYED  {dec:>6}\n"
            f"DECAYED  {pct:>5.1f}%\n\n"
            f"T½  {sim.half_life:>4} steps"
        )

        # 3. Bar chart heights
        total = max(rem + dec, 1)
        for bar, h in zip(self._bars, [rem, dec]):
            bar.set_height(h)
        self.ax_bar.set_ylim(0, total * 1.12)
        # refresh bar y-ticks
        self.ax_bar.yaxis.set_major_locator(
            plt.MaxNLocator(nbins=4, integer=True))
        self.ax_bar.tick_params(colors=T["text_color"], labelsize=7)

        # 4. Atom grid (rebuild only when count changes)
        self._rebuild_atom_grid(sim.atom_states, n)

    # ── atom grid helper ─────────────────────────────────────

    def _rebuild_atom_grid(self, atom_states: list[bool], total: int) -> None:
        T    = self.T
        disp = atom_states[:MAX_GRID_DISPLAY]
        nd   = len(disp)

        # rebuild patches only when atom count changes
        if nd != self._grid_n:
            for p in self._atom_patches:
                p.remove()
            self._atom_patches.clear()

            cols = max(1, int(np.ceil(np.sqrt(nd))))
            rows = max(1, int(np.ceil(nd / cols)))
            self._grid_cols = cols

            sz, gap = 0.72, 0.28          # square size + gap between them
            cell = sz + gap

            for i in range(nd):
                c = i % cols
                r = i // cols
                patch = Rectangle(
                    (c * cell, (rows - 1 - r) * cell),
                    sz, sz,
                    color=T["active_color"],
                    linewidth=0,
                )
                self.ax_atoms.add_patch(patch)
                self._atom_patches.append(patch)

            cols_w = cols * cell
            rows_h = rows * cell
            self.ax_atoms.set_xlim(-gap, cols_w)
            self.ax_atoms.set_ylim(-gap, rows_h)
            self._grid_n = nd

            label = (f"Atom Grid  (showing {nd}"
                     + (f" of {total}" if total > MAX_GRID_DISPLAY else "")
                     + ")")
            self.ax_atoms.set_title(label, color=T["title_color"],
                                     fontsize=9, pad=4)

        # update colours only
        ac = T["active_color"]
        dc = T["decay_color"]
        for patch, alive in zip(self._atom_patches, disp):
            patch.set_color(ac if alive else dc)


def build_figure(theme: dict):
    """Create figure + gridspec layout; return (fig, axes-tuple)."""
    plt.style.use("dark_background")
    fig = plt.figure(figsize=FIGURE_SIZE)
    fig.patch.set_facecolor(theme["fig_bg"])
    fig.suptitle(
        "Radioactive Decay Simulator",
        fontsize=16, fontweight="bold",
        color=theme["title_color"], y=0.97,
    )

    gs = fig.add_gridspec(6, 4, **GRIDSPEC_ARGS)

    ax_timeline = fig.add_subplot(gs[0:3, 0:3])
    ax_stats    = fig.add_subplot(gs[0:3, 3])
    ax_atoms    = fig.add_subplot(gs[3:6, 0:3])
    ax_bar      = fig.add_subplot(gs[3:6, 3])

    return fig, (ax_timeline, ax_stats, ax_atoms, ax_bar)
