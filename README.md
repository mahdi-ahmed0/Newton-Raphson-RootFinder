# Newton-Raphson Root Finder

A basic Python application for approximating roots of nonlinear equations using the Newton-Raphson method from the Numerical Methods lecture.

## Features
- Accepts a function `f(x)` and initial guess `x0`.
- Automatically calculates the first derivative using SymPy.
- Iterates using `x_(i+1) = x_i - f(x_i)/f'(x_i)`.
- Displays each iteration, approximation, function value, derivative, error, and total iteration count.
- Stops when `|x_(i+1) - x_i| < tolerance` or the maximum iteration count is reached.
- Plots the function and successive x approximations.
- Handles invalid expressions, near-zero derivatives, and iteration limits.
- Exports the iteration table as CSV.

## Requirements
Python 3.10 or newer is recommended.

## Installation
```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run
```bash
streamlit run main.py
```
Open the local URL printed by Streamlit in your browser.

## Input syntax
Use `x` as the variable. Examples:
- `x^3 - 8*x + 5`
- `x^4 - 11*x + 8`
- `exp(-x) - x`
- `sin(x) - 0.5`

Supported functions: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, `cosh`, `tanh`, `exp`, `log`, `sqrt`, and `Abs`. Use `*` for multiplication. Both `^` and `**` are accepted for powers.

## Test
```bash
python -m unittest discover -s tests -v
```

## Mathematical method
The Newton-Raphson update is:
`x_(i+1) = x_i - f(x_i)/f'(x_i)`.

The project uses the lecture-style step-size stopping condition:
`|x_(i+1) - x_i| < tolerance`.
It also displays `|f(x)|` so the user can inspect how close the result is to a zero of the function. A small step alone is not an absolute guarantee of a true root; interpret the residual too.

## Team roles (5 members)
1. Mathematics and validation: verify the formula and lecture examples.
2. Function processing: parse input and differentiate (`function_handler.py`).
3. Numerical engine: implement iterations (`newton_raphson.py`).
4. Graph: plot function and iteration points (`graph.py`).
5. Interface and integration: Streamlit UI and final integration (`main.py`).

## Submission checklist
- [ ] Run all unit tests.
- [ ] Test the lecture examples with their initial guesses.
- [ ] Test invalid input and a zero derivative.
- [ ] Confirm the graph and iteration table are visible.
- [ ] Add all five team members' actual names and academic IDs to the course form.
