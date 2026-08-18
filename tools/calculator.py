import ast


class _EvalError(Exception):
    pass


_ALLOWED_BINOPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv)
_ALLOWED_UNARYOPS = (ast.UAdd, ast.USub)


def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise _EvalError("Only int/float constants are allowed")

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, _ALLOWED_UNARYOPS):
        val = _eval_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +val
        if isinstance(node.op, ast.USub):
            return -val

    if isinstance(node, ast.BinOp) and isinstance(node.op, _ALLOWED_BINOPS):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op = node.op
        if isinstance(op, ast.Add):
            return left + right
        if isinstance(op, ast.Sub):
            return left - right
        if isinstance(op, ast.Mult):
            return left * right
        if isinstance(op, ast.Div):
            return left / right
        if isinstance(op, ast.Pow):
            return left ** right
        if isinstance(op, ast.Mod):
            return left % right
        if isinstance(op, ast.FloorDiv):
            return left // right

    # Safeguard: disallow names, calls, attributes, subscripts, comprehensions, etc.
    raise _EvalError(f"Unsupported expression node: {type(node).__name__}")


def calculate(expression: str, **kwargs):
    """Safely evaluate a numeric expression and return the result.

    Allowed nodes: int/float constants, + - * / ** % // and unary +/-.
    This intentionally excludes names, function calls, attributes, and other unsafe constructs.
    """
    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree)
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}
