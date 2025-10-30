# RBC Model - Solution Files

This directory contains complete solutions and reference implementations for the RBC model lesson.

## Contents

### Python Implementation

- **`Python/rbc_model.py`**: Complete object-oriented implementation of the RBC model
  - `RBCParameters` class: Parameter container
  - `RBCModel` class: Full model implementation with all methods
  - Can be imported as a module or run as a standalone script

### Running the Solutions

#### Option 1: Run the Python script

```bash
cd solution/Python
python rbc_model.py
```

This will:
- Compute the steady state
- Solve the model
- Simulate the economy
- Generate impulse responses
- Compute business cycle statistics
- Save plots to PNG files

#### Option 2: Import as a module

```python
from rbc_model import RBCModel, RBCParameters

# Create and solve model
model = RBCModel()
model.compute_steady_state()
model.solve_system()

# Simulate
simulation = model.simulate(T=200)

# Impulse responses
irf = model.impulse_response(T=40, shock_size=1.0)

# Statistics
stats = model.compute_business_cycle_stats(simulation)
```

#### Option 3: Use in Jupyter notebook

```python
# Add solution directory to path
import sys
sys.path.append('./solution/Python')

from rbc_model import RBCModel

# Use the model
model = RBCModel()
# ... your code here
```

## Using the Solution for Assignments

### For Parameter Sensitivity Analysis (Assignment Part 1)

```python
from rbc_model import RBCModel, RBCParameters

# Exercise 1.1: Different discount factors
results = []
for beta in [0.96, 0.99, 0.995]:
    params = RBCParameters(beta=beta)
    model = RBCModel(params)
    ss = model.compute_steady_state()
    results.append({
        'beta': beta,
        'K_ss': ss['K'],
        'R_ss': ss['R']
    })

import pandas as pd
print(pd.DataFrame(results))
```

### For Model Extensions (Assignment Part 2)

You can extend the `RBCModel` class:

```python
class ExtendedRBCModel(RBCModel):
    """Extended RBC model with government spending."""

    def __init__(self, params=None, g=0.2):
        super().__init__(params)
        self.g = g  # Government spending share

    def compute_steady_state(self):
        # Override to include government
        ss = super().compute_steady_state()
        ss['G'] = self.g * ss['Y']
        ss['C'] = ss['Y'] - ss['I'] - ss['G']
        return ss
```

### For Impulse Response Analysis (Assignment Part 3)

```python
model = RBCModel()
model.solve_system()

# Generate IRF
irf = model.impulse_response(T=40, shock_size=1.0)

# Analyze
variables = ['y_hat', 'c_hat', 'i_hat', 'n_hat']
for var in variables:
    peak_period = irf[var].abs().idxmax()
    peak_value = irf[var].iloc[peak_period]
    cumulative = irf[var].sum()
    print(f"{var}: Peak at t={peak_period}, value={peak_value:.4f}, "
          f"cumulative={cumulative:.4f}")
```

## Key Methods Reference

### RBCModel Class

| Method | Description | Returns |
|--------|-------------|---------|
| `compute_steady_state()` | Compute deterministic steady state | dict of steady state values |
| `log_linearize()` | Log-linearize around steady state | (A, B) matrices |
| `solve_system()` | Solve linear RE system | (P, F, eigenvalues) |
| `simulate(T, ...)` | Simulate economy | DataFrame with time series |
| `impulse_response(T, shock_size)` | Compute IRF | DataFrame with responses |
| `compute_business_cycle_stats(sim)` | Compute BC statistics | DataFrame with stats |
| `plot_simulation(sim)` | Plot simulation results | matplotlib Figure |
| `plot_irf(irf)` | Plot impulse responses | matplotlib Figure |

### RBCParameters Class

| Attribute | Description | Default |
|-----------|-------------|---------|
| `beta` | Discount factor | 0.99 |
| `psi` | Leisure preference | 2.0 |
| `alpha` | Capital share | 0.33 |
| `delta` | Depreciation rate | 0.025 |
| `rho` | TFP persistence | 0.95 |
| `sigma_eps` | TFP shock std dev | 0.007 |

