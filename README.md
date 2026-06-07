# Hybrid 5G Scheduler Algorithm

This project simulates how a 5G base station allocates **Resource Blocks (RBs)** to multiple users and compares two common scheduling strategies:

- **Round Robin (RR)** – gives turns to users in sequence
- **Proportional Fair (PF)** – balances fairness and throughput using user channel quality + throughput history

The simulation runs for multiple **TTIs (Transmission Time Intervals)**, stores results, and generates comparison plots.

---

## What this project demonstrates

- How scheduler choice changes total system throughput
- How fairly users are treated over time (Jain’s fairness index)
- How CQI (channel quality) impacts per-user data rates
- Trade-off between maximum throughput and balanced allocation

---

## Key features

- RR and PF scheduler implementations
- CQI-based throughput modelling with optional dynamic channel variation
- Per-TTI and summary CSV export
- Auto-generated visualizations (throughput, fairness, heatmaps, summary charts)
- Config-driven simulation settings (`config.py`)

---

## Requirements

- Python 3.10.x (project dependencies are pinned for this version)
- `numpy`, `pandas`, `matplotlib`, `seaborn`

Install dependencies:

```bash
pip install -r requirements.txt
```

If you are using a newer Python version and pinned installs fail, install compatible latest packages manually:

```bash
pip install numpy pandas matplotlib seaborn
```

---

## Quick start

Run the simulation:

```bash
python main.py
```

Run tests:

```bash
python test_simulation.py
```

---

## Configuration

All simulation parameters are in `/tmp/workspace/SUBHAM-RAJ-01/Hybrid-5G-Scheduler-Algorithm-/config.py`.

Useful settings:

- `NUM_USERS`, `NUM_RBS`, `NUM_TTIS`
- `DYNAMIC_CHANNEL`, `CQI_CHANGE_PROBABILITY`
- `MIN_CQI`, `MAX_CQI`
- `PF_ALPHA` (PF smoothing factor)

You can switch between small/large presets by uncommenting preset blocks at the bottom of `config.py`.

---

## Output

After each run:

- `results/`
  - `round_robin_tti_results.csv`
  - `proportional_fair_tti_results.csv`
  - scheduler summary CSV files
- `plots/`
  - throughput comparison
  - fairness comparison
  - RB allocation heatmaps
  - summary metric charts

Output files are overwritten on each run so you always see the latest experiment results.

---

## Project structure

```
Hybrid-5G-Scheduler-Algorithm-/
├── main.py              # Entry point
├── scheduler.py         # Round Robin + Proportional Fair logic
├── system.py            # Core simulation engine
├── user.py              # User model (CQI, throughput tracking)
├── config.py            # All tunable parameters
├── visualizer.py        # Plot generation
├── test_simulation.py   # Test suite
├── results/             # Generated CSV outputs
└── plots/               # Generated figures
```
