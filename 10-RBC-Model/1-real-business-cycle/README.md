# Real Business Cycle (RBC) Model

## Introduction

The **Real Business Cycle (RBC) model** is a class of macroeconomic models that explains business-cycle fluctuations as the result of real (rather than nominal) shocks to the economy. Developed by Kydland and Prescott (1982), who won the Nobel Prize in Economics in 2004, the RBC model is a cornerstone of modern macroeconomics and Dynamic Stochastic General Equilibrium (DSGE) modeling.

### Key Features

- **Microfoundations**: Built on optimal decisions by households and firms
- **General Equilibrium**: All markets clear in equilibrium
- **Dynamic**: Forward-looking agents make intertemporal decisions
- **Stochastic**: Economy is subject to random shocks (especially technology shocks)
- **Real Factors**: Business cycles driven by real factors (productivity), not monetary factors

### Why Study RBC Models?

1. **Understanding Economic Fluctuations**: Provides a framework to understand why economies experience booms and recessions
2. **Policy Analysis**: Helps evaluate the effects of fiscal and monetary policies
3. **Numerical Methods**: Introduces computational techniques used in modern economics
4. **Machine Learning Connection**: The numerical solution methods have parallels with ML optimization techniques

## The Basic RBC Model

### 1. Model Setup

The economy consists of:
- **Representative Household**: Makes consumption and labor supply decisions
- **Representative Firm**: Chooses capital and labor to maximize profits
- **Technology Shocks**: Random productivity fluctuations

### 2. Mathematical Formulation

#### Household Problem

The representative household maximizes lifetime utility:

```
max E_0 Σ_{t=0}^∞ β^t U(C_t, L_t)
```

Where:
- `C_t` = Consumption at time t
- `L_t` = Leisure at time t (labor supply = 1 - L_t)
- `β` = Discount factor (0 < β < 1)
- `E_0` = Expectation operator at time 0

We typically use a **separable utility function**:

```
U(C_t, L_t) = ln(C_t) + ψ ln(L_t)
```

Where `ψ` controls the preference for leisure.

**Budget Constraint**:

```
C_t + I_t = W_t N_t + R_t K_t
```

Where:
- `I_t` = Investment
- `W_t` = Wage rate
- `N_t` = Labor supply (N_t = 1 - L_t)
- `R_t` = Rental rate of capital
- `K_t` = Capital stock

**Capital Accumulation**:

```
K_{t+1} = (1 - δ) K_t + I_t
```

Where `δ` is the depreciation rate.

#### Firm Problem

The representative firm maximizes profits:

```
max π_t = Y_t - W_t N_t - R_t K_t
```

Subject to the **Cobb-Douglas production function**:

```
Y_t = A_t K_t^α N_t^{1-α}
```

Where:
- `Y_t` = Output
- `A_t` = Total Factor Productivity (TFP) / Technology
- `α` = Capital share (typically around 0.33)

**Technology Process** (AR(1) process in logs):

```
ln(A_t) = ρ ln(A_{t-1}) + ε_t
```

Where:
- `ρ` = Persistence parameter (0 < ρ < 1)
- `ε_t` ~ N(0, σ_ε^2) = Technology shock

### 3. Equilibrium Conditions

#### First-Order Conditions (FOCs)

From household optimization:

1. **Labor-Leisure Trade-off**:
   ```
   ψ C_t / L_t = W_t
   ```

2. **Euler Equation** (consumption-saving decision):
   ```
   1 / C_t = β E_t [(1 / C_{t+1}) (R_{t+1} + 1 - δ)]
   ```

From firm optimization:

3. **Labor Demand**:
   ```
   W_t = (1 - α) A_t K_t^α N_t^{-α}
   ```

4. **Capital Demand**:
   ```
   R_t = α A_t K_t^{α-1} N_t^{1-α}
   ```

#### Market Clearing

