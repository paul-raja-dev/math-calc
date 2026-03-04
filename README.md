# Numerical ODE Solver

A full-stack web application for solving first-order ordinary differential equations numerically using **Euler's method** and the **4th-order Runge-Kutta (RK4)** method, with optional exact symbolic solutions via SymPy.

![Stack](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Stack](https://img.shields.io/badge/SymPy-3B5526?style=flat&logo=sympy&logoColor=white)
![Stack](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chartdotjs&logoColor=white)

---

## Features

- **Euler's Method** – simple first-order numerical solver
- **RK4 Method** – classic 4th-order Runge-Kutta for high accuracy
- **Exact Solutions** – SymPy-powered symbolic solving with initial conditions
- **Error Analysis** – point-by-point comparison against exact solutions
- **Interactive Chart** – visualize all curves on one Chart.js graph
- **Compare Mode** – run both methods side-by-side

---

## Quick Start

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### 2. Frontend

Simply open `frontend/index.html` in your browser. No build step required.

### 3. Run Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

---

## API Endpoints

### `POST /api/solve`

Solve an ODE using a single method.

**Request:**

```json
{
  "equation": "x + y",
  "x0": 0,
  "y0": 1,
  "h": 0.1,
  "steps": 10,
  "method": "euler"
}
```

**Response:**

```json
{
  "method": "euler",
  "steps": [
    { "x": 0.0, "y": 1.0, "error": 0.0 },
    { "x": 0.1, "y": 1.1, "error": 0.003428 },
    ...
  ],
  "exact_available": true
}
```

### `POST /api/compare`

Compare Euler and RK4 (with optional exact solution).

**Request:**

```json
{
  "equation": "x + y",
  "x0": 0,
  "y0": 1,
  "h": 0.1,
  "steps": 10
}
```

**Response:**

```json
{
  "euler": [ { "x": 0.0, "y": 1.0, "error": 0.0 }, ... ],
  "rk4":   [ { "x": 0.0, "y": 1.0, "error": 0.0 }, ... ],
  "exact":  [ { "x": 0.0, "y": 1.0, "error": 0.0 }, ... ]
}
```

---

## Example Input

| Field    | Value   |
|----------|---------|
| Equation | `x + y` |
| x₀       | `0`     |
| y₀       | `1`     |
| h        | `0.1`   |
| Steps    | `10`    |

---

## Project Structure

```
numerical-ode-solver/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── requirements.txt
│   ├── routers/solver.py     # /solve and /compare endpoints
│   ├── solvers/              # euler.py, rk4.py, exact.py
│   ├── core/                 # parser.py, error_analysis.py
│   └── models/schemas.py     # Pydantic models
├── frontend/
│   ├── index.html            # Single-page UI
│   ├── style.css             # Dark theme
│   └── js/                   # api.js, chart.js, main.js
├── tests/                    # pytest test suite
├── .gitignore
└── README.md
```

---

## License

MIT
