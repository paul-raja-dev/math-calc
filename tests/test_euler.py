"""Tests for Euler's method solver."""

import math
import sys
import os

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from solvers.euler import euler_solve


def test_euler_exponential():
    """Test Euler's method with dy/dx = y, y(0) = 1 → exact = e^x.

    Euler's method should approximate e^x with reasonable accuracy at h=0.1.
    """
    f = lambda x, y: y  # dy/dx = y
    results = euler_solve(f, x0=0, y0=1, h=0.1, steps=5)

    # Should have 6 points (initial + 5 steps)
    assert len(results) == 6

    # Verify initial condition
    assert results[0] == (0, 1)

    # Compare each step to e^x – Euler at h=0.1 should be within 0.1 tolerance
    for x_val, y_val in results:
        exact = math.exp(x_val)
        assert abs(y_val - exact) < 0.1, (
            f"Euler value {y_val} too far from exact {exact} at x={x_val}"
        )


def test_euler_linear():
    """Test Euler with dy/dx = 1, y(0) = 0 → exact y = x."""
    f = lambda x, y: 1
    results = euler_solve(f, x0=0, y0=0, h=0.5, steps=4)

    assert len(results) == 5
    for x_val, y_val in results:
        assert abs(y_val - x_val) < 1e-10, (
            f"Expected y={x_val}, got y={y_val}"
        )


def test_euler_step_count():
    """Verify correct number of output points."""
    f = lambda x, y: 0
    results = euler_solve(f, x0=0, y0=5, h=0.1, steps=20)
    assert len(results) == 21
