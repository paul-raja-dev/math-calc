/**
 * chart.js – Chart.js wrapper for rendering ODE solution curves.
 */

/** @type {import('chart.js').Chart | null} */
let currentChart = null;

/**
 * Render solution curves on a Chart.js line chart.
 *
 * @param {string}  canvasId  – ID of the <canvas> element.
 * @param {Array}   eulerData – Array of { x, y } objects (Euler), may be null.
 * @param {Array}   rk4Data   – Array of { x, y } objects (RK4), may be null.
 * @param {Array}   exactData – Array of { x, y } objects (Exact), may be null.
 */
function renderChart(canvasId, eulerData, rk4Data, exactData) {
    // Destroy previous chart instance to prevent canvas reuse errors
    if (currentChart) {
        currentChart.destroy();
        currentChart = null;
    }

    const ctx = document.getElementById(canvasId).getContext("2d");

    const datasets = [];

    if (eulerData && eulerData.length) {
        datasets.push({
            label: "Euler",
            data: eulerData.map((p) => ({ x: p.x, y: p.y })),
            borderColor: "#f59e0b",
            backgroundColor: "rgba(245, 158, 11, 0.15)",
            pointBackgroundColor: "#f59e0b",
            borderWidth: 2,
            pointRadius: 3,
            tension: 0.3,
        });
    }

    if (rk4Data && rk4Data.length) {
        datasets.push({
            label: "RK4",
            data: rk4Data.map((p) => ({ x: p.x, y: p.y })),
            borderColor: "#22d3ee",
            backgroundColor: "rgba(34, 211, 238, 0.15)",
            pointBackgroundColor: "#22d3ee",
            borderWidth: 2,
            pointRadius: 3,
            tension: 0.3,
        });
    }

    if (exactData && exactData.length) {
        datasets.push({
            label: "Exact",
            data: exactData.map((p) => ({ x: p.x, y: p.y })),
            borderColor: "#4ade80",
            backgroundColor: "rgba(74, 222, 128, 0.10)",
            pointBackgroundColor: "#4ade80",
            borderWidth: 2,
            borderDash: [6, 3],
            pointRadius: 3,
            tension: 0.3,
        });
    }

    currentChart = new Chart(ctx, {
        type: "line",
        data: { datasets },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            interaction: { mode: "nearest", intersect: false },
            plugins: {
                legend: {
                    labels: {
                        color: "#e4e4ef",
                        font: { family: "'Inter', sans-serif", size: 12 },
                        usePointStyle: true,
                        pointStyle: "circle",
                    },
                },
                tooltip: {
                    backgroundColor: "rgba(14,14,20,0.9)",
                    titleColor: "#e4e4ef",
                    bodyColor: "#e4e4ef",
                    borderColor: "rgba(167,139,250,0.3)",
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 10,
                },
            },
            scales: {
                x: {
                    type: "linear",
                    title: {
                        display: true,
                        text: "x",
                        color: "#9396a5",
                        font: { family: "'Inter', sans-serif", weight: "600" },
                    },
                    grid: { color: "rgba(255,255,255,0.04)" },
                    ticks: { color: "#9396a5" },
                },
                y: {
                    title: {
                        display: true,
                        text: "y",
                        color: "#9396a5",
                        font: { family: "'Inter', sans-serif", weight: "600" },
                    },
                    grid: { color: "rgba(255,255,255,0.04)" },
                    ticks: { color: "#9396a5" },
                },
            },
        },
    });
}