## Advanced Usage

### Custom Parameters

```python
from rbc_model import RBCModel, RBCParameters

# Create custom parameters
params = RBCParameters(
    beta=0.98,
    alpha=0.36,
    rho=0.90
)

# Initialize model with custom parameters
model = RBCModel(params)
```

### Multiple Simulations

```python
import numpy as np

# Run multiple simulations with different shocks
simulations = []
for i in range(100):
    sim = model.simulate(T=200, seed=i)
    simulations.append(sim)

# Compute ensemble average
ensemble_avg = pd.concat(simulations).groupby('period').mean()
```

### Comparative Statics

```python
# Compare different parameter values
rho_values = [0.7, 0.85, 0.95]
irfs = {}

for rho in rho_values:
    params = RBCParameters(rho=rho)
    model = RBCModel(params)
    model.solve_system()
    irfs[rho] = model.impulse_response()

# Plot comparison
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
for rho, irf in irfs.items():
    plt.plot(irf['period'], irf['y_hat']*100, label=f'ρ={rho}')
plt.legend()
plt.xlabel('Periods')
plt.ylabel('% deviation from steady state')
plt.title('Output Response for Different ρ')
plt.grid(True)
plt.show()
```

## Testing the Implementation

The solution includes internal consistency checks:

```python
model = RBCModel()
model.solve_system()
sim = model.simulate(T=200)

# Check resource constraint
Y = sim['Y'].values
C = sim['C'].values
I = sim['I'].values
residual = Y - C - I
print(f"Max resource constraint error: {np.max(np.abs(residual)):.10f}")

# Should be very small (< 1e-6)
```

## Numerical Considerations

### Accuracy

The log-linear approximation is accurate for small deviations from steady state (< 5%). For larger shocks, higher-order perturbation methods are needed.

### Stability

The model should have exactly 2 stable eigenvalues (equal to the number of state variables). Check this:

```python
_, _, eigenvalues = model.solve_system()
n_stable = sum(np.abs(eigenvalues) < 1)
print(f"Number of stable eigenvalues: {n_stable}")
# Should print: 2
```

### Computational Speed

For large simulations:
- Use vectorized operations (already implemented)
- Avoid loops where possible
- Consider numba JIT compilation for production code

## Troubleshooting

### Common Issues

1. **"Steady state not computed"**: Call `compute_steady_state()` before other methods
2. **Unstable simulations**: Check that eigenvalues are correctly computed
3. **Negative values**: Ensure shocks are not too large for log-linear approximation
4. **Import errors**: Make sure solution directory is in Python path

### Getting Help

If you encounter issues:
1. Check that all prerequisites are installed: numpy, scipy, pandas, matplotlib
2. Verify parameter values are economically reasonable
3. Review the main notebook for examples
4. Compare your results with the solution output

## Additional Resources

### Mathematical Details

See the main README.md for:
- Derivation of equilibrium conditions
- Log-linearization procedure
- Solution method explanation

### Code Style

The solution follows these conventions:
- PEP 8 style guide
- Type hints in function signatures (Python 3.5+)
- Docstrings in NumPy format
- Object-oriented design for extensibility

### Performance Benchmarks

On a typical laptop (2020+):
- Steady state computation: < 1ms
- Model solution: < 10ms
- 200-period simulation: < 50ms
- 1000 Monte Carlo simulations: < 5s

## Citation

If you use this code in your research or teaching, please cite:

```
RBC Model Implementation for ML-For-Beginners
Based on: Kydland, F. E., & Prescott, E. C. (1982).
"Time to build and aggregate fluctuations." Econometrica, 50(6), 1345-1370.
```

## License

This solution is provided for educational purposes as part of the ML-For-Beginners curriculum.

---

**Note**: These are reference solutions. For maximum learning, attempt the exercises yourself before consulting these files!
