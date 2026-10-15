import ast
import operator
import re


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


def calculate(command):
    text = command.lower().replace("?", "").strip()

    percent = re.search(r"(\d+(?:\.\d+)?)\s*percent of\s*(\d+(?:\.\d+)?)", text)
    if percent:
        return f"The answer is {float(percent.group(1)) * float(percent.group(2)) / 100:g}."

    if not ("calculate" in text or "what is" in text or "what's" in text):
        return None

    expression = text
    for phrase in ("calculate", "what is", "what's"):
        expression = expression.replace(phrase, "")

    replacements = {
        "multiplied by": "*",
        "times": "*",
        "divided by": "/",
        "plus": "+",
        "minus": "-",
        "to the power of": "**",
    }
    for word, symbol in replacements.items():
        expression = expression.replace(word, symbol)

    expression = expression.strip()

    if not re.fullmatch(r"[0-9.\s+*/()\-]+", expression):
        return None

    try:
        result = evaluate_expression(ast.parse(expression, mode="eval").body)
        return f"The answer is {result:g}."
    except (SyntaxError, ValueError, ZeroDivisionError):
        return "I could not calculate that."


def evaluate_expression(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](evaluate_expression(node.left), evaluate_expression(node.right))

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -evaluate_expression(node.operand)

    raise ValueError("Unsupported calculation")
