"""
Test script to verify the 5G scheduler simulation works correctly.

Run this before the full simulation to catch any issues.
"""

import numpy as np
from user import User
from scheduler import RoundRobinScheduler, ProportionalFairScheduler
from system import System
from utils import (
    get_throughput_from_cqi,
    calculate_jains_fairness_index,
    generate_random_cqi,
    update_cqi_dynamic
)


def test_user_class():
    """Test User class functionality."""
    print("Testing User class...")
    
    user = User(user_id=0, cqi=10)
    assert user.user_id == 0
    assert user.cqi == 10
    assert user.average_throughput == 0.1
    
    user.update_instantaneous_throughput(5.0)
    assert user.instantaneous_throughput == 5.0
    
    user.allocate_rb(5.0)
    assert user.rb_count == 1
    assert user.total_data == 5.0
    
    pf_metric = user.get_pf_metric()
    assert pf_metric == 5.0 / 0.1
    
    user.update_average_throughput(alpha=0.1)
    assert user.average_throughput > 0.1
    
    print("✓ User class tests passed")


def test_utils():
    """Test utility functions."""
    print("Testing utility functions...")
    
    # Test CQI to throughput mapping
    tput = get_throughput_from_cqi(1)
    assert tput == 0.15
    
    tput = get_throughput_from_cqi(15)
    assert tput == 5.55
    
    # Test fairness calculation
    throughputs = [10, 10, 10]
    jfi = calculate_jains_fairness_index(throughputs)
    assert abs(jfi - 1.0) < 0.001  # Perfect fairness
    
    throughputs = [30, 0, 0]
    jfi = calculate_jains_fairness_index(throughputs)
    assert jfi < 0.5  # Poor fairness
    
    # Test CQI generation
    cqis = generate_random_cqi(10, min_cqi=1, max_cqi=15)
    assert len(cqis) == 10
    assert all(1 <= cqi <= 15 for cqi in cqis)
    
    # Test dynamic CQI update
    new_cqi = update_cqi_dynamic(10, change_probability=1.0, max_change=2)
    assert 1 <= new_cqi <= 15
    
    print("✓ Utility function tests passed")


def test_round_robin_scheduler():
    """Test Round Robin scheduler."""
    print("Testing Round Robin scheduler...")
    
    scheduler = RoundRobinScheduler()
    
    # Create test users
    users = [User(i, cqi=10) for i in range(3)]
    for user in users:
        user.update_instantaneous_throughput(2.73)
    
    # Schedule 9 RBs
    allocations = scheduler.schedule(users, num_rbs=9, tti=0)
    
    assert len(allocations) == 9
    
    # Check round-robin distribution
    user_rb_counts = [0, 0, 0]
    for user_id, rb_index, throughput in allocations:
        user_rb_counts[user_id] += 1
    
    assert user_rb_counts == [3, 3, 3]  # Equal distribution
    
    print("✓ Round Robin scheduler tests passed")


def test_proportional_fair_scheduler():
    """Test Proportional Fair scheduler."""
    print("Testing Proportional Fair scheduler...")
    
    scheduler = ProportionalFairScheduler(alpha=0.1)
    
    # Create test users with different CQI
    users = [
        User(0, cqi=15),  # High CQI
        User(1, cqi=5),   # Low CQI
        User(2, cqi=10)   # Medium CQI
    ]
    
    users[0].update_instantaneous_throughput(5.55)
    users[1].update_instantaneous_throughput(0.88)
    users[2].update_instantaneous_throughput(2.73)
    
    # Schedule 10 RBs
    allocations = scheduler.schedule(users, num_rbs=10, tti=0)
    
    assert len(allocations) == 10
    
    # User with highest CQI should get more RBs initially
    user_rb_counts = [0, 0, 0]
    for user_id, rb_index, throughput in allocations:
        user_rb_counts[user_id] += 1
    
    # User 0 (highest CQI) should get most RBs
    assert user_rb_counts[0] >= user_rb_counts[1]
    assert user_rb_counts[0] >= user_rb_counts[2]
    
    print("✓ Proportional Fair scheduler tests passed")


def test_system_simulation():
    """Test System simulation."""
    print("Testing System simulation...")
    
    np.random.seed(42)
    cqi_list = [10, 12, 8]
    
    scheduler = RoundRobinScheduler()
    system = System(num_users=3, num_rbs=10, cqi_list=cqi_list, scheduler=scheduler)
    
    # Run a few TTIs
    results = system.run_simulation(num_ttis=10, dynamic_channel=False, log_interval=5)
    
    assert len(results) == 10
    assert system.current_tti == 10
    
    # Check TTI data structure
    tti_data = results[0]
    assert 'tti' in tti_data
    assert 'allocations' in tti_data
    assert 'total_throughput' in tti_data
    assert 'fairness_index' in tti_data
    
    # Get summary statistics
    summary = system.get_summary_statistics()
    assert 'total_system_throughput' in summary
    assert 'avg_fairness_index' in summary
    assert summary['num_ttis'] == 10
    
    print("✓ System simulation tests passed")


def test_integration():
    """Test full integration with both schedulers."""
    print("Testing full integration...")
    
    np.random.seed(42)
    NUM_USERS = 5
    NUM_RBS = 20
    NUM_TTIS = 50
    
    cqi_list = generate_random_cqi(NUM_USERS, min_cqi=5, max_cqi=15)
    
    # Test Round Robin
    rr_scheduler = RoundRobinScheduler()
    rr_system = System(NUM_USERS, NUM_RBS, cqi_list.copy(), rr_scheduler)
    rr_results = rr_system.run_simulation(NUM_TTIS, dynamic_channel=True, log_interval=25)
    rr_summary = rr_system.get_summary_statistics()
    
    assert len(rr_results) == NUM_TTIS
    assert rr_summary['total_system_throughput'] > 0
    
    # Test Proportional Fair
    pf_scheduler = ProportionalFairScheduler(alpha=0.01)
    pf_system = System(NUM_USERS, NUM_RBS, cqi_list.copy(), pf_scheduler)
    pf_results = pf_system.run_simulation(NUM_TTIS, dynamic_channel=True, log_interval=25)
    pf_summary = pf_system.get_summary_statistics()
    
    assert len(pf_results) == NUM_TTIS
    assert pf_summary['total_system_throughput'] > 0
    
    # PF should typically achieve higher throughput
    print(f"  RR Total Throughput: {rr_summary['total_system_throughput']:.2f} Mbps")
    print(f"  PF Total Throughput: {pf_summary['total_system_throughput']:.2f} Mbps")
    
    if pf_summary['total_system_throughput'] > rr_summary['total_system_throughput']:
        print("  ✓ PF achieves higher throughput (expected)")
    else:
        print("  ⚠ RR achieves higher throughput (unusual but possible)")
    
    print("✓ Integration tests passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print(" " * 20 + "RUNNING SIMULATION TESTS")
    print("="*70 + "\n")
    
    try:
        test_user_class()
        test_utils()
        test_round_robin_scheduler()
        test_proportional_fair_scheduler()
        test_system_simulation()
        test_integration()
        
        print("\n" + "="*70)
        print(" " * 20 + "ALL TESTS PASSED ✓")
        print("="*70)
        print("\nThe simulation is ready to run!")
        print("Execute: python main.py")
        print("="*70 + "\n")
        
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
