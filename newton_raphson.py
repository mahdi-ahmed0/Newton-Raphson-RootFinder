"""Newton-Raphson numerical solver."""
import math
import numpy as np
import sympy as sp

def solve_newton_raphson(expr, derivative, x0, tolerance=1e-4, max_iterations=100):
    """
    Returns (rows, status, message).
    The course stopping criterion is |x_(n+1) - x_n| < tolerance.
    Residual |f(x)| is also recorded as a diagnostic.
    """
    if tolerance <= 0:
        raise ValueError("Tolerance must be greater than zero.")
    if max_iterations < 1:
        raise ValueError("Maximum iterations must be at least 1.")

    f = sp.lambdify(sp.Symbol("x"), expr, modules=["numpy"])
    df = sp.lambdify(sp.Symbol("x"), derivative, modules=["numpy"])

    def evaluate(func, value, label):
        try:
            result = float(func(value))
        except Exception as exc:
            raise ValueError(f"Could not evaluate {label} at x = {value}.") from exc
        if not math.isfinite(result):
            raise ValueError(f"{label} is not finite at x = {value}.")
        return result

    current = float(x0)
    f_current = evaluate(f, current, "f(x)")
    rows = [{
        "Iteration": 0, "x": current, "f(x)": f_current,
        "f'(x)": evaluate(df, current, "f'(x)"), "Error": None
    }]

    if abs(f_current) < tolerance:
        return rows, True, "The initial guess already satisfies the function tolerance."

    for iteration in range(1, max_iterations + 1):
        derivative_value = evaluate(df, current, "f'(x)")
        if abs(derivative_value) < 1e-14:
            return rows, False, "Derivative is zero or too close to zero; iteration stopped."

        next_x = current - f_current / derivative_value
        if not math.isfinite(next_x):
            return rows, False, "The iteration produced a non-finite value."
        next_f = evaluate(f, next_x, "f(x)")
        error = abs(next_x - current)
        next_derivative = evaluate(df, next_x, "f'(x)")

        rows.append({
            "Iteration": iteration, "x": next_x, "f(x)": next_f,
            "f'(x)": next_derivative, "Error": error
        })

        if error < tolerance:
            return rows, True, "Converged: |x_new - x_old| is below the tolerance."

        current, f_current = next_x, next_f

    return rows, False, f"Maximum number of iterations ({max_iterations}) reached."

def evaluate_function(expr, values):
    f = sp.lambdify(sp.Symbol("x"), expr, modules=["numpy"])
    return np.asarray(f(values), dtype=float)
