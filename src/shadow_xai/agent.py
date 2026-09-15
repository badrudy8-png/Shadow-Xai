"""Small, bounded agent orchestration layer."""

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class AgentResult:
    goal: str
    steps: tuple[str, ...]
    completed: bool
    error: str = ""


class Agent:
    def __init__(self, max_steps: int = 5, retries: int = 1) -> None:
        self.max_steps, self.retries = max_steps, retries

    def plan(self, goal: str) -> list[str]:
        clean = goal.strip()
        if not clean:
            raise ValueError("goal must not be empty")
        return [f"Understand goal: {clean}", "Execute approved actions", "Verify completion"]

    def run(self, goal: str, executor: Callable[[str], str] | None = None) -> AgentResult:
        steps = self.plan(goal)[:self.max_steps]
        executor = executor or (lambda step: step)
        completed_steps: list[str] = []
        try:
            for step in steps:
                for attempt in range(self.retries + 1):
                    try:
                        completed_steps.append(executor(step))
                        break
                    except Exception:
                        if attempt == self.retries:
                            raise
            return AgentResult(goal, tuple(completed_steps), bool(completed_steps))
        except Exception as error:
            return AgentResult(goal, tuple(completed_steps), False, str(error))
