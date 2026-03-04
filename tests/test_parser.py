"""Tests for the equation parser."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from core.parser import parse_equation


def test_parse_simple_expression():
    """parse_equation('x + y') should return a callable."""
    f = parse_equation("x + y")
    assert callable(f)


def test_parse_correct_value():
    """f(1, 1) should equal 2.0 for 'x + y'."""
    f = parse_equation("x + y")
    assert f(1, 1) == 2.0


def test_parse_complex_expression():
    """Test a more complex expression: x**2 + sin(y)."""
    import math

    f = parse_equation("x**2 + sin(y)")
    result = f(2, math.pi / 2)
    expected = 4.0 + 1.0  # 2² + sin(π/2) = 5
    assert abs(result - expected) < 1e-10


def test_parse_invalid_expression():
    """Invalid expressions should raise ValueError."""
    with pytest.raises(ValueError):
        parse_equation("invalid$$expr")


def test_parse_empty_string():
    """Empty string should raise ValueError."""
    with pytest.raises(ValueError):
        parse_equation("")
