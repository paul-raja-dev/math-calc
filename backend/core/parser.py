"""Parse ODE equation strings into callable Python functions using SymPy."""

import sympy
from sympy import symbols, sympify, lambdify


def parse_equation(equation_str: str) -> callable:
    """Parse a string equation into a callable f(x, y).

    Args:
        equation_str: A mathematical expression string, e.g. "x + y", "x**2 - y".

    Returns:
        A callable that accepts (x, y) and returns the evaluated expression.

    Raises:
        ValueError: If the expression cannot be parsed or contains invalid symbols.
    """
    x, y = symbols("x y")
    allowed_symbols = {x, y}

    try:
        expr = sympify(equation_str, locals={"x": x, "y": y})
    except (sympy.SympifyError, SyntaxError, TypeError) as exc:
        raise ValueError(
            f"Invalid equation '{equation_str}': {exc}"
        ) from exc

    # Ensure only x, y (and constants) appear
    free = expr.free_symbols
    if not free.issubset(allowed_symbols):
        unexpected = free - allowed_symbols
        raise ValueError(
            f"Equation contains unexpected symbols: {unexpected}. Only 'x' and 'y' are allowed."
        )

    f = lambdify(["x", "y"], expr, modules=["math"])
    return f
