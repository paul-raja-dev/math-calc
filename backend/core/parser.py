"""Parse ODE equation strings into callable Python functions using SymPy."""

import sympy
from sympy import (
    symbols, sympify, lambdify,
    sin, cos, tan, exp, log, sqrt, Abs,
    asin, acos, atan, sinh, cosh, tanh,
    sec, csc, cot,
    pi, E,
    ceiling, floor,
)


def parse_equation(equation_str: str) -> callable:
    """Parse a string equation into a callable f(x, y).

    Supports common math functions: sin, cos, tan, exp, log, ln, sqrt, abs,
    asin, acos, atan, sinh, cosh, tanh, sec, csc, cot, and constants pi, e.

    Args:
        equation_str: A mathematical expression string,
            e.g. "x + y", "sin(x) + log(y)", "exp(-x**2)".

    Returns:
        A callable that accepts (x, y) and returns the evaluated expression.

    Raises:
        ValueError: If the expression cannot be parsed or contains invalid symbols.
    """
    if not equation_str or not equation_str.strip():
        raise ValueError("Equation cannot be empty.")

    x, y = symbols("x y")
    allowed_symbols = {x, y}

    # Map common function names and constants that users may type
    local_dict = {
        # Variables
        "x": x, "y": y,
        # Trigonometric
        "sin": sin, "cos": cos, "tan": tan,
        "sec": sec, "csc": csc, "cot": cot,
        # Inverse trigonometric
        "asin": asin, "acos": acos, "atan": atan,
        "arcsin": asin, "arccos": acos, "arctan": atan,
        # Hyperbolic
        "sinh": sinh, "cosh": cosh, "tanh": tanh,
        # Exponential & logarithmic
        "exp": exp, "log": log, "ln": log,
        # Roots & absolute value
        "sqrt": sqrt, "abs": Abs,
        # Rounding
        "ceil": ceiling, "floor": floor,
        # Constants
        "pi": pi, "e": E, "E": E,
    }

    try:
        expr = sympify(equation_str, locals=local_dict)
    except (sympy.SympifyError, SyntaxError, TypeError) as exc:
        raise ValueError(
            f"Invalid equation '{equation_str}': {exc}"
        ) from exc

    # Ensure only x, y (and constants) appear
    free = expr.free_symbols
    if not free.issubset(allowed_symbols):
        unexpected = free - allowed_symbols
        raise ValueError(
            f"Equation contains unexpected symbols: {unexpected}. "
            f"Only 'x' and 'y' are allowed."
        )

    f = lambdify(["x", "y"], expr, modules=["math"])
    return f
