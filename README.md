# 5G Scheduler Simulation: Round Robin vs Proportional Fair

A Python 3.10.7-compatible simulation project that models how a 5G base station schedules Resource Blocks (RBs) among multiple users using Round Robin and Proportional Fair scheduling algorithms.

## Features

- **Two Scheduling Algorithms**: Round Robin (RR) and Proportional Fair (PF)
- **Realistic 5G Modeling**: CQI-based throughput mapping, multiple users, configurable RBs
- **Comprehensive Metrics**: Per-user throughput, system throughput, fairness index, RB utilization
- **Data Export**: All results saved to CSV files using pandas
- **Visualizations**: Line plots, bar charts, and heatmaps comparing schedulers

## Requirements

- Python 3.10.7
- NumPy
- Pandas
- Matplotlib
- Seaborn (optional)

## Installation

Install required packages:
```bash
pip install numpy pandas matplotlib seaborn
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

## Usage

### Run Simulation
```bash
# Use your system's Python (adjust path as needed)
python main.py

# Or if you have multiple Python versions:
C:\Users\YourUsername\AppData\Local\Programs\Python\Python312\python.exe main.py
```

### Run Tests (Optional)
```bash
python test_simulation.py
```

### Customize Parameters
Edit `config.py` to change simulation parameters without modifying code.

## Project Structure

```
5G-Scheduler-Simulation/
├── main.py              # Entry point - run this
├── user.py              # User class with CQI tracking
├── scheduler.py         # RR and PF implementations
├── system.py            # Simulation engine
├── utils.py             # Helper functions
├── visualizer.py        # Plotting functions
├── config.py            # Configuration parameters
├── test_simulation.py   # Unit tests
├── requirements.txt     # Dependencies
├── README.md            # This file
├── Explain.txt          # Detailed concept explanations
├── Mermaid_Diagrams.md  # Flow diagrams for presentations
├── results/             # CSV output (auto-generated)
└── plots/               # Visualization output (auto-generated)
```

## Output

- **CSV files**: `results/` folder (per-TTI data and summaries)
- **Visualizations**: `plots/` folder (6 comparison charts)
- **Console**: Clean performance comparison

Files are automatically replaced on each run (no duplicates).
