import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class LotkaVolterraModel:
    def __init__(self, alpha=1.0, beta=0.1, delta=0.075, gamma=0.5):
        """
        Initialize Lotka-Volterra model with parameters:
        alpha: prey growth rate
        beta: predation rate
        delta: predator death rate
        gamma: predator growth rate from predation
        """
        self.alpha = alpha
        self.beta = beta
        self.delta = delta
        self.gamma = gamma

    def dynamics(self, state, t):
        """
        Lotka-Volterra equations:
        dx/dt = αx - βxy
        dy/dt = δxy - γy
        where:
        x: prey population
        y: predator population
        """
        prey, predator = state
        
        # Population changes
        d_prey = self.alpha * prey - self.beta * prey * predator
        d_predator = -self.delta * predator + self.gamma * prey * predator
        
        return [d_prey, d_predator]

    def solve(self, initial_state, t_span, t_points=1000):
        """Solve the system numerically"""
        t = np.linspace(t_span[0], t_span[1], t_points)
        solution = odeint(self.dynamics, initial_state, t)
        return t, solution

    def plot_solution(self, t, solution):
        """Plot populations over time and phase space"""
        prey, predator = solution.T
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Population vs Time plot
        ax1.plot(t, prey, 'g-', label='Prey')
        ax1.plot(t, predator, 'r-', label='Predator')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Population')
        ax1.set_title('Population Dynamics')
        ax1.legend()
        ax1.grid(True)
        
        # Phase space plot
        ax2.plot(prey, predator, 'b-')
        ax2.set_xlabel('Prey Population')
        ax2.set_ylabel('Predator Population')
        ax2.set_title('Phase Space')
        ax2.grid(True)
        
        # Add arrow to show direction
        arrow_idx = len(t) // 10
        ax2.arrow(prey[arrow_idx], predator[arrow_idx],
                 prey[arrow_idx+1] - prey[arrow_idx],
                 predator[arrow_idx+1] - predator[arrow_idx],
                 head_width=0.1, head_length=0.1, fc='b', ec='b')
        
        plt.tight_layout()
        plt.show()

    def analyze_solution(self, solution):
        """Calculate key metrics from the solution"""
        prey, predator = solution.T
        
        metrics = {
            'max_prey': np.max(prey),
            'min_prey': np.min(prey),
            'max_predator': np.max(predator),
            'min_predator': np.min(predator),
            'avg_prey': np.mean(prey),
            'avg_predator': np.mean(predator),
            'prey_oscillation': np.max(prey) - np.min(prey),
            'predator_oscillation': np.max(predator) - np.min(predator)
        }
        
        return metrics

def main():
    # Create model instance
    model = LotkaVolterraModel()
    
    # Initial conditions
    initial_state = [10, 5]  # Initial prey and predator populations
    t_span = [0, 100]  # Time span for simulation
    
    # Solve the system
    t, solution = model.solve(initial_state, t_span)
    
    # Plot results
    model.plot_solution(t, solution)
    
    # Analyze results
    metrics = model.analyze_solution(solution)
    
    # Print analysis
    print("Population Analysis:")
    print("-" * 20)
    for key, value in metrics.items():
        print(f"{key}: {value:.2f}")

    # Calculate equilibrium points
    print("\nEquilibrium Points:")
    print(f"Prey: {model.delta/model.gamma:.2f}")
    print(f"Predator: {model.alpha/model.beta:.2f}")

if __name__ == "__main__":
    main()