5. **Resource Constraint**:
   ```
   C_t + I_t = Y_t
   ```

6. **Labor Market Clearing**: N_t = 1 - L_t

## Solution Methods

### 1. Log-Linearization

The most common approach is to **log-linearize** the equilibrium conditions around the steady state. This transforms the non-linear system into a linear system that can be solved analytically or numerically.

**Steps**:
1. Find the steady state (where all variables are constant)
2. Take first-order Taylor approximation around steady state
3. Solve the resulting linear difference equations

### 2. Numerical Solution

For this tutorial, we'll use **numerical methods**:
- Discretize the state space
- Solve using value function iteration or policy function iteration
- Simulate the economy given technology shocks

### 3. Calibration

Typical parameter values for the US economy:

| Parameter | Symbol | Value | Description |
|-----------|--------|-------|-------------|
| Discount factor | β | 0.99 | Implies 4% annual interest rate |
| Depreciation rate | δ | 0.025 | 2.5% quarterly (10% annual) |
| Capital share | α | 0.33 | Capital's share of income |
| Leisure preference | ψ | 2.0 | Balances labor/leisure |
| TFP persistence | ρ | 0.95 | High persistence in productivity |
| TFP shock std. | σ_ε | 0.007 | Standard deviation of shocks |

## Implementation Roadmap

In the accompanying Jupyter notebook, we will:

1. **Define parameters** and calibrate the model
2. **Compute steady state** values analytically
3. **Log-linearize** the equilibrium conditions
4. **Solve the linear system** using eigenvalue decomposition
5. **Simulate** the economy with random technology shocks
6. **Generate impulse responses** to a one-time technology shock
7. **Compute business cycle statistics** (volatilities, correlations)
8. **Visualize results** with plots

## Expected Results

A well-calibrated RBC model can explain several key features of business cycles:

1. **Pro-cyclical variables**: Consumption, investment, hours worked all move together
2. **Investment volatility**: Investment is much more volatile than output
3. **Consumption smoothing**: Consumption is less volatile than output
4. **Persistent fluctuations**: Effects of shocks persist over time

## Extensions and Applications

### Possible Extensions
- **Government spending**: Add government sector
- **Money**: Incorporate monetary policy (towards DSGE models)
- **Multiple sectors**: Add more detailed production structure
- **Heterogeneous agents**: Move beyond representative agent

### Connection to Machine Learning

Modern applications use ML techniques in macroeconomic modeling:
- **Neural networks** to approximate policy functions
- **Reinforcement learning** for solving dynamic programming problems
- **Time series forecasting** to predict macro variables
- **Deep learning** for high-dimensional DSGE models

## Prerequisites

To understand this lesson, you should have:
- Basic calculus (derivatives, optimization)
- Some knowledge of economics (supply/demand, basic macro)
- Python programming basics
- Understanding of linear algebra

## Required Libraries

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.linalg import eig
import pandas as pd
```

## References

1. Kydland, F. E., & Prescott, E. C. (1982). "Time to build and aggregate fluctuations." *Econometrica*, 50(6), 1345-1370.
2. Cooley, T. F. (Ed.). (1995). *Frontiers of business cycle research*. Princeton University Press.
3. Ljungqvist, L., & Sargent, T. J. (2018). *Recursive macroeconomic theory*. MIT Press.
4. Fernández-Villaverde, J., Rubio-Ramírez, J. F., & Schorfheide, F. (2016). "Solution and estimation methods for DSGE models." *Handbook of macroeconomics*, 2, 527-724.

## Next Steps

Ready to implement the RBC model? Open the [notebook.ipynb](notebook.ipynb) to start coding!

After completing the notebook, try the [assignment](assignment.md) to test your understanding.

---

## Lesson Structure

- **Estimated time**: 3-4 hours
- **Level**: Advanced
- **Topics**: Macroeconomics, DSGE Models, Numerical Methods, Economic Simulations
