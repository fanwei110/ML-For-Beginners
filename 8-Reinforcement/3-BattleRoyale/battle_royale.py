"""Battle Royale simulation with human-like agents.

This module provides a grid-based environment populated with AI agents that
behave in a human-inspired, risk-averse style. Agents roam a city-like map with
streets, alleys, and dead-ends, preferring to disengage unless they hold a
meaningful advantage or are trapped.  The simulation is intended for teaching
and experimentation purposes and keeps the implementation dependency-light.

Example
-------
>>> from battle_royale import BattleRoyaleEnvironment
>>> env = BattleRoyaleEnvironment(grid_size=25, num_agents=12, seed=7)
>>> report = env.run(verbose=True)
>>> env.render_animation("battle.gif", dpi=100)

The resulting GIF shows the progression of the match and the textual report
contains a step-by-step log.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
import random
from typing import Dict, List, Optional, Sequence, Tuple

try:  # Optional visualisation dependencies
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
except ModuleNotFoundError:  # pragma: no cover - handled gracefully later
    plt = None
    mcolors = None

try:  # Optional numerical dependency
    import numpy as np
except ModuleNotFoundError:  # pragma: no cover - handled gracefully later
    np = None


Position = Tuple[int, int]
Direction = Tuple[int, int]

CARDINAL_DIRECTIONS: Tuple[Direction, ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))
DIAGONAL_DIRECTIONS: Tuple[Direction, ...] = ((1, 1), (1, -1), (-1, 1), (-1, -1))


@dataclass
class SkillProfile:
    """Defines optional skills that add heterogeneity to agents."""

    name: str
    cooldown: int
    last_used: int = field(default=-999)

    def ready(self, current_time: int) -> bool:
        return current_time - self.last_used >= self.cooldown

    def trigger(self, current_time: int) -> None:
        self.last_used = current_time


@dataclass
class Agent:
    """State and behaviour parameters for a single agent."""

    identifier: int
    position: Position
    health: float
    max_health: float
    attack_power: float
    armor: float
    vision_range: int
    base_speed: int
    attack_range: int
    aggression: float
    caution: float
    bravery_threshold: float
    skills: Sequence[SkillProfile]
    preferred_distance: Tuple[int, int]
    is_alive: bool = True
    score: float = 0.0

    def danger_aversion(self) -> float:
        """Combines aggression and caution into an avoidance scalar."""

        return max(0.1, self.caution - self.aggression * 0.5)

    def wants_engagement(self, advantage: float) -> bool:
        """Returns True if the agent is willing to fight given an advantage score."""

        if advantage >= self.bravery_threshold:
            return True
        # If severely injured and cornered, the agent fights back.
        if self.health < self.max_health * 0.25 and advantage > -self.bravery_threshold:
            return True
        return False


@dataclass
class ActionLog:
    tick: int
    actor: int
    action: str
    detail: str


class BattleRoyaleEnvironment:
    """Encapsulates the simulated city map and the agents inside it."""

    def __init__(
        self,
        grid_size: int = 25,
        num_agents: int = 10,
        num_blocks: int = 8,
        seed: Optional[int] = None,
        time_limit: int = 250,
        shrink_rate: float = 0.15,
        safe_radius_floor: int = 3,
        agent_params: Optional[Sequence[Dict[str, float]]] = None,
    ) -> None:
        self.grid_size = grid_size
        self.num_blocks = num_blocks
        self.rng = random.Random(seed)
        self.time_limit = time_limit
        self.shrink_rate = shrink_rate
        self.safe_radius_floor = safe_radius_floor
        self.tick = 0
        self.history: List[List[List[int]]] = []
        self.logs: List[ActionLog] = []
        self.grid = self._generate_city_map()
        self.open_tiles = {(x, y) for x in range(grid_size) for y in range(grid_size) if self.grid[x][y] == 0}
        self.agents: List[Agent] = []

        params = agent_params or [{} for _ in range(num_agents)]
        if len(params) != num_agents:
            raise ValueError("agent_params must match num_agents if provided")

        for identifier, overrides in enumerate(params, start=1):
            self.agents.append(self._create_agent(identifier, overrides))

        if len({agent.position for agent in self.agents}) != len(self.agents):
            raise RuntimeError("Agents spawned on top of one another; try another seed or adjust map size")

    # ------------------------------------------------------------------
    # Map generation and geometry helpers
    # ------------------------------------------------------------------
    def _generate_city_map(self) -> List[List[int]]:
        """Create a grid with blocky buildings, alleys, and dead-ends."""

        grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        margin = 2

        def carve_rectangle(x0: int, y0: int, w: int, h: int) -> None:
            x1 = min(self.grid_size - margin, x0 + w)
            y1 = min(self.grid_size - margin, y0 + h)
            for i in range(x0, x1):
                for j in range(y0, y1):
                    grid[i][j] = 1

        # Place rectangular buildings.
        for _ in range(self.num_blocks):
            width = self.rng.randint(max(2, self.grid_size // 6), max(3, self.grid_size // 4))
            height = self.rng.randint(max(2, self.grid_size // 6), max(3, self.grid_size // 4))
            x = self.rng.randint(margin, self.grid_size - width - margin)
            y = self.rng.randint(margin, self.grid_size - height - margin)
            carve_rectangle(x, y, width, height)

        # Carve alleyways forming dead-ends by removing narrow strips.
        for _ in range(self.num_blocks // 2):
            corridor_length = self.rng.randint(self.grid_size // 3, self.grid_size - margin)
            horizontal = self.rng.choice([True, False])
            if horizontal:
                x = self.rng.randint(margin, self.grid_size - margin - 1)
                max_start = self.grid_size - margin - corridor_length
                if max_start < margin:
                    continue
                y_start = self.rng.randint(margin, max_start)
                for i in range(x, min(self.grid_size, x + 2)):
                    for j in range(y_start, min(self.grid_size, y_start + corridor_length)):
                        grid[i][j] = 0
                if self.rng.random() < 0.6:
                    for i in range(x, min(self.grid_size, x + 2)):
                        for j in range(max(margin, y_start + corridor_length - 2), min(self.grid_size, y_start + corridor_length)):
                            grid[i][j] = 1
            else:
                y = self.rng.randint(margin, self.grid_size - margin - 1)
                max_start = self.grid_size - margin - corridor_length
                if max_start < margin:
                    continue
                x_start = self.rng.randint(margin, max_start)
                for i in range(x_start, min(self.grid_size, x_start + corridor_length)):
                    for j in range(y, min(self.grid_size, y + 2)):
                        grid[i][j] = 0
                if self.rng.random() < 0.6:
                    for i in range(max(margin, x_start + corridor_length - 2), min(self.grid_size, x_start + corridor_length)):
                        for j in range(y, min(self.grid_size, y + 2)):
                            grid[i][j] = 1

        # Add sparse debris for cover.
        for _ in range(self.grid_size * 2):
            x = self.rng.randrange(self.grid_size)
            y = self.rng.randrange(self.grid_size)
            if grid[x][y] == 0 and self.rng.random() < 0.2:
                grid[x][y] = 2
        return grid

    def _create_agent(self, identifier: int, overrides: Dict[str, float]) -> Agent:
        spawn = self.rng.choice(list(self.open_tiles))
        self.open_tiles.remove(spawn)

        base = dict(
            health=self.rng.uniform(70, 120),
            attack_power=self.rng.uniform(12, 20),
            armor=self.rng.uniform(0.1, 0.4),
            vision_range=self.rng.randint(4, 7),
            base_speed=1,
            attack_range=self.rng.randint(1, 2),
            aggression=self.rng.uniform(0.3, 0.7),
            caution=self.rng.uniform(0.6, 0.95),
            bravery_threshold=self.rng.uniform(5, 15),
        )
        base.update(overrides)

        skill_pool = [
            SkillProfile("dash", cooldown=6),
            SkillProfile("medkit", cooldown=8),
            SkillProfile("grenade", cooldown=7),
        ]
        skills = self.rng.sample(skill_pool, k=self.rng.randint(1, len(skill_pool)))
        preferred_distance = (
            self.rng.randint(2, 4),
            self.rng.randint(4, 7),
        )
        return Agent(
            identifier=identifier,
            position=spawn,
            health=base["health"],
            max_health=base["health"],
            attack_power=base["attack_power"],
            armor=base["armor"],
            vision_range=int(base["vision_range"]),
            base_speed=int(base["base_speed"]),
            attack_range=int(base["attack_range"]),
            aggression=float(base["aggression"]),
            caution=float(base["caution"]),
            bravery_threshold=float(base["bravery_threshold"]),
            skills=skills,
            preferred_distance=preferred_distance,
        )

    # ------------------------------------------------------------------
    # Simulation entry points
    # ------------------------------------------------------------------
    def run(self, verbose: bool = False) -> Dict[str, object]:
        """Simulate until a single agent remains or the time limit elapses."""

        self.history.clear()
        self.logs.clear()
        self.tick = 0
        while self.tick < self.time_limit and self.alive_agents_count > 1:
            self.history.append(self._snapshot())
            order = self.agents_in_random_order
            for agent in order:
                if agent.is_alive:
                    self._step_agent(agent)
            self.apply_zone_damage()
            self.tick += 1

        self.history.append(self._snapshot())
        summary = {
            "winner": self._winner_id,
            "ticks": self.tick,
            "log": list(self.logs),
        }
        if verbose:
            for entry in self.logs:
                print(f"[{entry.tick:03d}] Agent {entry.actor}: {entry.action} - {entry.detail}")
            if summary["winner"] is None:
                print("No winner before the timer expired.")
            else:
                print(f"Winner: Agent {summary['winner']} in {summary['ticks']} ticks")
        return summary

    @property
    def alive_agents_count(self) -> int:
        return sum(agent.is_alive for agent in self.agents)

    @property
    def agents_in_random_order(self) -> List[Agent]:
        order = [agent for agent in self.agents if agent.is_alive]
        self.rng.shuffle(order)
        return order

    @property
    def _winner_id(self) -> Optional[int]:
        alive = [agent.identifier for agent in self.agents if agent.is_alive]
        return alive[0] if len(alive) == 1 else None

    def _snapshot(self) -> List[List[int]]:
        grid = [[-1 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                grid[x][y] = self.grid[x][y]
        for agent in self.agents:
            if agent.is_alive:
                grid[agent.position[0]][agent.position[1]] = agent.identifier + 2
        return grid

    # ------------------------------------------------------------------
    # Core agent behaviour
    # ------------------------------------------------------------------
    def _step_agent(self, agent: Agent) -> None:
        visible_enemies = self._visible_enemies(agent)
        self._maybe_use_skills(agent, visible_enemies)

        in_range = [enemy for enemy in visible_enemies if self._distance(agent.position, enemy.position) <= agent.attack_range]
        if in_range:
            target = self._select_target(agent, in_range)
            advantage = agent.health - target.health
            target_trapped = self._is_trapped(target)
            if agent.wants_engagement(advantage) or target_trapped:
                self._attack(agent, target)
                return

        move = self._choose_movement(agent, visible_enemies)
        if move is not None:
            self._move_agent(agent, move)
        elif visible_enemies:
            # Forced to engage despite the odds.
            target = self._select_target(agent, visible_enemies)
            self._attack(agent, target)

    def _maybe_use_skills(self, agent: Agent, enemies: Sequence[Agent]) -> None:
        for skill in agent.skills:
            if not skill.ready(self.tick):
                continue
            if skill.name == "medkit" and agent.health < agent.max_health * 0.55:
                heal_amount = 15
                agent.health = min(agent.max_health, agent.health + heal_amount)
                skill.trigger(self.tick)
                self._log(agent.identifier, "heal", f"used medkit (+{heal_amount:.0f} HP)")
            elif skill.name == "dash" and enemies:
                retreat = self._best_retreat(agent, enemies)
                if retreat:
                    agent.position = retreat
                    skill.trigger(self.tick)
                    self._log(agent.identifier, "dash", "sprinted to safer cover")
                    return
            elif skill.name == "grenade" and enemies:
                target = self._select_target(agent, enemies)
                if self._distance(agent.position, target.position) <= agent.vision_range:
                    damage = 10
                    target.health -= damage
                    skill.trigger(self.tick)
                    self._log(agent.identifier, "grenade", f"threw grenade at Agent {target.identifier} (-{damage:.0f} HP)")
                    if target.health <= 0:
                        self._kill(target, attacker=agent)

    def _choose_movement(self, agent: Agent, enemies: Sequence[Agent]) -> Optional[Position]:
        candidates = self._legal_moves(agent)
        if not candidates:
            return None

        if enemies:
            # Evaluate positions for disengagement.
            scores = []
            for option in candidates:
                score = self._score_retreat_position(agent, option, enemies)
                scores.append((score, option))
            scores.sort(reverse=True)
            best_score, best_option = scores[0]
            if best_score > 0:
                return best_option

        # Exploratory movement searching for better loot/opportunities.
        urgency = self.tick / max(1, self.time_limit)
        target_point = self._shrinking_zone_center
        scores = []
        for option in candidates:
            dist_to_center = self._distance(option, target_point)
            entropy = self.rng.random() * 0.5
            score = -dist_to_center + entropy + urgency
            scores.append((score, option))
        scores.sort(reverse=True)
        return scores[0][1]

    def _legal_moves(self, agent: Agent) -> List[Position]:
        moves = []
        for dx, dy in CARDINAL_DIRECTIONS:
            nx, ny = agent.position[0] + dx, agent.position[1] + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and self.grid[nx][ny] == 0:
                if not any(other.is_alive and other.position == (nx, ny) for other in self.agents):
                    moves.append((nx, ny))
        return moves

    def _score_retreat_position(self, agent: Agent, option: Position, enemies: Sequence[Agent]) -> float:
        min_dist = min(self._distance(option, enemy.position) for enemy in enemies)
        min_pref, max_pref = agent.preferred_distance
        distance_score = 0.0
        if min_dist < min_pref:
            distance_score = - (min_pref - min_dist) * agent.danger_aversion()
        elif min_dist > max_pref:
            distance_score = - (min_dist - max_pref) * 0.1
        cover_bonus = sum(1 for dx, dy in CARDINAL_DIRECTIONS if self._is_cover(option, (dx, dy)))
        choke_penalty = 1 if self._is_dead_end(option) else 0
        safe_zone_score = -self._zone_pressure(option)
        return distance_score + cover_bonus - choke_penalty + safe_zone_score

    def _best_retreat(self, agent: Agent, enemies: Sequence[Agent]) -> Optional[Position]:
        options = self._legal_moves(agent)
        if not options:
            return None
        scored = [(self._score_retreat_position(agent, opt, enemies), opt) for opt in options]
        scored.sort(reverse=True)
        if scored and scored[0][0] > 0:
            return scored[0][1]
        return None

    def _is_cover(self, position: Position, direction: Direction) -> bool:
        nx, ny = position[0] + direction[0], position[1] + direction[1]
        if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
            return self.grid[nx][ny] in (1, 2)
        return True

    def _is_dead_end(self, position: Position) -> bool:
        exits = 0
        for dx, dy in CARDINAL_DIRECTIONS:
            nx, ny = position[0] + dx, position[1] + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and self.grid[nx][ny] == 0:
                exits += 1
        return exits <= 1

    def _is_trapped(self, agent: Agent) -> bool:
        return self._is_dead_end(agent.position) and not self._legal_moves(agent)

    def _visible_enemies(self, agent: Agent) -> List[Agent]:
        enemies = []
        for other in self.agents:
            if other is agent or not other.is_alive:
                continue
            dist = self._distance(agent.position, other.position)
            if dist <= agent.vision_range and self._has_line_of_sight(agent.position, other.position):
                enemies.append(other)
        return enemies

    def _has_line_of_sight(self, start: Position, end: Position) -> bool:
        x0, y0 = start
        x1, y1 = end
        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            return True
        for step in range(1, steps):
            t = step / steps
            x = round(x0 + dx * t)
            y = round(y0 + dy * t)
            if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
                return False
            if self.grid[x][y] == 1:
                return False
        return True

    def _select_target(self, agent: Agent, enemies: Sequence[Agent]) -> Agent:
        # Prefer the weakest visible opponent or one already cornered.
        def score(enemy: Agent) -> Tuple[int, float]:
            return (
                1 if self._is_trapped(enemy) else 0,
                -enemy.health,
            )

        return sorted(enemies, key=score, reverse=True)[0]

    def _attack(self, agent: Agent, target: Agent) -> None:
        damage = max(1.0, agent.attack_power * (1 - target.armor))
        target.health -= damage
        agent.score += damage
        self._log(agent.identifier, "attack", f"hit Agent {target.identifier} for {damage:.1f}")
        if target.health <= 0:
            self._kill(target, attacker=agent)

    def _kill(self, target: Agent, attacker: Optional[Agent] = None) -> None:
        target.is_alive = False
        if attacker is not None:
            attacker.score += 25
            self._log(attacker.identifier, "eliminate", f"defeated Agent {target.identifier}")
        else:
            self._log(target.identifier, "eliminate", "was eliminated by the zone")

    def _move_agent(self, agent: Agent, new_position: Position) -> None:
        agent.position = new_position
        self._log(agent.identifier, "move", f"relocated to {new_position}")

    def _log(self, actor: int, action: str, detail: str) -> None:
        self.logs.append(ActionLog(self.tick, actor, action, detail))

    # ------------------------------------------------------------------
    # Zone pressure mechanics
    # ------------------------------------------------------------------
    @property
    def _shrinking_zone_center(self) -> Position:
        return (self.grid_size // 2, self.grid_size // 2)

    def _zone_radius(self) -> float:
        return max(self.safe_radius_floor, self.grid_size / 2 - self.tick * self.shrink_rate)

    def _zone_pressure(self, position: Position) -> float:
        cx, cy = self._shrinking_zone_center
        dist = self._distance(position, (cx, cy))
        radius = self._zone_radius()
        if dist <= radius:
            return 0.0
        return (dist - radius) * 0.5

    def apply_zone_damage(self) -> None:
        for agent in self.agents:
            if not agent.is_alive:
                continue
            pressure = self._zone_pressure(agent.position)
            if pressure <= 0:
                continue
            damage = pressure
            agent.health -= damage
            if agent.health <= 0:
                self._kill(agent)

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------
    @staticmethod
    def _distance(a: Position, b: Position) -> float:
        return math.dist(a, b)

    def render_frame(self, index: int):
        """Return a matplotlib Figure for a given historical frame."""

        if plt is None or mcolors is None:
            raise RuntimeError("matplotlib is required for rendering frames")

        state = self.history[index]
        cmap = mcolors.ListedColormap([
            "#1b2838",  # walls/buildings (1)
            "#6c757d",  # debris/cover (2)
            "#0b5ed7",  # agent bodies (>=2)
            "#111111",  # background placeholder
        ])
        flat_max = max(max(row) for row in state)
        norm = mcolors.BoundaryNorm([-1, 0, 1, 2, flat_max + 2], cmap.N)
        fig, ax = plt.subplots(figsize=(6, 6))
        if np is not None:
            data = np.array(state).T
        else:
            data = [list(row) for row in zip(*state)]
        ax.imshow(data, cmap=cmap, norm=norm, origin="lower")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"Tick {index}")

        # Draw shrinking safe zone.
        circle = plt.Circle(self._shrinking_zone_center, self._zone_radius(), color="white", fill=False, linestyle="--", linewidth=1.2)
        ax.add_patch(circle)

        return fig

    def render_animation(self, output_path: str, dpi: int = 80) -> None:
        if not self.history:
            raise RuntimeError("Run the simulation before rendering")
        if plt is None or mcolors is None:
            raise RuntimeError("matplotlib is required for rendering animations")
        if np is None:
            raise RuntimeError("numpy is required for GIF export")
        frames = []
        for i in range(len(self.history)):
            fig = self.render_frame(i)
            fig.canvas.draw()
            frames.append(np.array(fig.canvas.renderer.buffer_rgba()))
            plt.close(fig)
        self._save_gif(frames, output_path, dpi=dpi)

    def _save_gif(self, frames: Sequence["np.ndarray"], output_path: str, dpi: int) -> None:
        try:
            import imageio.v3 as iio
        except ModuleNotFoundError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("imageio is required for GIF export") from exc

        fps = max(1, min(10, len(frames) // max(1, self.time_limit // 10)))
        iio.imwrite(output_path, frames, extension=".gif", fps=fps)


__all__ = ["BattleRoyaleEnvironment", "Agent", "SkillProfile", "ActionLog"]
