"""Classic 4th-order Runge-Kutta method for solving first-order ODEs."""

from typing import List, Tuple


def rk4_solve(
    f: callable,
    x0: float,
    y0: float,
    h: float,
    steps: int,
) -> List[Tuple[float, float]]:
    """Solve dy/dx = f(x, y) using the classic RK4 method.

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
        k1 = f(x, y)
        k2 = f(x + h / 2, y + h * k1 / 2)
        k3 = f(x + h / 2, y + h * k2 / 2)
        k4 = f(x + h, y + h * k3)

        y = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        x = x + h
        results.append((round(x, 10), y))

    return results
