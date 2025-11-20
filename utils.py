"""
Utility functions for CQI mapping, metrics calculation, and helper operations.
"""

import numpy as np

# CQI to throughput mapping (Mbps per RB)
# Based on 3GPP specifications - simplified mapping
CQI_TO_THROUGHPUT = {
    1: 0.15,   # Very poor channel
    2: 0.23,
    3: 0.38,
    4: 0.60,
    5: 0.88,
    6: 1.18,
    7: 1.48,
    8: 1.91,
    9: 2.41,
    10: 2.73,
    11: 3.32,
    12: 3.90,
    13: 4.52,
    14: 5.12,
    15: 5.55   # Excellent channel
}


def get_throughput_from_cqi(cqi):
    """
    Get achievable throughput (Mbps) for a given CQI value.
    
    Args:
        cqi: Channel Quality Indicator (1-15)
        
    Returns:
        Throughput in Mbps per Resource Block
    """
    return CQI_TO_THROUGHPUT.get(cqi, 1.0)


def calculate_jains_fairness_index(throughputs):
    """
    Calculate Jain's Fairness Index.
    
    JFI = (sum of throughputs)^2 / (n * sum of throughputs^2)
    
    Range: [1/n, 1] where 1 means perfect fairness
    
    Args:
        throughputs: List or array of user throughputs
        
    Returns:
        Jain's Fairness Index (0 to 1)
    """
    throughputs = np.array(throughputs)
    n = len(throughputs)
    
    if n == 0 or np.sum(throughputs) == 0:
        return 0.0
    
    numerator = np.sum(throughputs) ** 2
    denominator = n * np.sum(throughputs ** 2)
    
    return numerator / denominator if denominator > 0 else 0.0


def generate_random_cqi(num_users, min_cqi=1, max_cqi=15):
    """
    Generate random CQI values for users.
    
    Args:
        num_users: Number of users
        min_cqi: Minimum CQI value
        max_cqi: Maximum CQI value
        
    Returns:
        List of CQI values
    """
    return np.random.randint(min_cqi, max_cqi + 1, size=num_users).tolist()


def update_cqi_dynamic(current_cqi, change_probability=0.1, max_change=2):
    """
    Simulate dynamic channel conditions by randomly changing CQI.
    
    Args:
        current_cqi: Current CQI value
        change_probability: Probability of CQI change
        max_change: Maximum CQI change per update
        
    Returns:
        New CQI value (1-15)
    """
    if np.random.random() < change_probability:
        change = np.random.randint(-max_change, max_change + 1)
        new_cqi = current_cqi + change
        return max(1, min(15, new_cqi))
    return current_cqi


def calculate_spectral_efficiency(total_throughput, num_rbs, bandwidth_per_rb=180):
    """
    Calculate spectral efficiency (bps/Hz).
    
    Args:
        total_throughput: Total throughput in Mbps
        num_rbs: Number of resource blocks
        bandwidth_per_rb: Bandwidth per RB in kHz (default 180 kHz for 5G)
        
    Returns:
        Spectral efficiency in bps/Hz
    """
    total_bandwidth_mhz = (num_rbs * bandwidth_per_rb) / 1000.0
    if total_bandwidth_mhz == 0:
        return 0.0
    
    # Convert Mbps to bps and MHz to Hz
    return (total_throughput * 1e6) / (total_bandwidth_mhz * 1e6)
