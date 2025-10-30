# Assignment: Real Business Cycle Model

## Instructions

Complete the following exercises to deepen your understanding of the RBC model. You should modify and extend the code from the main notebook (`notebook.ipynb`).

## Part 1: Parameter Sensitivity Analysis (30 points)

### Exercise 1.1: Discount Factor (10 points)

Change the discount factor `β` and analyze its effects:

1. Run the model with three different values: β = 0.96, β = 0.99, β = 0.995
2. For each value, compute:
   - The steady state capital stock
   - The steady state interest rate (R)
   - The relative volatility of investment
3. Create a table comparing these values
4. Explain intuitively why β affects these variables

**Questions:**
- What happens to capital accumulation when households are more patient (higher β)?
- How does β affect the business cycle properties of the model?

### Exercise 1.2: Technology Persistence (10 points)

Vary the persistence parameter `ρ` of the technology process:

1. Simulate the model with ρ = 0.7, ρ = 0.9, ρ = 0.95
2. Generate impulse response functions for each case
3. Plot all three IRFs on the same graph for comparison
4. Calculate the half-life of shocks (time for effect to decay by 50%)

**Questions:**
- How does persistence affect the duration of business cycles?
- Which value of ρ produces cycles most similar to US data?

### Exercise 1.3: Capital Share (10 points)

Experiment with different values of the capital share parameter `α`:

1. Use α = 0.25, α = 0.33 (baseline), α = 0.40
2. For each case, compute and compare:
   - Labor share of income (1 - α)
   - Steady state capital-output ratio
   - Correlation between output and labor
3. Which value best matches the US economy where labor income is about 2/3 of GDP?

## Part 2: Model Extensions (40 points)

### Exercise 2.1: Government Spending (15 points)

Add government spending to the model:

1. Modify the resource constraint to: `C_t + I_t + G_t = Y_t`
2. Assume government spending is a fraction of output: `G_t = g * Y_t` where g = 0.2
3. Add a shock to government spending: `g_t = g_ss + ε_g,t`
4. Solve the extended model and compute IRFs to government spending shocks

**Deliverables:**
- Modified equilibrium conditions
- IRF plots showing responses to a 1% government spending shock
- Comparison of technology shock vs. government spending shock effects

### Exercise 2.2: Investment Adjustment Costs (15 points)

Introduce costs of adjusting the capital stock:

1. Modify the capital accumulation equation to include adjustment costs:
   ```
   K_{t+1} = (1-δ)K_t + I_t - (φ/2)(I_t/K_t - δ)^2 K_t
   ```
   where φ controls the adjustment cost (try φ = 2)

2. Re-derive the firm's first-order conditions
3. Solve the model and compare to the baseline

**Questions:**
- How do adjustment costs affect investment volatility?
- What happens to the impulse responses?
- Do adjustment costs improve the model's fit to data?

### Exercise 2.3: Variable Capital Utilization (10 points)

Allow firms to vary the utilization rate of capital:

1. Production becomes: `Y_t = A_t (u_t K_t)^α N_t^(1-α)` where u_t is utilization
2. Higher utilization has costs: cost function `a(u_t) = b * u_t^2 / 2`
3. Add the firm's FOC for optimal utilization choice

**Task:**
- Derive the new equilibrium conditions
- Explain how this affects the propagation of shocks
- (Bonus) Implement and simulate the extended model

## Part 3: Empirical Analysis (20 points)

### Exercise 3.1: Matching US Data (10 points)

The model's business cycle statistics don't perfectly match US data. Your task:

1. Identify the three biggest discrepancies between model and data
2. For each discrepancy, suggest one modification that might improve the fit
3. Implement one of your suggestions and show the results

**Possible modifications:**
- Habit formation: `U(C_t, L_t) = ln(C_t - h*C_{t-1}) + ψ ln(L_t)`
- Multiple shock processes (investment-specific technology)
- Non-separable preferences

### Exercise 3.2: Impulse Response Analysis (10 points)

Conduct a detailed analysis of impulse responses:

1. Compute IRFs for a 1% technology shock
2. Calculate the cumulative response over 20 periods for each variable
3. Determine when each variable reaches its peak response
4. Create a table summarizing these findings

**Questions:**
- Which variables respond most strongly on impact?
- Which variables have the most delayed response?
- Why does investment respond more than consumption?

## Part 4: Computational Challenges (10 points)

