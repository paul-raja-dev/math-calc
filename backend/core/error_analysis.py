"""Error analysis utilities for comparing numerical solutions."""

from typing import List, Tuple, Dict


def compute_error(
    approx: List[Tuple[float, float]],
    exact: List[Tuple[float, float]],
) -> List[float]:
    """Compute point-by-point absolute errors between approximate and exact solutions.

    Args:
        approx: List of (x, y) tuples from the numerical method.
        exact: List of (x, y) tuples from the exact solution.

    Returns:
        List of absolute error values |y_approx - y_exact| at each step.
    """
    errors = []
    for (_, y_a), (_, y_e) in zip(approx, exact):
        errors.append(abs(y_a - y_e))
    return errors


def compute_error_stats(errors: List[float]) -> Dict[str, float]:
    """Compute summary statistics for a list of errors.

    Returns:
        Dict with max_error, mean_error, and final_error.
    """
    if not errors:
        return {"max_error": 0.0, "mean_error": 0.0, "final_error": 0.0}

    return {
        "max_error": max(errors),
        "mean_error": sum(errors) / len(errors),
        "final_error": errors[-1],
    }
