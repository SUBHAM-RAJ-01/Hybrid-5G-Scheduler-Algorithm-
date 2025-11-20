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

```bash
pip install numpy pandas matplotlib seaborn
```

## Usage

```bash
python main.py
```

## Project Structure

- `main.py` - Entry point for running simulations
- `user.py` - User class with CQI and throughput tracking
- `scheduler.py` - Base scheduler and RR/PF implementations
- `system.py` - 5G system simulation engine
- `utils.py` - Helper functions for metrics and CQI mapping
- `visualizer.py` - Plotting and visualization functions
- `Explain.txt` - Detailed explanation of concepts and methodology
- `Mermaid_Diagrams.md` - Mermaid code for presentation diagrams

## Output

- CSV files with simulation results in `results/` folder
- Visualization plots in `plots/` folder
- Console logs showing simulation progress
