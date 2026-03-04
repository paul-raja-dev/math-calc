"""FastAPI application entry point for the Numerical ODE Solver."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.solver import router as solver_router

app = FastAPI(
    title="Numerical ODE Solver",
    description="Solve first-order ODEs using Euler's method, RK4, and exact symbolic solutions.",
    version="1.0.0",
)

# CORS – fully open for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include solver router under /api prefix
app.include_router(solver_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Numerical ODE Solver API – visit /docs for interactive documentation."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
