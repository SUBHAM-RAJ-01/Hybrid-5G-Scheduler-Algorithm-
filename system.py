"""
5G System simulation engine that manages users, schedulers, and TTI execution.
"""

import numpy as np
from user import User
from utils import get_throughput_from_cqi, update_cqi_dynamic, calculate_jains_fairness_index


class System:
    """
    5G Base Station System that manages users and resource allocation.
    
    Attributes:
        num_users: Number of users in the system
        num_rbs: Number of available Resource Blocks
        users: List of User objects
        scheduler: Scheduler instance (RR or PF)
    """
    
    def __init__(self, num_users, num_rbs, cqi_list, scheduler):
        self.num_users = num_users
        self.num_rbs = num_rbs
        self.scheduler = scheduler
        self.users = []
        
        # Initialize users with given CQI values
        for i, cqi in enumerate(cqi_list):
            user = User(user_id=i, cqi=cqi)
            self.users.append(user)
        
        # Simulation tracking
        self.tti_results = []
        self.current_tti = 0
        
    def run_tti(self, dynamic_channel=False):
        """
        Execute one Transmission Time Interval (TTI).
        
        Args:
            dynamic_channel: If True, randomly update user CQI values
            
        Returns:
            Dictionary with TTI results
        """
        # Reset per-TTI statistics
        for user in self.users:
            user.reset_tti_stats()
        
        # Update channel conditions (CQI) if dynamic
        if dynamic_channel:
            for user in self.users:
                user.cqi = update_cqi_dynamic(user.cqi)
        
        # Update instantaneous throughput based on current CQI
        for user in self.users:
            throughput = get_throughput_from_cqi(user.cqi)
            user.update_instantaneous_throughput(throughput)
        
        # Schedule resource blocks
        allocations = self.scheduler.schedule(self.users, self.num_rbs, self.current_tti)
        
        # Collect TTI statistics
        tti_data = {
            'tti': self.current_tti,
            'allocations': allocations,
            'user_throughputs': [user.total_data for user in self.users],
            'user_rb_counts': [user.rb_count for user in self.users],
            'user_cqi': [user.cqi for user in self.users],
            'user_avg_throughput': [user.average_throughput for user in self.users],
            'total_throughput': sum(user.total_data for user in self.users),
            'fairness_index': calculate_jains_fairness_index([user.total_data for user in self.users])
        }
        
        self.tti_results.append(tti_data)
        self.current_tti += 1
        
        return tti_data
    
    def run_simulation(self, num_ttis, dynamic_channel=False, log_interval=100):
        """
        Run simulation for multiple TTIs.
        
        Args:
            num_ttis: Number of TTIs to simulate
            dynamic_channel: Enable dynamic channel conditions
            log_interval: Print progress every N TTIs
            
        Returns:
            List of TTI results
        """
        print(f"\n{'='*60}")
        print(f"Starting Simulation: {self.scheduler.name}")
        print(f"Users: {self.num_users}, RBs: {self.num_rbs}, TTIs: {num_ttis}")
        print(f"Dynamic Channel: {dynamic_channel}")
        print(f"{'='*60}\n")
        
        for tti in range(num_ttis):
            self.run_tti(dynamic_channel=dynamic_channel)
            
            if (tti + 1) % log_interval == 0:
                total_tput = self.tti_results[-1]['total_throughput']
                fairness = self.tti_results[-1]['fairness_index']
                print(f"TTI {tti + 1}/{num_ttis} | "
                      f"Total Throughput: {total_tput:.2f} Mbps | "
                      f"Fairness: {fairness:.4f}")
        
        print(f"\nSimulation Complete: {self.scheduler.name}\n")
        return self.tti_results
    
    def get_summary_statistics(self):
        """
        Calculate summary statistics across all TTIs.
        
        Returns:
            Dictionary with summary metrics
        """
        if not self.tti_results:
            return {}
        
        # Aggregate per-user throughput across all TTIs
        user_total_throughput = [0.0] * self.num_users
        user_total_rbs = [0] * self.num_users
        
        for tti_data in self.tti_results:
            for user_id, throughput in enumerate(tti_data['user_throughputs']):
                user_total_throughput[user_id] += throughput
            for user_id, rb_count in enumerate(tti_data['user_rb_counts']):
                user_total_rbs[user_id] += rb_count
        
        # Calculate average throughput per user
        avg_user_throughput = [tput / len(self.tti_results) for tput in user_total_throughput]
        
        # System-level metrics
        total_system_throughput = sum(user_total_throughput)
        avg_system_throughput = total_system_throughput / len(self.tti_results)
        
        # Fairness metrics
        fairness_values = [tti['fairness_index'] for tti in self.tti_results]
        avg_fairness = np.mean(fairness_values)
        
        # RB utilization
        total_rbs_allocated = sum(user_total_rbs)
        total_rbs_available = self.num_rbs * len(self.tti_results)
        rb_utilization = (total_rbs_allocated / total_rbs_available) * 100 if total_rbs_available > 0 else 0
        
        summary = {
            'scheduler': self.scheduler.name,
            'num_ttis': len(self.tti_results),
            'user_total_throughput': user_total_throughput,
            'user_avg_throughput': avg_user_throughput,
            'user_total_rbs': user_total_rbs,
            'total_system_throughput': total_system_throughput,
            'avg_system_throughput': avg_system_throughput,
            'avg_fairness_index': avg_fairness,
            'rb_utilization_percent': rb_utilization
        }
        
        return summary
    
    def reset(self):
        """Reset simulation state."""
        self.tti_results = []
        self.current_tti = 0
        for user in self.users:
            user.total_data = 0.0
            user.average_throughput = 0.1
            user.reset_tti_stats()
