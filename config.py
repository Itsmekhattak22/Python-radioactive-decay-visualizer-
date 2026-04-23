# ============================================================
#  config.py  –  Radioactive Decay Simulator
#  All constants, default values, and colour themes live here.
# ============================================================

# ── Simulation defaults ──────────────────────────────────────
DEFAULT_ATOMS    = 500
DEFAULT_HALFLIFE = 10
DEFAULT_DURATION = 50

ATOM_MIN,     ATOM_MAX     = 1,   2500
HALFLIFE_MIN, HALFLIFE_MAX = 1,   100
DURATION_MIN, DURATION_MAX = 1,   500

ANIMATION_INTERVAL_MS = 100   # milliseconds per frame
MAX_GRID_DISPLAY      = 1600  # max atoms rendered in grid

# ── Figure geometry ──────────────────────────────────────────
FIGURE_SIZE   = (10, 6)
GRIDSPEC_ARGS = dict(
    hspace = 2.5,
    wspace = 0.3,
    left   = 0.05,
    right  = 0.98,
    top    = 0.88,
    bottom = 0.18,
)

# ── Colour themes ────────────────────────────────────────────
THEMES = {
    # Option A – Neon Science  (default)
    "neon": dict(
        fig_bg       = "#0a0e1a",
        axes_bg      = "#0d1220",
        title_color  = "#00e5ff",
        text_color   = "#e0f7fa",
        grid_alpha   = 0.12,
        active_color = "#00e5ff",
        decay_color  = "#ff1744",
        accent_color = "#d500f9",
        bar_active   = "#00e5ff",
        bar_decay    = "#ff1744",
        stats_face   = "#111c3a",
        stats_edge   = "#00e5ff",
        btn_start    = ("#004d1a", "#00c853"),
        btn_pause    = ("#4a3000", "#ff6d00"),
        btn_reset    = ("#4a0000", "#d50000"),
        textbox_bg   = "#0d1a3a",
        textbox_hover= "#1a2a50",
        label_color  = "#90caf9",
    ),
    # Option B – Clean Laboratory
    "lab": dict(
        fig_bg       = "#f4f6f8",
        axes_bg      = "#ffffff",
        title_color  = "#1a237e",
        text_color   = "#212121",
        grid_alpha   = 0.20,
        active_color = "#00695c",
        decay_color  = "#b71c1c",
        accent_color = "#1565c0",
        bar_active   = "#00897b",
        bar_decay    = "#e53935",
        stats_face   = "#e8eaf6",
        stats_edge   = "#3949ab",
        btn_start    = ("#c8e6c9", "#388e3c"),
        btn_pause    = ("#fff3e0", "#f57c00"),
        btn_reset    = ("#ffcdd2", "#c62828"),
        textbox_bg   = "#e3f2fd",
        textbox_hover= "#bbdefb",
        label_color  = "#37474f",
    ),
}

ACTIVE_THEME = "neon"   # change to "lab" for the light theme


def get_theme() -> dict:
    return THEMES[ACTIVE_THEME]
