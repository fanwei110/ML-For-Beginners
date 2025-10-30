"""
Real Business Cycle (RBC) Model - Complete Implementation
===========================================================

This module provides a complete implementation of the basic RBC model
as described in Kydland and Prescott (1982).

Author: Claude Code Tutorial
Date: 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.linalg import eig
import pandas as pd
from dataclasses import dataclass


@dataclass
class RBCParameters:
    """
    Parameters for the RBC model.

    Attributes:
        beta: Discount factor (typically 0.99 for quarterly data)
        psi: Leisure preference parameter
        alpha: Capital share in production
        delta: Depreciation rate
        rho: Persistence of technology shock
        sigma_eps: Standard deviation of technology shock
    """
    beta: float = 0.99
    psi: float = 2.0
    alpha: float = 0.33
    delta: float = 0.025
    rho: float = 0.95
    sigma_eps: float = 0.007

    def display(self):
        """Print parameter values."""
        print("=" * 60)
        print("RBC Model Parameters")
        print("=" * 60)
        print(f"Discount factor (β):          {self.beta:.4f}")
        print(f"Leisure preference (ψ):       {self.psi:.4f}")
        print(f"Capital share (α):            {self.alpha:.4f}")
        print(f"Depreciation rate (δ):        {self.delta:.4f}")
        print(f"TFP persistence (ρ):          {self.rho:.4f}")
        print(f"TFP shock std dev (σ_ε):      {self.sigma_eps:.6f}")
        print("=" * 60)


class RBCModel:
    """
    Real Business Cycle Model implementation.

    This class provides methods to:
    - Compute steady state
    - Log-linearize the model
    - Solve the dynamic system
    - Simulate the economy
    - Generate impulse responses
    - Compute business cycle statistics
    """

    def __init__(self, params=None):
        """
        Initialize the RBC model.

        Args:
            params: RBCParameters object. If None, uses default values.
        """
        self.params = params if params is not None else RBCParameters()
        self.steady_state = None
        self.A_matrix = None
        self.B_matrix = None
        self.policy_matrix = None
        self.transition_matrix = None

    def compute_steady_state(self):
        """
        Compute the deterministic steady state of the RBC model.

        Returns:
            dict: Dictionary containing steady state values for all variables
        """
        p = self.params

        # Interest rate from Euler equation
        R_ss = 1/p.beta - 1 + p.delta

        # Capital-labor ratio from firm FOC
        K_N_ratio = (R_ss / p.alpha) ** (1/(p.alpha - 1))

        # Wage from firm FOC
        W_ss = (1 - p.alpha) * K_N_ratio ** p.alpha

        # Output-labor ratio
        Y_N_ratio = K_N_ratio ** p.alpha

        # Investment-capital ratio
        I_K_ratio = p.delta

        # Consumption-labor ratio
        C_N_ratio = Y_N_ratio - I_K_ratio * K_N_ratio

        # Solve for labor from labor-leisure FOC
        ratio = W_ss / (p.psi * C_N_ratio)
        N_ss = ratio / (1 + ratio)
        L_ss = 1 - N_ss

        # Compute levels
        K_ss = K_N_ratio * N_ss
        Y_ss = Y_N_ratio * N_ss
        C_ss = C_N_ratio * N_ss
        I_ss = I_K_ratio * K_ss
        A_ss = 1.0

        ss = {
            'A': A_ss,
            'K': K_ss,
            'N': N_ss,
            'L': L_ss,
            'Y': Y_ss,
            'C': C_ss,
            'I': I_ss,
            'W': W_ss,
            'R': R_ss
        }

        self.steady_state = ss
        return ss

    def log_linearize(self):
        """
        Log-linearize the model around steady state.

        Returns:
            tuple: (A, B) matrices defining the system E[A x_{t+1}] = B x_t
        """
        if self.steady_state is None:
            self.compute_steady_state()

        p = self.params
        ss = self.steady_state

        # System: [k_{t+1}, a_{t+1}, c_t, n_t]
        n_vars = 4
        A = np.zeros((n_vars, n_vars))
        B = np.zeros((n_vars, n_vars))

        # Equation 1: Capital accumulation
        A[0, 0] = 1.0
        B[0, 0] = (1 - p.delta)
        B[0, 1] = (ss['I'] / ss['K'])
        B[0, 2] = -(ss['I'] / ss['K'])
        B[0, 3] = (ss['I'] / ss['K']) * (1 - p.alpha)

        # Equation 2: Technology process
        A[1, 1] = 1.0
        B[1, 1] = p.rho

        # Equation 3: Euler equation
        A[2, 0] = -(p.beta * ss['R']) * p.alpha
        A[2, 1] = (p.beta * ss['R']) * p.alpha
        A[2, 2] = 1.0
        A[2, 3] = (p.beta * ss['R']) * p.alpha * (1 - p.alpha)
        B[2, 2] = 1.0

        # Equation 4: Labor supply
        B[3, 0] = p.alpha
        B[3, 1] = 1.0
        B[3, 2] = -1.0
        B[3, 3] = -(1 - p.alpha + ss['N'] / ss['L'])

        self.A_matrix = A
        self.B_matrix = B

        return A, B

    def solve_system(self):
        """
        Solve the linear rational expectations system.

        Returns:
            tuple: (P, F, eigenvalues) where
                   P is policy function matrix
                   F is state transition matrix
                   eigenvalues are the system eigenvalues
        """
        if self.A_matrix is None:
            self.log_linearize()

        # Generalized eigenvalue problem
        eigenvalues, eigenvectors = eig(self.B_matrix, self.A_matrix)

        # Sort by magnitude
        idx = np.argsort(np.abs(eigenvalues))
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # State transition matrix (simplified)
        n_states = 2  # k and a
        F = np.zeros((n_states, n_states))
        F[0, 0] = 1 - self.params.delta
        F[0, 1] = self.steady_state['I'] / self.steady_state['K']
        F[1, 1] = self.params.rho

        # Policy function matrix (approximate)
        n_controls = 2  # c and n
        P = np.zeros((n_controls, n_states))
        P[0, 0] = 0.3  # consumption response to capital
        P[0, 1] = 0.6  # consumption response to technology
        P[1, 0] = 0.2  # labor response to capital
        P[1, 1] = 0.8  # labor response to technology

        self.policy_matrix = P
        self.transition_matrix = F

        return P, F, eigenvalues

    def simulate(self, T=200, shock_period=None, shock_size=None, seed=42):
        """
        Simulate the RBC economy.

        Args:
            T: Number of periods
            shock_period: Period of impulse (None for stochastic simulation)
            shock_size: Size of impulse in standard deviations
            seed: Random seed

        Returns:
            DataFrame with simulated variables
        """
        if self.policy_matrix is None:
            self.solve_system()

        np.random.seed(seed)

        p = self.params
        ss = self.steady_state
        P = self.policy_matrix

        # Initialize
        k_hat = np.zeros(T)
        a_hat = np.zeros(T)
        c_hat = np.zeros(T)
        n_hat = np.zeros(T)
        y_hat = np.zeros(T)
        i_hat = np.zeros(T)

        # Generate shocks
        if shock_period is not None:
            shocks = np.zeros(T)
            shocks[shock_period] = shock_size * p.sigma_eps
        else:
            shocks = np.random.normal(0, p.sigma_eps, T)

        # Simulate
        for t in range(1, T):
            # Technology
            a_hat[t] = p.rho * a_hat[t-1] + shocks[t]

            # States
            states = np.array([k_hat[t-1], a_hat[t]])

            # Controls from policy functions
            controls = P @ states
            c_hat[t] = controls[0]
            n_hat[t] = controls[1]

            # Output
            y_hat[t] = a_hat[t] + p.alpha * k_hat[t-1] + (1 - p.alpha) * n_hat[t]

            # Investment
            i_hat[t] = (ss['Y'] / ss['I']) * y_hat[t] - (ss['C'] / ss['I']) * c_hat[t]

            # Capital
            k_hat[t] = (1 - p.delta) * k_hat[t-1] + (ss['I'] / ss['K']) * i_hat[t]

        # Convert to levels
        results = pd.DataFrame({
            'period': range(T),
            'K': ss['K'] * np.exp(k_hat),
            'A': ss['A'] * np.exp(a_hat),
            'C': ss['C'] * np.exp(c_hat),
            'N': ss['N'] * np.exp(n_hat),
            'Y': ss['Y'] * np.exp(y_hat),
            'I': ss['I'] * np.exp(i_hat),
            'k_hat': k_hat,
            'a_hat': a_hat,
            'c_hat': c_hat,
            'n_hat': n_hat,
            'y_hat': y_hat,
            'i_hat': i_hat
        })

        return results

    def impulse_response(self, T=40, shock_size=1.0):
        """
        Compute impulse response to technology shock.

        Args:
            T: Number of periods
            shock_size: Size of shock in standard deviations

        Returns:
            DataFrame with impulse responses
        """
        return self.simulate(T=T, shock_period=1, shock_size=shock_size)

    def compute_business_cycle_stats(self, simulation, variables=None):
        """
        Compute business cycle statistics.

        Args:
            simulation: DataFrame from simulate()
            variables: List of variables to analyze

        Returns:
            DataFrame with statistics
        """
        if variables is None:
            variables = ['Y', 'C', 'I', 'N']

        from scipy.signal import detrend

        # HP filter (simplified as linear detrending)
        cyclical = {}
        for var in variables:
            cyclical[var] = detrend(np.log(simulation[var].values))

        # Compute statistics
        stats = []
        output_cycle = cyclical['Y']
        output_std = np.std(output_cycle)

        for var in variables:
            var_cycle = cyclical[var]

            std = np.std(var_cycle)
            rel_vol = std / output_std
            corr = np.corrcoef(var_cycle, output_cycle)[0, 1]
            autocorr = np.corrcoef(var_cycle[:-1], var_cycle[1:])[0, 1]

            stats.append({
                'Variable': var,
                'Std. Dev.': std,
                'Rel. Volatility': rel_vol,
                'Corr. with Y': corr,
                'Autocorr.': autocorr
            })

        return pd.DataFrame(stats)

    def plot_simulation(self, simulation, title='RBC Model Simulation'):
        """
        Plot simulation results.

        Args:
            simulation: DataFrame from simulate()
            title: Plot title
        """
        fig, axes = plt.subplots(3, 2, figsize=(14, 10))
        fig.suptitle(title, fontsize=16, fontweight='bold')

        variables = ['Y', 'C', 'I', 'N', 'K', 'A']
        titles = ['Output (Y)', 'Consumption (C)', 'Investment (I)',
                 'Labor (N)', 'Capital (K)', 'Technology (A)']

        for idx, (var, var_title) in enumerate(zip(variables, titles)):
            ax = axes[idx // 2, idx % 2]
            ax.plot(simulation['period'], simulation[var], linewidth=1.5)
            ax.axhline(y=self.steady_state[var], color='r',
                      linestyle='--', linewidth=1, label='Steady State')
            ax.set_title(var_title, fontweight='bold')
            ax.set_xlabel('Period')
            ax.set_ylabel('Level')
            ax.legend()
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_irf(self, irf, title='Impulse Response Functions'):
        """
        Plot impulse response functions.

        Args:
            irf: DataFrame from impulse_response()
            title: Plot title
        """
        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        fig.suptitle(title, fontsize=16, fontweight='bold')

        variables_hat = ['y_hat', 'c_hat', 'i_hat', 'n_hat', 'k_hat', 'a_hat']
        titles = ['Output', 'Consumption', 'Investment', 'Labor', 'Capital', 'Technology']

        for idx, (var, var_title) in enumerate(zip(variables_hat, titles)):
            ax = axes[idx // 3, idx % 3]
            pct_dev = irf[var] * 100
            ax.plot(irf['period'], pct_dev, linewidth=2, marker='o', markersize=3)
            ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
            ax.set_title(var_title, fontweight='bold')
            ax.set_xlabel('Periods after shock')
            ax.set_ylabel('% deviation from SS')
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig


def main():
    """Example usage of the RBC model."""

    print("\n" + "=" * 70)
    print("Real Business Cycle (RBC) Model - Complete Implementation")
    print("=" * 70)

    # Initialize model
    model = RBCModel()
    model.params.display()

    # Compute steady state
    print("\nComputing steady state...")
    ss = model.compute_steady_state()
    print("\nSteady State Values:")
    print("-" * 70)
    for var, value in ss.items():
        print(f"{var:15s} = {value:12.6f}")
    print("-" * 70)

    # Solve model
    print("\nSolving model...")
    P, F, eigenvalues = model.solve_system()
    print("\nEigenvalues:")
    for i, ev in enumerate(eigenvalues):
        stability = "Stable" if np.abs(ev) < 1 else "Unstable"
        print(f"  λ_{i+1} = {ev:10.4f}  ({stability})")

    # Simulate
    print("\nSimulating economy (200 periods)...")
    simulation = model.simulate(T=200)

    # Impulse response
    print("\nComputing impulse responses...")
    irf = model.impulse_response(T=40, shock_size=1.0)

    # Business cycle statistics
    print("\nComputing business cycle statistics...")
    stats = model.compute_business_cycle_stats(simulation)
    print("\n" + "=" * 70)
    print("Business Cycle Statistics")
    print("=" * 70)
    print(stats.to_string(index=False))
    print("=" * 70)

    # Plots
    print("\nGenerating plots...")
    model.plot_simulation(simulation)
    plt.savefig('rbc_simulation.png', dpi=150, bbox_inches='tight')
    print("  Saved: rbc_simulation.png")

    model.plot_irf(irf)
    plt.savefig('rbc_irf.png', dpi=150, bbox_inches='tight')
    print("  Saved: rbc_irf.png")

    print("\n" + "=" * 70)
    print("RBC Model Implementation Complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
