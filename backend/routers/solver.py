"""API router for ODE solver endpoints."""

from fastapi import APIRouter, HTTPException

from models.schemas import (
    SolveRequest,
    CompareRequest,
    StepResult,
    SolveResponse,
    CompareResponse,
)
from core.parser import parse_equation
from core.error_analysis import compute_error
from solvers.euler import euler_solve
from solvers.rk4 import rk4_solve
from solvers.exact import exact_solve

router = APIRouter()


@router.post("/solve", response_model=SolveResponse)
async def solve(request: SolveRequest):
    """Solve an ODE using the specified numerical method."""
    try:
        f = parse_equation(request.equation)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # Choose solver
    if request.method == "euler":
        raw = euler_solve(f, request.x0, request.y0, request.h, request.steps)
    else:
        raw = rk4_solve(f, request.x0, request.y0, request.h, request.steps)

    # Attempt exact solution for error calculation
    exact_raw = exact_solve(
        request.equation, request.x0, request.y0, request.steps, request.h
    )

    exact_available = exact_raw is not None

    if exact_available:
        errors = compute_error(raw, exact_raw)
        steps = [
            StepResult(x=pt[0], y=pt[1], error=err)
            for pt, err in zip(raw, errors)
        ]
    else:
        steps = [StepResult(x=pt[0], y=pt[1], error=None) for pt in raw]

    return SolveResponse(
        method=request.method,
        steps=steps,
        exact_available=exact_available,
    )


@router.post("/compare", response_model=CompareResponse)
async def compare(request: CompareRequest):
    """Compare Euler and RK4 solutions, with optional exact solution."""
    try:
        f = parse_equation(request.equation)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    euler_raw = euler_solve(f, request.x0, request.y0, request.h, request.steps)
    rk4_raw = rk4_solve(f, request.x0, request.y0, request.h, request.steps)
    exact_raw = exact_solve(
        request.equation, request.x0, request.y0, request.steps, request.h
    )

    if exact_raw is not None:
        euler_errors = compute_error(euler_raw, exact_raw)
        rk4_errors = compute_error(rk4_raw, exact_raw)

        euler_steps = [
            StepResult(x=pt[0], y=pt[1], error=err)
            for pt, err in zip(euler_raw, euler_errors)
        ]
        rk4_steps = [
            StepResult(x=pt[0], y=pt[1], error=err)
            for pt, err in zip(rk4_raw, rk4_errors)
        ]
        exact_steps = [
            StepResult(x=pt[0], y=pt[1], error=0.0)
            for pt in exact_raw
        ]
    else:
        euler_steps = [StepResult(x=pt[0], y=pt[1]) for pt in euler_raw]
        rk4_steps = [StepResult(x=pt[0], y=pt[1]) for pt in rk4_raw]
        exact_steps = None

    return CompareResponse(
        euler=euler_steps,
        rk4=rk4_steps,
        exact=exact_steps,
    )
