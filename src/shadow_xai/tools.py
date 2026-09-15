"""Allowlisted tools with validation, timeout, and audit records."""

import ast
import operator
import time
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    handler: Callable[[str], str]
    timeout: float = 3.0


class SafeCalculator:
    OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}

    def __call__(self, expression: str) -> str:
        def evaluate(node: ast.AST) -> float:
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            if isinstance(node, ast.UnaryOp) and type(node.op) in self.OPS:
                return self.OPS[type(node.op)](evaluate(node.operand))
            if isinstance(node, ast.BinOp) and type(node.op) in self.OPS:
                return self.OPS[type(node.op)](evaluate(node.left), evaluate(node.right))
            raise ValueError("only numeric arithmetic is allowed")
        tree = ast.parse(expression, mode="eval")
        return str(evaluate(tree.body))


class ToolRegistry:
    def __init__(self, allowed: set[str] | None = None) -> None:
        self.tools: dict[str, ToolSpec] = {}
        self.allowed = allowed if allowed is not None else set()
        self.audit: list[dict[str, Any]] = []

    def register(self, spec: ToolSpec) -> None:
        self.tools[spec.name] = spec

    def call(self, name: str, argument: str) -> str:
        started = time.time(); status = "ok"
        if name not in self.tools or (self.allowed and name not in self.allowed):
            raise PermissionError(f"tool not allowed: {name}")
        spec = self.tools[name]
        try:
            with ThreadPoolExecutor(max_workers=1) as pool:
                result = pool.submit(spec.handler, argument).result(timeout=spec.timeout)
            return str(result)
        except Exception:
            status = "error"
            raise
        finally:
            self.audit.append({"tool": name, "status": status, "duration_ms": round((time.time()-started)*1000, 2)})

    def describe(self) -> list[dict[str, str]]:
        return [{"name": x.name, "description": x.description} for x in self.tools.values() if not self.allowed or x.name in self.allowed]


def default_registry() -> ToolRegistry:
    registry = ToolRegistry(allowed={"calculator"})
    registry.register(ToolSpec("calculator", "Evaluate safe numeric arithmetic", SafeCalculator()))
    return registry
