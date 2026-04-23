# ☢️ Radioactive Decay Simulator

> *Every atom holds its breath — until it doesn't.*

A real-time, interactive visualisation of stochastic radioactive decay built with Python and Matplotlib.
Watch hundreds of atoms decay step-by-step, explore the relationship between half-life and exponential loss, and tweak parameters on the fly.

---

## ✨ Features

| Feature                   | Detail                                                                             |
| ------------------------- | ---------------------------------------------------------------------------------- |
| **Live atom grid**        | Up to 1,600 atoms rendered as colour-coded squares (cyan = active, red = decayed)  |
| **Decay timeline**        | Real-time dual-line chart tracking active and decayed populations                  |
| **Statistics panel**      | Step counter, live counts, and decay percentage                                    |
| **Adjustable parameters** | Atoms (1–2,500), Half-Life (1–100 steps), Duration (1–500 steps)                   |
| **Pause / Resume**        | Freeze the simulation at any moment                                                |
| **Two colour themes**     | *Neon Science* (dark) and *Clean Laboratory* (light) — configurable in `config.py` |
| **Fast rendering**        | Persistent matplotlib artists — **no full redraw per frame**                       |

---

## 🧠 Physics Behind the Simulation

This simulation uses the **exponential decay law**:

[
P = 1 - e^{-\lambda \Delta t}
]

Where:

* (\lambda = \frac{\ln(2)}{T_{1/2}})
* (\Delta t = \frac{T_{1/2}}{50})

Each atom has a random chance to decay during every time step based on this probability.

---

## 🛠 Tech Stack

* **Python 3.10+**
* **Matplotlib 3.7+** — figures, animation, widgets
* **NumPy 1.24+** — grid geometry helpers
* **Pure-Python** linked list for decay history

---

## 📁 Project Structure

```bash
radioactive_decay/
├── main.py          # Entry point — wires all modules together
├── simulator.py     # Core physics & stochastic decay logic
├── visualizer.py    # Matplotlib figure, panels, persistent artists
├── ui_controls.py   # Buttons, text inputs, event callbacks
├── linked_list.py   # Custom singly-linked list for decay history
├── config.py        # Constants, layout geometry, colour themes
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/your-username/radioactive-decay-simulator.git

# 2. Navigate into the project
cd radioactive-decay-simulator

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the simulator
python main.py
```

> Tested on Python 3.10 – 3.12 (Windows, macOS, Linux)

---

## 🔭 Future Improvements

1. **Real-time parameter sliders** — adjust half-life and atom count dynamically
2. **Isotope selection system** — presets like C-14, U-238, Ra-226
3. **Daughter product chains** — multi-stage decay simulations
4. **CSV export** — save timeline data for analysis
5. **Batch statistics mode** — run multiple simulations and compute averages

---

## 📄 License

MIT © 2025 — see [LICENSE](LICENSE) for details.

---

## 👩‍💻 Author

**Emman Khattak**
Software Engineering Student @ NUST
Physics + Programming Enthusiast 💻⚛️