### Exercise 4.1: Accuracy Check (5 points)

Verify that your solution satisfies the equilibrium conditions:

1. Take your simulated data
2. Check that the Euler equation holds approximately
3. Check that the budget constraint is satisfied
4. Compute and report the maximum absolute error

### Exercise 4.2: Alternative Solution Method (5 points)

The notebook uses log-linearization. Research and briefly describe an alternative method:

1. Explain one other solution method (e.g., value function iteration, perturbation methods, projection methods)
2. What are the advantages and disadvantages compared to log-linearization?
3. When would you prefer the alternative method?

## Bonus Challenge (20 points extra)

### Neural Network Policy Function Approximation

Use machine learning to approximate the model's policy functions:

1. Generate a large dataset by simulating the linear model
2. Train a neural network to predict consumption and labor as functions of capital and technology:
   ```
   [C_t, N_t] = NN(K_t, A_t)
   ```
3. Compare the neural network's predictions to the true policy functions
4. Use the neural network to simulate the economy and compare results

**Deliverables:**
- Neural network architecture description
- Training procedure and loss curves
- Comparison plots of NN vs. linear policy functions
- Discussion: When would NN approach be necessary?

**Hints:**
- Use a simple feedforward network (2-3 hidden layers)
- Try different activation functions (ReLU, tanh)
- Normalize inputs and outputs for better training

## Submission Guidelines

Submit a Jupyter notebook containing:

1. **Code**: Well-commented Python code for all exercises
2. **Outputs**: All plots, tables, and numerical results
3. **Analysis**: Written explanations answering the questions
4. **Documentation**: Brief introduction explaining your approach

### Evaluation Criteria

- **Correctness** (40%): Code runs without errors and produces correct results
- **Analysis** (30%): Thoughtful interpretation of results
- **Presentation** (20%): Clear plots, tables, and explanations
- **Creativity** (10%): Novel insights or additional explorations

## Helpful Resources

### Python Tips

```python
# Plotting multiple IRFs
plt.figure(figsize=(12, 6))
for rho in [0.7, 0.9, 0.95]:
    params.rho = rho
    irf = simulate_rbc(params, ss, P, F, T=40, shock_period=1, shock_size=1.0)
    plt.plot(irf['period'], irf['y_hat']*100, label=f'ρ={rho}')
plt.legend()
plt.xlabel('Periods')
plt.ylabel('% deviation from steady state')
plt.title('Output IRF for different ρ values')
plt.show()
```

### Mathematical Derivations

For extensions, you'll need to:
1. Write down the new optimization problem
2. Form the Lagrangian
3. Take first-order conditions
4. Log-linearize around steady state
5. Solve the new linear system

### Common Pitfalls

- **Steady state**: Make sure the extended model steady state is computed correctly
- **Log-linearization**: Be careful with the algebra, especially for products and ratios
- **Stability**: Check that the extended model has the right number of stable eigenvalues
- **Units**: Keep track of whether variables are in levels, logs, or percentage deviations

## Additional Questions for Discussion

1. **Policy implications**: How would you use this model to evaluate a proposed tax cut?

2. **Model limitations**: What important features of real economies does the basic RBC model miss?

3. **Micro vs. Macro**: The model assumes a representative agent. How might results differ with heterogeneous agents?

4. **Forecasting**: Could you use this model to forecast next quarter's GDP? Why or why not?

5. **Financial crisis**: Can the basic RBC model explain the 2008-2009 recession? What would you need to add?

## Solutions

Solutions are provided in the `solution/` directory, but try to complete the exercises on your own first! The learning comes from struggling with the problems.

Good luck, and enjoy exploring the RBC model!

---

## Grading Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| Part 1 (Parameter Sensitivity) | 30 | Correct implementation, clear plots, thoughtful analysis |
| Part 2 (Extensions) | 40 | Mathematical derivations, working code, interpretation |
| Part 3 (Empirical Analysis) | 20 | Data comparison, suggested improvements, implementation |
| Part 4 (Computational) | 10 | Error checking, method comparison |
| Code Quality | - | Clean, commented, reproducible |
| Presentation | - | Professional plots, clear writing |
| Bonus Challenge | +20 | Neural network implementation and analysis |
| **Total** | **100** (+20 bonus) | |

**Estimated time**: 8-12 hours (without bonus), 15-20 hours (with bonus)
