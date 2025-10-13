"""Battle royale simulation with human-inspired tactical behavior.

This script builds a square arena populated with rectangular obstacles and simulates
an entirely AI-controlled battle royale. Agents prefer to disengage unless they have a
clear advantage or are trapped, encouraging more human-like hit-and-run tactics.

Run ``python battle_royale_simulation.py --help`` for usage information.
"""
from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

try:  # pragma: no cover - optional dependency for visualization only.
    import matplotlib.animation as animation
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover
    animation = None  # type: ignore[assignment]
    plt = None  # type: ignore[assignment]

Position = Tuple[int, int]


@dataclass
class Agent:
    """Represents a single combatant in the arena."""

    identifier: int
    position: Position
    health: float
    attack: float
    defense: float
    vision: int
    bravery_threshold: float
    speed: int = 1
    preferred_cover: float = 0.4
    intent: str = field(default="search", init=False)

    def is_alive(self) -> bool:
        return self.health > 0

    def distance_to(self, other: "Agent") -> float:
        return math.dist(self.position, other.position)


class Arena:
    """Square arena with axis-aligned rectangular obstacles."""

    def __init__(self, size: int, obstacles: Sequence[Tuple[Position, Position]]):
        self.size = size
        self.obstacles = self._inflate_obstacles(obstacles)
        self.center = (size - 1) / 2.0

    def _inflate_obstacles(
        self, rectangles: Sequence[Tuple[Position, Position]]
    ) -> Dict[Position, bool]:
        cells: Dict[Position, bool] = {}
        for (x0, y0), (x1, y1) in rectangles:
            for x in range(x0, x1 + 1):
                for y in range(y0, y1 + 1):
                    cells[(x, y)] = True
        return cells

    def is_blocked(self, position: Position) -> bool:
        x, y = position
        if not (0 <= x < self.size and 0 <= y < self.size):
            return True
        return self.obstacles.get(position, False)

    def neighbours(self, position: Position) -> List[Position]:
        x, y = position
        candidates = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        return [pos for pos in candidates if not self.is_blocked(pos)]

    def moves_with_cover(self, position: Position) -> List[Tuple[Position, float]]:
        """Return free neighbour positions paired with cover score."""

        def cover_score(pos: Position) -> float:
            px, py = pos
            walls = 0
            for nx in range(px - 1, px + 2):
                for ny in range(py - 1, py + 2):
                    if (nx, ny) == pos:
                        continue
                    if self.obstacles.get((nx, ny), False):
                        walls += 1
            return walls / 8.0

        return [(move, cover_score(move)) for move in self.neighbours(position)]

    def distance_from_center(self, position: Position) -> float:
        x, y = position
        return math.dist((x, y), (self.center, self.center))


