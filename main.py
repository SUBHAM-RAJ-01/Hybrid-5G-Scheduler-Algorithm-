"""
Main entry point for 5G Scheduler Simulation.

Simulates Round Robin and Proportional Fair schedulers,
compares their performance, and generates visualizations.
"""

import numpy as np
import pandas as pd
from user import User
from scheduler import RoundRobinScheduler, ProportionalFairScheduler
from system import System
from utils import generate_random_cqi
from visualizer import generate_all_plots, create_output_dirs
import time
import config


def save_results_to_csv(results, summary, scheduler_name):
    """
    Save simulation results to CSV files.
    
    Args:
        results: List of TTI results
        summary: Summary statistics dictionary
        scheduler_name: Name of the scheduler
    """
    create_output_dirs()
    
    # Save per-TTI results
    tti_data = []
    for tti in results:
        row = {
            'TTI': tti['tti'],
            'Total_Throughput_Mbps': tti['total_throughput'],
            'Fairness_Index': tti['fairness_index']
        }
        # Add per-user throughput
        for user_id, tput in enumerate(tti['user_throughputs']):
            row[f'User_{user_id}_Throughput'] = tput
        # Add per-user RB count
        for user_id, rb_count in enumerate(tti['user_rb_counts']):
            row[f'User_{user_id}_RBs'] = rb_count
        
        tti_data.append(row)
    
    df_tti = pd.DataFrame(tti_data)
    filename = f'results/{scheduler_name.lower().replace(" ", "_")}_tti_results.csv'
    df_tti.to_csv(filename, index=False)
    
    # Save summary statistics
    summary_data = {
        'Metric': [
            'Total System Throughput (Mbps)',
            'Avg System Throughput (Mbps/TTI)',
            'Avg Fairness Index',
            'RB Utilization (%)'
        ],
        'Value': [
            summary['total_system_throughput'],
            summary['avg_system_throughput'],
            summary['avg_fairness_index'],
            summary['rb_utilization_percent']
        ]
    }
    
    # Add per-user metrics
    for user_id in range(len(summary['user_total_throughput'])):
        summary_data['Metric'].append(f'User {user_id} Total Throughput (Mbps)')
        summary_data['Value'].append(summary['user_total_throughput'][user_id])
    
    for user_id in range(len(summary['user_avg_throughput'])):
        summary_data['Metric'].append(f'User {user_id} Avg Throughput (Mbps/TTI)')
        summary_data['Value'].append(summary['user_avg_throughput'][user_id])
    
    df_summary = pd.DataFrame(summary_data)
    filename = f'results/{scheduler_name.lower().replace(" ", "_")}_summary.csv'
    df_summary.to_csv(filename, index=False)


def print_summary_comparison(rr_summary, pf_summary):
    """
    Print a formatted comparison of scheduler performance.
    
    Args:
        rr_summary: Round Robin summary statistics
        pf_summary: Proportional Fair summary statistics
    """
    print("\n" + "="*80)
    print("PERFORMANCE COMPARISON")
    print("="*80)
    
    print(f"\n{'Metric':<40} {'Round Robin':>18} {'Proportional Fair':>18}")
    print("-" * 80)
    
    print(f"{'Total System Throughput (Mbps)':<40} "
          f"{rr_summary['total_system_throughput']:>18.2f} "
          f"{pf_summary['total_system_throughput']:>18.2f}")
    
    print(f"{'Avg System Throughput (Mbps/TTI)':<40} "
          f"{rr_summary['avg_system_throughput']:>18.2f} "
          f"{pf_summary['avg_system_throughput']:>18.2f}")
    
    print(f"{'Avg Fairness Index':<40} "
          f"{rr_summary['avg_fairness_index']:>18.4f} "
          f"{pf_summary['avg_fairness_index']:>18.4f}")
    
    print(f"{'RB Utilization (%)':<40} "
          f"{rr_summary['rb_utilization_percent']:>18.2f} "
          f"{pf_summary['rb_utilization_percent']:>18.2f}")
    
    print("="*80)
    
    # Analysis
    print("\nKEY FINDINGS:")
    
    if pf_summary['total_system_throughput'] > rr_summary['total_system_throughput']:
        improvement = ((pf_summary['total_system_throughput'] - rr_summary['total_system_throughput']) 
                      / rr_summary['total_system_throughput'] * 100)
        print(f"  → PF achieves {improvement:.1f}% higher throughput")
    else:
        print(f"  → RR achieves higher throughput")
    
    if pf_summary['avg_fairness_index'] > rr_summary['avg_fairness_index']:
        print(f"  → PF provides better fairness ({pf_summary['avg_fairness_index']:.3f} vs {rr_summary['avg_fairness_index']:.3f})")
    else:
        print(f"  → RR provides better fairness ({rr_summary['avg_fairness_index']:.3f} vs {pf_summary['avg_fairness_index']:.3f})")
    
    print(f"  → Winner: {'Proportional Fair' if pf_summary['total_system_throughput'] > rr_summary['total_system_throughput'] else 'Round Robin'} (overall performance)")
    print("="*80)


