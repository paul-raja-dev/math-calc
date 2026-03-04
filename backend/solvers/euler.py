"""Euler's method for solving first-order ODEs."""

from typing import List, Tuple


def euler_solve(
    f: callable,
    x0: float,
    y0: float,
    h: float,
    steps: int,
) -> List[Tuple[float, float]]:
    """Solve dy/dx = f(x, y) using Euler's method.

    Args:
        f: The derivative function f(x, y).
        x0: Initial x value.
        y0: Initial y value.
        h: Step size.
        steps: Number of steps to compute.

    Returns:
        List of (x, y) tuples including the initial point.
    """
    results: List[Tuple[float, float]] = [(x0, y0)]
    x, y = x0, y0

    for _ in range(steps):
        y = y + h * f(x, y)
        x = x + h
        results.append((round(x, 10), y))

    return results
