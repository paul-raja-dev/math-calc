"""Pydantic models for ODE solver API requests and responses."""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class SolveRequest(BaseModel):
    """Request body for solving an ODE with a single method."""

    equation: str = Field(..., description="ODE right-hand side as a string, e.g. 'x + y'")
    x0: float = Field(..., description="Initial x value")
    y0: float = Field(..., description="Initial y value")
    h: float = Field(..., description="Step size")
    steps: int = Field(..., ge=1, description="Number of steps")
    method: Literal["euler", "rk4"] = Field(..., description="Numerical method to use")


class CompareRequest(BaseModel):
    """Request body for comparing Euler and RK4 solutions."""

    equation: str = Field(..., description="ODE right-hand side as a string")
    x0: float = Field(..., description="Initial x value")
    y0: float = Field(..., description="Initial y value")
    h: float = Field(..., description="Step size")
    steps: int = Field(..., ge=1, description="Number of steps")


class StepResult(BaseModel):
    """A single step in the numerical solution."""

    x: float
    y: float
    error: Optional[float] = None


class SolveResponse(BaseModel):
    """Response for a single-method solve request."""

    method: str
    steps: List[StepResult]
    exact_available: bool


class CompareResponse(BaseModel):
    """Response for a compare request (both methods + optional exact)."""

    euler: List[StepResult]
    rk4: List[StepResult]
    exact: Optional[List[StepResult]] = None
