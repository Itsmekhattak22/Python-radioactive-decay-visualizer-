#!/usr/bin/env python3
# ============================================================
#  main.py  –  Entry point for Radioactive Decay Simulator
# ============================================================

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from config      import ANIMATION_INTERVAL_MS, get_theme
from simulator   import DecaySimulator
from visualizer  import DecayVisualizer, build_figure
from ui_controls import UIControls


class SimulatorApp:
    """
    Top-level controller.
    Owns the simulator, visualizer, and UI; drives the animation loop.
    """

    def __init__(self) -> None:
        self.sim = DecaySimulator()
        self.viz = DecayVisualizer()

        theme = get_theme()
        fig, (ax_tl, ax_st, ax_at, ax_bar) = build_figure(theme)
        self.fig = fig

        self.viz.setup(fig, ax_tl, ax_st, ax_at, ax_bar)
        self.controls = UIControls(fig, self)

        # initial (empty) render
        self.viz.update(self.sim)

    def _animate(self, _frame) -> list:
        if self.sim.is_running and not self.sim.is_paused:
            self.sim.step()
            self.viz.update(self.sim)
        return []

    def run(self) -> None:
        # keep a reference so the animation isn't garbage-collected
        self._anim = animation.FuncAnimation(
            self.fig,
            self._animate,
            interval=ANIMATION_INTERVAL_MS,
            blit=False,
            cache_frame_data=False,
        )
        plt.show()


if __name__ == "__main__":
    SimulatorApp().run()
