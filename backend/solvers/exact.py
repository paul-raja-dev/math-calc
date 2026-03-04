"""Exact (symbolic) ODE solver using SymPy dsolve."""

from typing import List, Optional, Tuple

import sympy
from sympy import Symbol, Function, Eq, sympify, lambdify, dsolve


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

    try:
        # Parse RHS expression
        rhs = sympify(equation_str, locals={"x": x, "y": y(x)})

        # Formulate ODE: y'(x) = rhs
        ode = Eq(y(x).diff(x), rhs)

        # Solve symbolically
        general_solution = dsolve(ode, y(x))

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
        # If sympy cannot solve the ODE, return None
        return None
