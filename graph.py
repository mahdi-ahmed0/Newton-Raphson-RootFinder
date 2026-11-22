"""Plot the function and the Newton-Raphson approximations."""
import numpy as np
import matplotlib.pyplot as plt
from newton_raphson import evaluate_function

def create_graph(expr, rows):
    xs = [row["x"] for row in rows]
    left, right = min(xs), max(xs)
    span = max(right - left, 1.0)
    x_min, x_max = left - 0.8 * span, right + 0.8 * span
    grid = np.linspace(x_min, x_max, 600)

    with np.errstate(all="ignore"):
        ys = evaluate_function(expr, grid)
    ys = np.where(np.isfinite(ys), ys, np.nan)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(grid, ys, label="f(x)", linewidth=2)
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="black", linewidth=1)

    # Iteration approximations are shown on the x-axis.
    ax.scatter(xs, [0] * len(xs), color="crimson", zorder=4, label="Newton-Raphson x values")
    for i, value in enumerate(xs):
        ax.annotate(f"x{i}", (value, 0), xytext=(4, 9), textcoords="offset points", fontsize=8)

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("Newton-Raphson Root Approximation")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    return fig
