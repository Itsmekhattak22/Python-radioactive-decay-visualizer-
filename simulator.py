# ============================================================
#  simulator.py  –  Core physics and decay logic
#  No matplotlib imports – pure data model.
# ============================================================

import random
from linked_list import DecayList
from config import (
    DEFAULT_ATOMS, DEFAULT_HALFLIFE, DEFAULT_DURATION,
    ATOM_MIN, ATOM_MAX, HALFLIFE_MIN, HALFLIFE_MAX,
    DURATION_MIN, DURATION_MAX,
)


class DecaySimulator:
    """
    Simulates stochastic radioactive decay.

    Each time-step every surviving atom decays with probability
        p = 1 − 0.5^(1 / half_life)
    derived from the continuous exponential-decay law
        N(t) = N₀ · e^(−λt),  λ = ln2 / T½
    """

    def __init__(
        self,
        initial_atoms: int = DEFAULT_ATOMS,
        half_life:     int = DEFAULT_HALFLIFE,
        duration:      int = DEFAULT_DURATION,
    ) -> None:
        self.initial_atoms = initial_atoms
        self.half_life     = half_life
        self.duration      = duration

        # runtime state
        self.atom_states:  list[bool] = []
        self.decay_list:   DecayList  = DecayList()
        self.timeline:     dict       = {}
        self.current_step: int        = 0
        self.is_running:   bool       = False
        self.is_paused:    bool       = False

        self.reset()

    # ── public API ───────────────────────────────────────────

    def reset(self) -> None:
        self.atom_states  = [True] * self.initial_atoms
        self.decay_list.clear()
        self.timeline = {
            "steps":     [0],
            "remaining": [self.initial_atoms],
            "decayed":   [0],
        }
        self.current_step = 0
        self.is_running   = False
        self.is_paused    = False

    def step(self) -> None:
        """Advance one time-unit; no-op if finished."""
        if self.current_step >= self.duration:
            self.is_running = False
            return

        p = self._decay_probability()
        for idx, alive in enumerate(self.atom_states):
            if alive and random.random() < p:
                self.atom_states[idx] = False
                self.decay_list.append(idx, self.current_step + 1)

        self.current_step += 1
        remaining = sum(self.atom_states)
        self.timeline["steps"].append(self.current_step)
        self.timeline["remaining"].append(remaining)
        self.timeline["decayed"].append(self.initial_atoms - remaining)

    @property
    def remaining(self) -> int:
        return self.timeline["remaining"][-1]

    @property
    def decayed(self) -> int:
        return self.timeline["decayed"][-1]

    @property
    def finished(self) -> bool:
        return self.current_step >= self.duration

    # ── parameter setters (with clamping) ────────────────────

    def set_atoms(self, value: int) -> int:
        self.initial_atoms = max(ATOM_MIN, min(ATOM_MAX, value))
        return self.initial_atoms

    def set_half_life(self, value: int) -> int:
        self.half_life = max(HALFLIFE_MIN, min(HALFLIFE_MAX, value))
        return self.half_life

    def set_duration(self, value: int) -> int:
        self.duration = max(DURATION_MIN, min(DURATION_MAX, value))
        return self.duration

    # ── internal ─────────────────────────────────────────────

    def _decay_probability(self) -> float:
        return 1.0 - 0.5 ** (1.0 / self.half_life)
