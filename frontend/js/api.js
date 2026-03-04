/**
 * api.js – API client for the Numerical ODE Solver backend.
 */

const BASE_URL = "http://localhost:8000/api";

/**
 * Solve an ODE using a single method (Euler or RK4).
 * @param {Object} payload – { equation, x0, y0, h, steps, method }
 * @returns {Promise<Object>} SolveResponse JSON
 */
async function solveSingle(payload) {
  const res = await fetch(`${BASE_URL}/solve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Server error (${res.status})`);
  }

  return res.json();
}

/**
 * Compare Euler and RK4 solutions (plus optional exact).
 * @param {Object} payload – { equation, x0, y0, h, steps }
 * @returns {Promise<Object>} CompareResponse JSON
 */
async function compareBoth(payload) {
  const res = await fetch(`${BASE_URL}/compare`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Server error (${res.status})`);
  }

  return res.json();
}
