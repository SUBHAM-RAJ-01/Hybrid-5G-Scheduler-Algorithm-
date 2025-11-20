"""
Visualization functions for comparing scheduler performance.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Try to import seaborn, but don't fail if not available
try:
    import seaborn as sns
    sns.set_style("whitegrid")
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False


def create_output_dirs():
    """Create output directories for plots."""
    os.makedirs('plots', exist_ok=True)
    os.makedirs('results', exist_ok=True)


def plot_throughput_comparison(rr_summary, pf_summary, num_users):
    """
    Plot per-user average throughput comparison between RR and PF.
    
    Args:
        rr_summary: Summary statistics from Round Robin scheduler
        pf_summary: Summary statistics from Proportional Fair scheduler
        num_users: Number of users
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    user_ids = list(range(num_users))
    x = np.arange(num_users)
    width = 0.35
    
    rr_throughputs = rr_summary['user_avg_throughput']
    pf_throughputs = pf_summary['user_avg_throughput']
    
    bars1 = ax.bar(x - width/2, rr_throughputs, width, label='Round Robin', alpha=0.8, color='skyblue')
    bars2 = ax.bar(x + width/2, pf_throughputs, width, label='Proportional Fair', alpha=0.8, color='salmon')
    
    ax.set_xlabel('User ID', fontsize=12)
    ax.set_ylabel('Average Throughput (Mbps)', fontsize=12)
    ax.set_title('Per-User Average Throughput: Round Robin vs Proportional Fair', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(user_ids)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/throughput_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_system_throughput_over_time(rr_results, pf_results, window=50):
    """
    Plot total system throughput over time for both schedulers.
    
    Args:
        rr_results: TTI results from Round Robin scheduler
        pf_results: TTI results from Proportional Fair scheduler
        window: Moving average window size
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    rr_throughputs = [tti['total_throughput'] for tti in rr_results]
    pf_throughputs = [tti['total_throughput'] for tti in pf_results]
    
    # Calculate moving average for smoother visualization
    rr_ma = np.convolve(rr_throughputs, np.ones(window)/window, mode='valid')
    pf_ma = np.convolve(pf_throughputs, np.ones(window)/window, mode='valid')
    
    ttis_rr = list(range(len(rr_ma)))
    ttis_pf = list(range(len(pf_ma)))
    
    ax.plot(ttis_rr, rr_ma, label='Round Robin', linewidth=2, alpha=0.8, color='blue')
    ax.plot(ttis_pf, pf_ma, label='Proportional Fair', linewidth=2, alpha=0.8, color='red')
    
    ax.set_xlabel('TTI (Transmission Time Interval)', fontsize=12)
    ax.set_ylabel('Total System Throughput (Mbps)', fontsize=12)
    ax.set_title(f'System Throughput Over Time (Moving Avg, window={window})', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/system_throughput_over_time.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_fairness_comparison(rr_results, pf_results):
    """
    Plot Jain's Fairness Index over time for both schedulers.
    
    Args:
        rr_results: TTI results from Round Robin scheduler
        pf_results: TTI results from Proportional Fair scheduler
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    rr_fairness = [tti['fairness_index'] for tti in rr_results]
    pf_fairness = [tti['fairness_index'] for tti in pf_results]
    
    window = 50
    rr_ma = np.convolve(rr_fairness, np.ones(window)/window, mode='valid')
    pf_ma = np.convolve(pf_fairness, np.ones(window)/window, mode='valid')
    
    ttis = list(range(len(rr_ma)))
    
    ax.plot(ttis, rr_ma, label='Round Robin', linewidth=2, alpha=0.8, color='green')
    ax.plot(ttis, pf_ma, label='Proportional Fair', linewidth=2, alpha=0.8, color='orange')
    
    ax.set_xlabel('TTI (Transmission Time Interval)', fontsize=12)
    ax.set_ylabel("Jain's Fairness Index", fontsize=12)
    ax.set_title("Fairness Comparison Over Time (Moving Avg)", fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    ax.set_ylim([0, 1.05])
    
    plt.tight_layout()
    plt.savefig('plots/fairness_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_rb_allocation_heatmap(results, scheduler_name, num_users, sample_ttis=100):
    """
    Plot heatmap showing RB allocation pattern across users and TTIs.
    
    Args:
        results: TTI results from scheduler
        scheduler_name: Name of the scheduler
        num_users: Number of users
        sample_ttis: Number of TTIs to sample for visualization
    """
    # Sample TTIs for visualization (to avoid overcrowding)
    step = max(1, len(results) // sample_ttis)
    sampled_results = results[::step][:sample_ttis]
    
    # Create allocation matrix: rows=TTIs, cols=Users
    allocation_matrix = np.zeros((len(sampled_results), num_users))
    
    for i, tti_data in enumerate(sampled_results):
        rb_counts = tti_data['user_rb_counts']
        allocation_matrix[i, :] = rb_counts
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    if SEABORN_AVAILABLE:
        sns.heatmap(allocation_matrix.T, cmap='YlOrRd', cbar_kws={'label': 'RBs Allocated'},
                    xticklabels=False, yticklabels=list(range(num_users)), ax=ax)
    else:
        im = ax.imshow(allocation_matrix.T, cmap='YlOrRd', aspect='auto', interpolation='nearest')
        cbar = plt.colorbar(im, ax=ax, label='RBs Allocated')
        ax.set_yticks(range(num_users))
        ax.set_yticklabels(range(num_users))
    
    ax.set_xlabel('TTI (sampled)', fontsize=12)
    ax.set_ylabel('User ID', fontsize=12)
    ax.set_title(f'RB Allocation Pattern: {scheduler_name}', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    filename = f'plots/rb_allocation_heatmap_{scheduler_name.lower().replace(" ", "_")}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()


def plot_summary_metrics(rr_summary, pf_summary):
    """
    Plot summary comparison of key metrics between schedulers.
    
    Args:
        rr_summary: Summary statistics from Round Robin scheduler
        pf_summary: Summary statistics from Proportional Fair scheduler
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Total System Throughput
    ax = axes[0, 0]
    schedulers = ['Round Robin', 'Proportional Fair']
    throughputs = [rr_summary['total_system_throughput'], pf_summary['total_system_throughput']]
    bars = ax.bar(schedulers, throughputs, color=['skyblue', 'salmon'], alpha=0.8)
    ax.set_ylabel('Total Throughput (Mbps)', fontsize=11)
    ax.set_title('Total System Throughput', fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontsize=10)
    
    # 2. Average Fairness Index
    ax = axes[0, 1]
    fairness = [rr_summary['avg_fairness_index'], pf_summary['avg_fairness_index']]
    bars = ax.bar(schedulers, fairness, color=['green', 'orange'], alpha=0.8)
    ax.set_ylabel("Jain's Fairness Index", fontsize=11)
    ax.set_title('Average Fairness Index', fontsize=12, fontweight='bold')
    ax.set_ylim([0, 1.05])
    ax.grid(axis='y', alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}', ha='center', va='bottom', fontsize=10)
    
    # 3. RB Utilization
    ax = axes[1, 0]
    utilization = [rr_summary['rb_utilization_percent'], pf_summary['rb_utilization_percent']]
    bars = ax.bar(schedulers, utilization, color=['purple', 'teal'], alpha=0.8)
    ax.set_ylabel('RB Utilization (%)', fontsize=11)
    ax.set_title('Resource Block Utilization', fontsize=12, fontweight='bold')
    ax.set_ylim([0, 105])
    ax.grid(axis='y', alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=10)
    
    # 4. Average Throughput per User
    ax = axes[1, 1]
    avg_tput = [rr_summary['avg_system_throughput'], pf_summary['avg_system_throughput']]
    bars = ax.bar(schedulers, avg_tput, color=['coral', 'lightblue'], alpha=0.8)
    ax.set_ylabel('Avg Throughput (Mbps/TTI)', fontsize=11)
    ax.set_title('Average System Throughput per TTI', fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', fontsize=10)
    
    plt.suptitle('Scheduler Performance Comparison', fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig('plots/summary_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()


def generate_all_plots(rr_results, pf_results, rr_summary, pf_summary, num_users):
    """
    Generate all visualization plots.
    
    Args:
        rr_results: TTI results from Round Robin scheduler
        pf_results: TTI results from Proportional Fair scheduler
        rr_summary: Summary statistics from Round Robin scheduler
        pf_summary: Summary statistics from Proportional Fair scheduler
        num_users: Number of users
    """
    print("\nGenerating visualizations...", end='')
    
    create_output_dirs()
    
    plot_throughput_comparison(rr_summary, pf_summary, num_users)
    plot_system_throughput_over_time(rr_results, pf_results)
    plot_fairness_comparison(rr_results, pf_results)
    plot_rb_allocation_heatmap(rr_results, "Round Robin", num_users)
    plot_rb_allocation_heatmap(pf_results, "Proportional Fair", num_users)
    plot_summary_metrics(rr_summary, pf_summary)
    
    print(" Done ✓")
