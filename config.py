"""
Configuration file for 5G Scheduler Simulation.

Modify these parameters to customize the simulation without editing main.py.
"""

# ============================================================================
# SIMULATION PARAMETERS
# ============================================================================

# Number of users in the simulation
NUM_USERS = 10

# Number of Resource Blocks available per TTI
NUM_RBS = 50

# Number of Transmission Time Intervals to simulate
NUM_TTIS = 1000

# Enable dynamic channel conditions (CQI changes over time)
DYNAMIC_CHANNEL = True

# Random seed for reproducibility (set to None for random behavior)
RANDOM_SEED = 42

# ============================================================================
# CHANNEL PARAMETERS
# ============================================================================

# Minimum CQI value for user initialization (1-15)
MIN_CQI = 3

# Maximum CQI value for user initialization (1-15)
MAX_CQI = 15

# Probability of CQI change per TTI (0.0 to 1.0)
CQI_CHANGE_PROBABILITY = 0.1

# Maximum CQI change per update
MAX_CQI_CHANGE = 2

# ============================================================================
# SCHEDULER PARAMETERS
# ============================================================================

# Proportional Fair alpha (smoothing factor for average throughput)
# Smaller values = more weight on history
# Larger values = more weight on recent allocations
PF_ALPHA = 0.01

# ============================================================================
# OUTPUT PARAMETERS
# ============================================================================

# Directory for CSV results
RESULTS_DIR = 'results'

# Directory for visualization plots
PLOTS_DIR = 'plots'

# Logging interval (print progress every N TTIs)
LOG_INTERVAL = 100

# Number of TTIs to sample for heatmap visualization
HEATMAP_SAMPLE_TTIS = 100

# Moving average window for throughput plots
MOVING_AVERAGE_WINDOW = 50

# ============================================================================
# VISUALIZATION PARAMETERS
# ============================================================================

# DPI for saved plots (higher = better quality, larger file size)
PLOT_DPI = 300

# Figure size for plots (width, height in inches)
FIGURE_SIZE_LARGE = (14, 6)
FIGURE_SIZE_MEDIUM = (12, 6)
FIGURE_SIZE_SMALL = (10, 5)

# Enable/disable specific plots
ENABLE_THROUGHPUT_COMPARISON = True
ENABLE_SYSTEM_THROUGHPUT_PLOT = True
ENABLE_FAIRNESS_PLOT = True
ENABLE_HEATMAPS = True
ENABLE_SUMMARY_METRICS = True

# ============================================================================
# ADVANCED PARAMETERS
# ============================================================================

# Bandwidth per Resource Block in kHz (for spectral efficiency calculation)
BANDWIDTH_PER_RB = 180

# Initial average throughput for users (to avoid division by zero in PF)
INITIAL_AVG_THROUGHPUT = 0.1

# ============================================================================
# PRESET CONFIGURATIONS
# ============================================================================

# Uncomment one of these to use preset configurations

# # Small Test Configuration (fast execution)
# NUM_USERS = 5
# NUM_RBS = 25
# NUM_TTIS = 100
# LOG_INTERVAL = 20

# # Large Scale Configuration (detailed analysis)
# NUM_USERS = 20
# NUM_RBS = 100
# NUM_TTIS = 5000
# LOG_INTERVAL = 500

# # Static Channel Configuration (no CQI variation)
# DYNAMIC_CHANNEL = False
# CQI_CHANGE_PROBABILITY = 0.0

# # High Mobility Configuration (frequent CQI changes)
# DYNAMIC_CHANNEL = True
# CQI_CHANGE_PROBABILITY = 0.3
# MAX_CQI_CHANGE = 3

# # Poor Channel Configuration (low CQI values)
# MIN_CQI = 1
# MAX_CQI = 8

# # Excellent Channel Configuration (high CQI values)
# MIN_CQI = 10
# MAX_CQI = 15
