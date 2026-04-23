# ============================================================
#  ui_controls.py  –  All matplotlib widget wiring
# ============================================================

import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
from config import get_theme


class UIControls:
    """
    Creates and wires the three buttons and three text inputs.
    Callbacks receive a reference to the SimulatorApp controller.
    """

    def __init__(self, fig, app) -> None:
        self.fig = fig
        self.app = app
        T = get_theme()

        # ── Row geometry ──────────────────────────────────────
        # controls sit below the gridspec bottom (0.18 → 0.06 band)
        y, h = 0.055, 0.05

        # ── Text boxes ────────────────────────────────────────
        ax_atoms    = fig.add_axes([0.05, y, 0.09, h])
        ax_halflife = fig.add_axes([0.23, y, 0.09, h])
        ax_duration = fig.add_axes([0.41, y, 0.09, h])

        self.tb_atoms = TextBox(
            ax_atoms, "Atoms ",
            initial=str(app.sim.initial_atoms),
            color=T["textbox_bg"], hovercolor=T["textbox_hover"],
        )
        self.tb_halflife = TextBox(
            ax_halflife, "Half-Life ",
            initial=str(app.sim.half_life),
            color=T["textbox_bg"], hovercolor=T["textbox_hover"],
        )
        self.tb_duration = TextBox(
            ax_duration, "Duration ",
            initial=str(app.sim.duration),
            color=T["textbox_bg"], hovercolor=T["textbox_hover"],
        )

        # style labels
        for tb in (self.tb_atoms, self.tb_halflife, self.tb_duration):
            tb.label.set_color(T["label_color"])
            tb.label.set_fontsize(8)
            tb.text_disp.set_color(T["text_color"])
            tb.text_disp.set_fontsize(8)

        # ── Buttons ───────────────────────────────────────────
        ax_start = fig.add_axes([0.60, y, 0.11, h])
        ax_pause = fig.add_axes([0.73, y, 0.11, h])
        ax_reset = fig.add_axes([0.86, y, 0.11, h])

        sc, sh = T["btn_start"]
        pc, ph = T["btn_pause"]
        rc, rh = T["btn_reset"]

        self.btn_start = Button(ax_start, "▶  Start", color=sc, hovercolor=sh)
        self.btn_pause = Button(ax_pause, "||  Pause", color=pc, hovercolor=ph)
        self.btn_reset = Button(ax_reset, "↺  Reset", color=rc, hovercolor=rh)

        for btn in (self.btn_start, self.btn_pause, self.btn_reset):
            btn.label.set_fontsize(8)
            btn.label.set_color(T["text_color"])

        # ── Wire events ───────────────────────────────────────
        self.btn_start.on_clicked(self._on_start)
        self.btn_pause.on_clicked(self._on_pause)
        self.btn_reset.on_clicked(self._on_reset)
        self.tb_atoms.on_submit(self._on_atoms)
        self.tb_halflife.on_submit(self._on_halflife)
        self.tb_duration.on_submit(self._on_duration)

    # ── handlers ─────────────────────────────────────────────

    def _on_start(self, _event) -> None:
        if self.app.sim.finished:
            self.app.sim.reset()
        self.app.sim.is_running = True
        self.app.sim.is_paused  = False

    def _on_pause(self, _event) -> None:
        self.app.sim.is_paused = not self.app.sim.is_paused

    def _on_reset(self, _event) -> None:
        self.app.sim.reset()
        self.app.viz.update(self.app.sim)
        plt.draw()

    def _on_atoms(self, text: str) -> None:
        try:
            v = self.app.sim.set_atoms(int(text))
        except ValueError:
            v = self.app.sim.initial_atoms
        self.tb_atoms.set_val(str(v))

    def _on_halflife(self, text: str) -> None:
        try:
            v = self.app.sim.set_half_life(int(text))
        except ValueError:
            v = self.app.sim.half_life
        self.tb_halflife.set_val(str(v))

    def _on_duration(self, text: str) -> None:
        try:
            v = self.app.sim.set_duration(int(text))
        except ValueError:
            v = self.app.sim.duration
        self.tb_duration.set_val(str(v))
