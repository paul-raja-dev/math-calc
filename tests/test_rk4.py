"""Tests for the RK4 solver – should be much more accurate than Euler."""

import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from solvers.euler import euler_solve
from solvers.rk4 import rk4_solve


def test_rk4_exponential():
    """RK4 with dy/dx = y, y(0) = 1 should closely approximate e^x."""
    f = lambda x, y: y
    results = rk4_solve(f, x0=0, y0=1, h=0.1, steps=5)

    assert len(results) == 6
    assert results[0] == (0, 1)

    # RK4 should be within 0.0001 of e^x at h=0.1
    for x_val, y_val in results:
        exact = math.exp(x_val)
        assert abs(y_val - exact) < 0.0001, (
            f"RK4 value {y_val} too far from exact {exact} at x={x_val}"
        )


def test_rk4_more_accurate_than_euler():
    """RK4 error should be smaller than Euler error at every step."""
    f = lambda x, y: y
    euler_results = euler_solve(f, x0=0, y0=1, h=0.1, steps=5)
    rk4_results = rk4_solve(f, x0=0, y0=1, h=0.1, steps=5)

    for (xe, ye), (xr, yr) in zip(euler_results[1:], rk4_results[1:]):
        exact = math.exp(xe)
        euler_err = abs(ye - exact)
        rk4_err = abs(yr - exact)
        assert rk4_err < euler_err, (
            f"RK4 error ({rk4_err}) >= Euler error ({euler_err}) at x={xe}"
        )


def test_rk4_quadratic():
    """Test RK4 with dy/dx = 2x, y(0) = 0 → exact y = x²."""
    f = lambda x, y: 2 * x
    results = rk4_solve(f, x0=0, y0=0, h=0.1, steps=10)

    for x_val, y_val in results:
        exact = x_val ** 2
        assert abs(y_val - exact) < 1e-10, (
            f"RK4 value {y_val} too far from exact {exact} at x={x_val}"
        )