class BattleRoyaleSimulation:
    def __init__(
        self,
        arena_size: int = 30,
        agent_count: int = 12,
        max_steps: int = 400,
        shrink_start: float = 0.4,
        shrink_rate: float = 0.05,
        storm_damage: float = 4.0,
        seed: Optional[int] = None,
    ) -> None:
        self.random = random.Random(seed)
        self.arena = Arena(arena_size, self._default_obstacles(arena_size))
        self.max_steps = max_steps
        self.shrink_start = int(max_steps * shrink_start)
        self.shrink_rate = shrink_rate
        self.storm_damage = storm_damage
        self.agents = self._spawn_agents(agent_count)
        self.history: List[Dict[str, object]] = []

    def _default_obstacles(self, size: int) -> List[Tuple[Position, Position]]:
        """Create a street-like grid with corners and dead ends."""
        margin = size // 8
        corridors = []

        # Perimeter blocks to create dead zones and corners.
        corridors.append(((0, 0), (size - 1, margin // 2)))
        corridors.append(((0, size - 1 - margin // 2), (size - 1, size - 1)))

        # Vertical buildings forming alleyways.
        spacing = size // 5
        for i in range(1, 5):
            x0 = i * spacing - spacing // 3
            x1 = i * spacing + spacing // 3
            corridors.append(((x0, margin), (x1, size - margin)))

        # Horizontal blocks to create intersections and choke points.
        for i in range(1, 4):
            y0 = i * spacing - spacing // 4
            y1 = i * spacing + spacing // 4
            corridors.append(((margin, y0), (size - margin, y1)))

        return corridors

    def _spawn_agents(self, count: int) -> List[Agent]:
        agents: List[Agent] = []
        attempts = 0
        while len(agents) < count and attempts < count * 20:
            attempts += 1
            pos = self.random.randrange(self.arena.size), self.random.randrange(
                self.arena.size
            )
            if self.arena.is_blocked(pos) or any(a.position == pos for a in agents):
                continue
            base_health = self.random.uniform(75, 110)
            attack = self.random.uniform(20, 35)
            defense = self.random.uniform(12, 25)
            vision = self.random.randint(5, 9)
            bravery = self.random.uniform(1.1, 1.45)
            agents.append(
                Agent(
                    identifier=len(agents) + 1,
                    position=pos,
                    health=base_health,
                    attack=attack,
                    defense=defense,
                    vision=vision,
                    bravery_threshold=bravery,
                )
            )
        if len(agents) < count:
            raise RuntimeError("Failed to place all agents without overlap.")
        return agents

    def _find_target(self, agent: Agent, opponents: Iterable[Agent]) -> Optional[Agent]:
        visible = [op for op in opponents if agent.distance_to(op) <= agent.vision]
        if not visible:
            return None
        return min(visible, key=lambda op: agent.distance_to(op))

    def _best_move_towards(self, start: Position, goal: Position) -> Position:
        options = self.arena.neighbours(start)
        if not options:
            return start
        return min(options, key=lambda pos: math.dist(pos, goal))

    def _best_escape_move(
        self, agent: Agent, opponent: Agent, allow_hold: bool = True
    ) -> Position:
        current_distance = agent.distance_to(opponent)
        escape_moves = [
            (pos, cover)
            for pos, cover in self.arena.moves_with_cover(agent.position)
            if math.dist(pos, opponent.position) >= current_distance
        ]
        if allow_hold and math.dist(agent.position, opponent.position) > current_distance:
            escape_moves.append((agent.position, 0))
        if not escape_moves:
            return agent.position
        escape_moves.sort(key=lambda item: (item[0] == agent.position, -item[1]))
        return escape_moves[0][0]

    def _resolve_combat(self, attacker: Agent, defender: Agent) -> None:
        attack_roll = attacker.attack * self.random.uniform(0.8, 1.2)
        defense_roll = defender.defense * self.random.uniform(0.7, 1.1)
        damage = max(4.0, attack_roll - 0.4 * defense_roll)
        defender.health -= damage

        # Counter-attack when defender is cornered or brave.
        if defender.health > 0:
            counter_factor = 0.6 if damage > attacker.health else 0.9
            counter_roll = defender.attack * self.random.uniform(0.6, 1.1)
            counter_damage = max(2.0, counter_factor * counter_roll - attacker.defense * 0.3)
            attacker.health -= counter_damage

    def _storm_radius(self, step: int) -> float:
        if step < self.shrink_start:
            return self.arena.size / math.sqrt(2)
        shrink_steps = step - self.shrink_start
        radius = self.arena.size / math.sqrt(2) - shrink_steps * self.shrink_rate
        return max(radius, self.arena.size * 0.25)

    def _apply_storm(self, step: int) -> None:
        radius = self._storm_radius(step)
        for agent in self.agents:
            if not agent.is_alive():
                continue
            dist = self.arena.distance_from_center(agent.position)
            if dist > radius:
                agent.health -= self.storm_damage

    def step(self, step_index: int) -> None:
        living_agents = [agent for agent in self.agents if agent.is_alive()]
        self.random.shuffle(living_agents)
        intents: Dict[int, Position] = {}

        for agent in living_agents:
            opponents = [op for op in self.agents if op.is_alive() and op is not agent]
            if not opponents:
                intents[agent.identifier] = agent.position
                continue

            target = self._find_target(agent, opponents)
            if target is None:
                # Wander using cover to emulate street sweeping.
                moves = self.arena.moves_with_cover(agent.position)
                if moves:
                    moves.sort(key=lambda item: (-item[1], self.random.random()))
                    intents[agent.identifier] = moves[0][0]
                else:
                    intents[agent.identifier] = agent.position
                agent.intent = "patrol"
                continue

            distance = agent.distance_to(target)
            advantage = (agent.health * agent.attack) / max(
                1.0, target.health * target.defense
            )

            escape_move = self._best_escape_move(agent, target)
            cornered = escape_move == agent.position and all(
                math.dist(move, target.position) < distance
                for move, _ in self.arena.moves_with_cover(agent.position)
            )

            # Decide between fighting, kiting, or hiding.
            if distance <= 1.5 and (advantage >= agent.bravery_threshold or cornered):
                move = self._best_move_towards(agent.position, target.position)
                agent.intent = "engage" if advantage >= agent.bravery_threshold else "desperate"
            elif advantage < agent.bravery_threshold and not cornered:
                move = escape_move
                agent.intent = "retreat"
            else:
                move = self._best_move_towards(agent.position, target.position)
                agent.intent = "shadow"

            intents[agent.identifier] = move

        # Apply moves.
        for agent in living_agents:
            agent.position = intents.get(agent.identifier, agent.position)

        # Resolve combat for agents that ended up adjacent or overlapping.
        engaged_pairs = set()
        for agent in living_agents:
            if not agent.is_alive():
                continue
            for opponent in living_agents:
                if opponent.identifier <= agent.identifier or not opponent.is_alive():
                    continue
                if agent.distance_to(opponent) <= 1.2:
                    pair = (agent.identifier, opponent.identifier)
                    if pair in engaged_pairs:
                        continue
                    engaged_pairs.add(pair)
                    # Determine aggressor based on intent.
                    if agent.intent in {"engage", "desperate"} and opponent.intent != "engage":
                        self._resolve_combat(agent, opponent)
                    elif opponent.intent in {"engage", "desperate"} and agent.intent != "engage":
                        self._resolve_combat(opponent, agent)
                    else:
                        # Mutual skirmish.
                        if self.random.random() < 0.5:
                            self._resolve_combat(agent, opponent)
                        else:
                            self._resolve_combat(opponent, agent)

        self._apply_storm(step_index)

        # Record history for visualization.
        snapshot = {
            "step": step_index,
            "storm_radius": self._storm_radius(step_index),
            "agents": [
                {
                    "id": agent.identifier,
                    "pos": agent.position,
                    "health": max(agent.health, 0),
                    "intent": agent.intent,
                    "alive": agent.is_alive(),
                }
                for agent in self.agents
            ],
        }
        self.history.append(snapshot)

    def run(self) -> int:
        for step in range(self.max_steps):
            alive = [agent for agent in self.agents if agent.is_alive()]
            if len(alive) <= 1:
                break
            self.step(step)
        alive = [agent for agent in self.agents if agent.is_alive()]
        return alive[0].identifier if alive else -1

    def animate(self, interval: int = 200) -> None:
        if plt is None or animation is None:
            raise RuntimeError(
                "Matplotlib is required for visualization. Install it with 'pip install matplotlib'."
            )
        if not self.history:
            raise RuntimeError("Run the simulation before calling animate().")

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xlim(-0.5, self.arena.size - 0.5)
        ax.set_ylim(-0.5, self.arena.size - 0.5)
        ax.set_aspect("equal")
        ax.set_title("Battle Royale Simulation")

        # Draw obstacles once.
        for (x, y), blocked in self.arena.obstacles.items():
            if blocked:
                ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color="dimgray", alpha=0.6))

        scatter = ax.scatter([], [], c=[], cmap="viridis", s=80, vmin=0, vmax=100)
        intents_text = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top")
        storm_circle = plt.Circle((self.arena.center, self.arena.center), 0, fill=False, ls="--")
        ax.add_patch(storm_circle)

        def update(frame: Dict[str, object]):
            agents = frame["agents"]  # type: ignore[index]
            xs = [agent["pos"][0] for agent in agents if agent["alive"]]
            ys = [agent["pos"][1] for agent in agents if agent["alive"]]
            health = [agent["health"] for agent in agents if agent["alive"]]
            scatter.set_offsets(list(zip(xs, ys)))
            scatter.set_array(health)
            intents = ", ".join(
                f"A{agent['id']}:{agent['intent'][0].upper()}({int(agent['health'])})"
                for agent in agents
                if agent["alive"]
            )
            intents_text.set_text(
                f"Step {frame['step']}\nAlive: {len(xs)}\nStorm radius: {frame['storm_radius']:.1f}\n{intents}"
            )
            storm_circle.set_radius(frame["storm_radius"])  # type: ignore[arg-type]
            return scatter, intents_text, storm_circle

        animation.FuncAnimation(
            fig,
            update,
            frames=self.history,
            interval=interval,
            repeat=False,
            blit=False,
        )
        plt.show()


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Battle royale simulation")
    parser.add_argument("--agents", type=int, default=12, help="Number of combatants")
    parser.add_argument("--size", type=int, default=30, help="Arena size (square)")
    parser.add_argument("--steps", type=int, default=400, help="Maximum number of steps")
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=200,
        help="Animation interval in milliseconds",
    )
    parser.add_argument(
        "--no-visual",
        action="store_true",
        help="Run without animation (prints the winner instead)",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = build_argument_parser().parse_args(argv)
    simulation = BattleRoyaleSimulation(
        arena_size=args.size,
        agent_count=args.agents,
        max_steps=args.steps,
        seed=args.seed,
    )
    winner = simulation.run()

    if args.no_visual:
        print(f"Winner: Agent {winner}" if winner != -1 else "No survivors")
    else:
        if plt is None or animation is None:
            raise SystemExit(
                "Matplotlib is not installed. Re-run with --no-visual or install it with 'pip install matplotlib'."
            )
        simulation.animate(interval=args.interval)


if __name__ == "__main__":
    main()
