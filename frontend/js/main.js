/**
 * main.js – Application controller for the Numerical ODE Solver frontend.
 */

(function () {
    "use strict";

    // ── DOM references ──
    const form = document.getElementById("solver-form");
    const solveBtn = document.getElementById("solve-btn");
    const btnText = solveBtn.querySelector(".btn-text");
    const btnLoader = solveBtn.querySelector(".btn-loader");
    const errorMsg = document.getElementById("error-msg");
    const resultsSection = document.getElementById("results-section");
    const tablesContainer = document.getElementById("tables-container");

    // ── Helpers ──

    /** Read all form inputs and return a payload object. */
    function readFormValues() {
        return {
            equation: document.getElementById("equation").value.trim(),
            x0: parseFloat(document.getElementById("x0").value),
            y0: parseFloat(document.getElementById("y0").value),
            h: parseFloat(document.getElementById("h").value),
            steps: parseInt(document.getElementById("steps").value, 10),
            method: document.getElementById("method").value,
        };
    }

    /** Simple client-side validation. Returns error string or null. */
    function validate(v) {
        if (!v.equation) return "Equation is required.";
        if (isNaN(v.x0)) return "x₀ must be a number.";
        if (isNaN(v.y0)) return "y₀ must be a number.";
        if (isNaN(v.h) || v.h <= 0) return "Step size h must be a positive number.";
        if (isNaN(v.steps) || v.steps < 1) return "Steps must be at least 1.";
        return null;
    }

    function showError(msg) {
        errorMsg.textContent = msg;
        errorMsg.hidden = false;
    }

    function hideError() {
        errorMsg.hidden = true;
    }

    function setLoading(on) {
        solveBtn.disabled = on;
        btnText.hidden = on;
        btnLoader.hidden = !on;
    }

    /** Format a number for display (6 decimal places). */
    function fmt(n) {
        if (n == null) return "—";
        return Number(n).toFixed(6);
    }

    /** Build an HTML table from an array of StepResults. */
    function buildTable(title, steps) {
        const hasError = steps.some((s) => s.error != null);

        let html = `<p class="table-title">${title}</p>`;
        html += `<table class="results-table"><thead><tr>
      <th>Step</th><th>x</th><th>y</th>${hasError ? "<th>Error</th>" : ""}
    </tr></thead><tbody>`;

        steps.forEach((s, i) => {
            html += `<tr>
        <td>${i}</td>
        <td>${fmt(s.x)}</td>
        <td>${fmt(s.y)}</td>
        ${hasError ? `<td>${fmt(s.error)}</td>` : ""}
      </tr>`;
        });

        html += "</tbody></table>";
        return html;
    }

    // ── Main handler ──

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        hideError();

        const values = readFormValues();
        const err = validate(values);
        if (err) {
            showError(err);
            return;
        }

        setLoading(true);
        resultsSection.hidden = true;

        try {
            if (values.method === "compare") {
                // Compare both methods
                const { equation, x0, y0, h, steps } = values;
                const data = await compareBoth({ equation, x0, y0, h, steps });

                // Tables
                let tablesHTML = buildTable("Euler Method", data.euler);
                tablesHTML += buildTable("Runge-Kutta 4", data.rk4);
                if (data.exact) {
                    tablesHTML += buildTable("Exact Solution", data.exact);
                }
                tablesContainer.innerHTML = tablesHTML;

                // Chart
                renderChart(
                    "solution-chart",
                    data.euler,
                    data.rk4,
                    data.exact || null
                );
            } else {
                // Single method
                const data = await solveSingle(values);

                tablesContainer.innerHTML = buildTable(
                    data.method === "euler" ? "Euler Method" : "Runge-Kutta 4",
                    data.steps
                );

                // Chart – place single method in the correct slot
                const isEuler = data.method === "euler";
                renderChart(
                    "solution-chart",
                    isEuler ? data.steps : null,
                    isEuler ? null : data.steps,
                    null
                );
            }

            resultsSection.hidden = false;
            resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
        } catch (error) {
            showError(error.message || "An unexpected error occurred.");
        } finally {
            setLoading(false);
        }
    });
})();
