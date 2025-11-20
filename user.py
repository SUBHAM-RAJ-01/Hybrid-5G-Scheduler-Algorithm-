"""
User class representing a 5G user equipment (UE) with channel quality and throughput tracking.
"""

class User:
    """
    Represents a single user in the 5G network.
    
    Attributes:
        user_id: Unique identifier for the user
        cqi: Channel Quality Indicator (1-15)
        instantaneous_throughput: Current achievable throughput based on CQI
        average_throughput: Running average throughput (for PF scheduler)
        total_data: Total data received across all TTIs
        rb_count: Number of RBs allocated to this user
    """
    
    def __init__(self, user_id, cqi):
        self.user_id = user_id
        self.cqi = cqi
        self.instantaneous_throughput = 0.0
        self.average_throughput = 0.1  # Small initial value to avoid division by zero
        self.total_data = 0.0
        self.rb_count = 0
        self.throughput_history = []
        
    def update_instantaneous_throughput(self, throughput):
        """Update the instantaneous throughput based on current channel conditions."""
        self.instantaneous_throughput = throughput
        
    def update_average_throughput(self, alpha=0.01):
        """
        Update average throughput using exponential moving average.
        
        Args:
            alpha: Smoothing factor (0 < alpha < 1)
                   Smaller alpha = more weight on history
        """
        self.average_throughput = (1 - alpha) * self.average_throughput + alpha * self.instantaneous_throughput
        
    def allocate_rb(self, throughput):
        """
        Allocate a resource block to this user.
        
        Args:
            throughput: Throughput achieved with this RB allocation
        """
        self.rb_count += 1
        self.total_data += throughput
        
    def get_pf_metric(self):
        """
        Calculate Proportional Fair metric.
        
        Returns:
            PF metric = instantaneous_throughput / average_throughput
        """
        if self.average_throughput == 0:
            return float('inf')
        return self.instantaneous_throughput / self.average_throughput
    
    def reset_tti_stats(self):
        """Reset per-TTI statistics (called at the start of each TTI)."""
        self.rb_count = 0
        self.instantaneous_throughput = 0.0
        
    def __repr__(self):
        return f"User(id={self.user_id}, CQI={self.cqi}, avg_tput={self.average_throughput:.2f})"