def main():
    """Main simulation function."""
    
    # Load simulation parameters from config
    NUM_USERS = config.NUM_USERS
    NUM_RBS = config.NUM_RBS
    NUM_TTIS = config.NUM_TTIS
    DYNAMIC_CHANNEL = config.DYNAMIC_CHANNEL
    
    print("\n" + "="*80)
    print("5G SCHEDULER SIMULATION - Round Robin vs Proportional Fair")
    print("="*80)
    
    print(f"\nSimulation Configuration:")
    print(f"  • Number of Users: {NUM_USERS}")
    print(f"  • Resource Blocks: {NUM_RBS}")
    print(f"  • Transmission Time Intervals: {NUM_TTIS}")
    print(f"  • Dynamic Channel Conditions: {DYNAMIC_CHANNEL}")
    
    # Generate random CQI values for users
    if config.RANDOM_SEED is not None:
        np.random.seed(config.RANDOM_SEED)
    cqi_list = generate_random_cqi(NUM_USERS, min_cqi=config.MIN_CQI, max_cqi=config.MAX_CQI)
    
    print(f"\nInitial User CQI Values: {cqi_list}")
    
    # ========== Round Robin Simulation ==========
    print("\n[1/2] Running Round Robin Scheduler...")
    
    rr_scheduler = RoundRobinScheduler()
    rr_system = System(NUM_USERS, NUM_RBS, cqi_list.copy(), rr_scheduler)
    
    start_time = time.time()
    rr_results = rr_system.run_simulation(NUM_TTIS, dynamic_channel=DYNAMIC_CHANNEL)
    rr_time = time.time() - start_time
    
    rr_summary = rr_system.get_summary_statistics()
    print(f"      Completed in {rr_time:.2f}s | Throughput: {rr_summary['total_system_throughput']:.0f} Mbps")
    
    # ========== Proportional Fair Simulation ==========
    print("\n[2/2] Running Proportional Fair Scheduler...")
    
    pf_scheduler = ProportionalFairScheduler(alpha=config.PF_ALPHA)
    pf_system = System(NUM_USERS, NUM_RBS, cqi_list.copy(), pf_scheduler)
    
    start_time = time.time()
    pf_results = pf_system.run_simulation(NUM_TTIS, dynamic_channel=DYNAMIC_CHANNEL)
    pf_time = time.time() - start_time
    
    pf_summary = pf_system.get_summary_statistics()
    print(f"      Completed in {pf_time:.2f}s | Throughput: {pf_summary['total_system_throughput']:.0f} Mbps")
    
    # ========== Save Results ==========
    print("\nSaving results...")
    
    save_results_to_csv(rr_results, rr_summary, "Round_Robin")
    save_results_to_csv(pf_results, pf_summary, "Proportional_Fair")
    
    # ========== Generate Visualizations ==========
    generate_all_plots(rr_results, pf_results, rr_summary, pf_summary, NUM_USERS)
    
    # ========== Print Comparison ==========
    print_summary_comparison(rr_summary, pf_summary)
    
    print("\n" + "="*80)
    print("SIMULATION COMPLETE ✓")
    print("="*80)
    print(f"\nResults saved to: results/ | Plots saved to: plots/")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
