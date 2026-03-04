"""Exact (symbolic) ODE solver using SymPy dsolve."""

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from typing import List, Optional, Tuple

import sympy
from sympy import (
    Symbol, Function, Eq, sympify, lambdify, dsolve,
    sin, cos, tan, exp, log, sqrt, Abs,
    asin, acos, atan, sinh, cosh, tanh,
    sec, csc, cot,
    pi, E as SymE,
    ceiling, floor,
)

# Timeout (seconds) for SymPy's dsolve – prevents hangs on complex ODEs
DSOLVE_TIMEOUT = 10

# Reusable thread pool for dsolve calls
_executor = ThreadPoolExecutor(max_workers=2)


def _run_dsolve(ode, y_func, x_sym):
    """Run dsolve in an isolated call (for use with timeout)."""
    return dsolve(ode, y_func)


def exact_solve(
    equation_str: str,
    x0: float,
    y0: float,
    steps: int,
    h: float,
) -> Optional[List[Tuple[float, float]]]:
    """Attempt to find the exact symbolic solution for dy/dx = f(x, y).

    Args:
        equation_str: Right-hand side of the ODE as a string.
        x0: Initial x value.
        y0: Initial y value.
        steps: Number of steps.
        h: Step size.

    Returns:
        List of (x, y) tuples if an exact solution is found, else None.
    """
    x = Symbol("x")
    y = Function("y")

    # Map common function names so expressions like "sin(x) + y" parse correctly
    local_dict = {
        "x": x, "y": y(x),
        "sin": sin, "cos": cos, "tan": tan,
        "sec": sec, "csc": csc, "cot": cot,
        "asin": asin, "acos": acos, "atan": atan,
        "arcsin": asin, "arccos": acos, "arctan": atan,
        "sinh": sinh, "cosh": cosh, "tanh": tanh,
        "exp": exp, "log": log, "ln": log,
        "sqrt": sqrt, "abs": Abs,
        "ceil": ceiling, "floor": floor,
        "pi": pi, "e": SymE, "E": SymE,
    }

    try:
        # Parse RHS expression
        rhs = sympify(equation_str, locals=local_dict)

        # Formulate ODE: y'(x) = rhs
        ode = Eq(y(x).diff(x), rhs)

        # Solve symbolically with a timeout to avoid long hangs
        future = _executor.submit(_run_dsolve, ode, y(x), x)
        try:
            general_solution = future.result(timeout=DSOLVE_TIMEOUT)
        except (FuturesTimeoutError, Exception):
            future.cancel()
            return None

        # Apply initial condition y(x0) = y0
        constants = general_solution.free_symbols - {x}
        particular = general_solution

        if constants:
            # Solve for arbitrary constants using the initial condition
            const_eqs = [particular.subs(x, x0).subs(y(x0), y0)]
            const_solutions = sympy.solve(const_eqs, list(constants))

            if isinstance(const_solutions, list):
                const_solutions = const_solutions[0] if const_solutions else {}
            if isinstance(const_solutions, tuple):
                const_solutions = dict(zip(constants, const_solutions))

            particular = particular.subs(const_solutions)

        # Extract the RHS of the solved equation y(x) = ...
        y_expr = particular.rhs

        # Convert to a callable
        y_func = lambdify(x, y_expr, modules=["math"])

        # Evaluate at each step
        results: List[Tuple[float, float]] = []
        for i in range(steps + 1):
            xi = x0 + i * h
            xi = round(xi, 10)
            yi = float(y_func(xi))
            results.append((xi, yi))

        return results

    except Exception:
        # If sympy cannot solve the ODE (or times out), return None
        return None
