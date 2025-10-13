# Battle Royale Simulation

This mini-project demonstrates how to build a **human-inspired battle royale**
environment that you can tweak and observe. Agents move through a square,
city-like map filled with alleys, cover, and deliberate dead-ends. They favour
survival, disengaging from fights unless they have a clear advantage, are
cornered, or the shrinking safe zone forces their hand.

## Features

- **City layout** – blocky buildings, alleys, and dead-ends encourage ambushes
  and defensive play.
- **Heterogeneous agents** – every agent has randomised health, damage, armour,
  vision, and one or more skills (dash, medkit, grenade) for variety.
- **Risk-aware behaviour** – agents only commit to a fight when healthy, when
  their opponent is trapped, or when they have no escape options.
- **Shrinking zone** – just like classic battle royale games, a shrinking safe
  radius applies pressure so that passive play eventually becomes risky.
- **Rich logging & visualisation** – capture the entire match history and
  render it to static frames or an animated GIF.

## Usage

```python
from battle_royale import BattleRoyaleEnvironment

# Configure the arena however you like
env = BattleRoyaleEnvironment(
    grid_size=27,
    num_agents=14,
    num_blocks=10,
    time_limit=220,
    seed=42,
)

# Run the simulation (set verbose=True to print a play-by-play log)
report = env.run(verbose=True)
print(report["winner"], "survived for", report["ticks"], "ticks")

# Render a GIF to inspect the fight visually
env.render_animation("battle.gif", dpi=110)
```

### Customising agents

Use the `agent_params` argument to override the automatically generated
statistics. Each dictionary in the sequence corresponds to one agent:

```python
cautious_duo = [
    {"aggression": 0.2, "caution": 0.95, "bravery_threshold": 12},
    {"aggression": 0.4, "vision_range": 8, "attack_range": 2},
]

env = BattleRoyaleEnvironment(num_agents=2, agent_params=cautious_duo, seed=7)
```

### Visualising individual frames

The `render_frame` helper converts any stored state into a Matplotlib figure.
This is convenient when you want to inspect key ticks without generating a
full animation.

```python
fig = env.render_frame(index=15)
fig.savefig("tick-15.png", dpi=120)
```

## Requirements

The simulation core itself has no third-party dependencies. Optional
visualisation features need:

- `matplotlib` for plotting frames or animations
- `numpy` and `imageio` for GIF export

Install them manually with `pip install matplotlib numpy imageio` if they are
not already present in your environment.

## Educational notes

This scenario is intentionally rule-based. Instead of using reinforcement
learning, it illustrates how hand-crafted heuristics can encode human biases
(like risk aversion, reliance on cover, and opportunistic aggression). It can
serve as a playground for later experiments with learning agents.
