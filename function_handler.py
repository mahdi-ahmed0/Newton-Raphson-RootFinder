"""Safe parsing and symbolic differentiation for one-variable functions."""
import ast
import sympy as sp

x = sp.Symbol("x")
_ALLOWED_FUNCTIONS = {
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
    "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
    "exp": sp.exp, "log": sp.log, "sqrt": sp.sqrt,
    "Abs": sp.Abs,
}
_ALLOWED_NAMES = {"x": x, "pi": sp.pi, "E": sp.E, **_ALLOWED_FUNCTIONS}
_ALLOWED_AST = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Add, ast.Sub, ast.Mult,
    ast.Div, ast.Pow, ast.Mod, ast.USub, ast.UAdd, ast.Call, ast.Name,
    ast.Load, ast.Constant,
)

def parse_function(expression: str):
    """Parse a user expression such as x**3 - 8*x + 5; ^ is accepted as power."""
    if not expression or not expression.strip():
        raise ValueError("Please enter a function.")
    expression = expression.strip().replace("^", "**")
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Invalid mathematical expression. Check its syntax.") from exc

    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_AST):
            raise ValueError("Unsupported expression element.")
        if isinstance(node, ast.Name) and node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Unsupported name: {node.id}")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_FUNCTIONS:
                raise ValueError("Only supported math functions such as sin, cos, exp, log and sqrt can be used.")
            if node.keywords:
                raise ValueError("Keyword arguments are not supported.")

    try:
        expr = sp.sympify(expression, locals=_ALLOWED_NAMES, evaluate=True)
    except Exception as exc:
        raise ValueError("Could not interpret this function.") from exc

    if not expr.free_symbols.issubset({x}):
        raise ValueError("The function must contain only the variable x.")
    derivative = sp.diff(expr, x)
    return expr, derivative
