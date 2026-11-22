import streamlit as st
import pandas as pd
import sympy as sp

from function_handler import parse_function
from newton_raphson import solve_newton_raphson
from graph import create_graph

st.set_page_config(page_title="Newton-Raphson Root Finder", page_icon="∑", layout="wide")
st.title("Newton-Raphson Root Finder")
st.caption("Numerical Methods — Solution of Nonlinear Equations")
st.write(
    "Enter a nonlinear function f(x), an initial guess x₀, and a tolerance. "
    "The app differentiates the function and applies the Newton-Raphson iteration."
)

with st.form("solver_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        function_text = st.text_input("Function f(x)", value="x^3 - 8*x + 5",
                                      help="Examples: x^3 - 8*x + 5, exp(-x)-x, sin(x)-0.5")
    with col2:
        x0 = st.number_input("Initial guess (x₀)", value=0.0, format="%.8f")
    with col3:
        tolerance = st.number_input("Tolerance", min_value=0.00000001,
                                    value=0.0001, format="%.8f")
    max_iterations = st.number_input("Maximum iterations", min_value=1, max_value=1000,
                                      value=100, step=1)
    submitted = st.form_submit_button("Calculate Root", type="primary")

if submitted:
    try:
        expr, derivative = parse_function(function_text)
        rows, converged, message = solve_newton_raphson(
            expr, derivative, x0, tolerance, int(max_iterations)
        )

        st.subheader("Function details")
        c1, c2 = st.columns(2)
        c1.latex(r"f(x) = " + sp.latex(expr))
        c2.latex(r"f'(x) = " + sp.latex(derivative))

        last = rows[-1]
        st.subheader("Result")
        m1, m2, m3 = st.columns(3)
        m1.metric("Approximate root", f"{last['x']:.10g}")
        m2.metric("Iterations", str(len(rows) - 1))
        m3.metric("|f(root)|", f"{abs(last['f(x)']):.3e}")

        if converged:
            st.success(message)
        else:
            st.warning(message)

        st.subheader("Iteration table")
        display_rows = []
        for row in rows:
            derivative_at_x = row["f'(x)"]
            display_rows.append({
                "Iteration": row["Iteration"],
                "x": f"{row['x']:.10g}",
                "f(x)": f"{row['f(x)']:.5e}",
                "f'(x)": f"{derivative_at_x:.5e}",
                "Error": "—" if row["Error"] is None else f"{row['Error']:.5e}",
            })
        st.dataframe(pd.DataFrame(display_rows), use_container_width=True, hide_index=True)

        st.subheader("Function graph and iteration points")
        fig = create_graph(expr, rows)
        st.pyplot(fig, use_container_width=True)
        st.caption("The red markers show the successive x approximations on the x-axis.")

        csv = pd.DataFrame(rows).to_csv(index=False).encode("utf-8")
        st.download_button("Download iteration results (CSV)", csv,
                           file_name="newton_raphson_results.csv", mime="text/csv")
    except Exception as exc:
        st.error(str(exc))

with st.expander("How the method works"):
    st.latex(r"x_{i+1}=x_i-\frac{f(x_i)}{f'(x_i)}")
    st.write("The iteration continues until |x(i+1) − x(i)| is smaller than the selected tolerance, "
             "or the maximum iteration count is reached. The residual |f(x)| is also displayed.")
    st.info("Supported functions include sin, cos, tan, exp, log, sqrt, sinh, cosh and abs (Abs). "
            "Use * for multiplication, ** or ^ for powers, and x as the variable.")
