"""
Scheduler implementations: Base Scheduler, Round Robin, and Proportional Fair.
"""

from abc import ABC, abstractmethod
import numpy as np


class BaseScheduler(ABC):
    """Abstract base class for all schedulers."""
    
    def __init__(self, name):
        self.name = name
        
    @abstractmethod
    def schedule(self, users, num_rbs, tti):
        """
        Schedule resource blocks to users.
        
        Args:
            users: List of User objects
            num_rbs: Number of available resource blocks
            tti: Current Transmission Time Interval
            
        Returns:
            List of tuples (user_id, rb_index, throughput)
        """
        pass
    
    def __repr__(self):
        return f"{self.name}Scheduler"


class RoundRobinScheduler(BaseScheduler):
    """
    Round Robin Scheduler.
    
    Allocates RBs sequentially to users in a circular manner,
    regardless of their channel quality.
    """
    
    def __init__(self):
        super().__init__("RoundRobin")
        self.last_user_index = 0
        
    def schedule(self, users, num_rbs, tti):
        """
        Allocate RBs using Round Robin algorithm.
        
        Each RB is assigned to the next user in sequence.
        """
        allocations = []
        num_users = len(users)
        
        if num_users == 0:
            return allocations
        
        for rb_index in range(num_rbs):
            # Select user in round-robin fashion
            user = users[self.last_user_index % num_users]
            throughput = user.instantaneous_throughput
            
            allocations.append((user.user_id, rb_index, throughput))
            user.allocate_rb(throughput)
            
            # Move to next user
            self.last_user_index = (self.last_user_index + 1) % num_users
            
        return allocations


class ProportionalFairScheduler(BaseScheduler):
    """
    Proportional Fair Scheduler.
    
    Allocates each RB to the user with the highest PF metric:
    PF_metric = instantaneous_throughput / average_throughput
    
    This balances between maximizing throughput and ensuring fairness.
    """
    
    def __init__(self, alpha=0.01):
        super().__init__("ProportionalFair")
        self.alpha = alpha  # Smoothing factor for average throughput
        
    def schedule(self, users, num_rbs, tti):
        """
        Allocate RBs using Proportional Fair algorithm.
        
        For each RB:
        1. Calculate PF metric for all users
        2. Assign RB to user with highest PF metric
        3. Update that user's average throughput
        """
        allocations = []
        
        if len(users) == 0:
            return allocations
        
        for rb_index in range(num_rbs):
            # Calculate PF metric for all users
            pf_metrics = []
            for user in users:
                pf_metric = user.get_pf_metric()
                pf_metrics.append((pf_metric, user))
            
            # Select user with highest PF metric
            pf_metrics.sort(key=lambda x: x[0], reverse=True)
            selected_user = pf_metrics[0][1]
            
            throughput = selected_user.instantaneous_throughput
            allocations.append((selected_user.user_id, rb_index, throughput))
            
            # Allocate RB to selected user
            selected_user.allocate_rb(throughput)
            
            # Update average throughput immediately after allocation
            selected_user.update_average_throughput(self.alpha)
        
        return allocations
