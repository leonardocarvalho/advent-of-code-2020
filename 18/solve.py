import math

input_file = "input.txt"
with open(input_file) as f:
    raw_expressions = f.read().strip().split("\n")


def compute_simple_expression_no_precedence(expression):
    elements = expression.split(" ")
    if len(elements) == 1:
        return int(elements)

    while "+" in elements or "*" in elements:
        operator = elements[1]
        e1 = int(elements[0])
        e2 = int(elements[2])
        value = e1 + e2 if operator == "+" else e1 * e2

        elements[0:3] = [str(value)]

    return int(elements[0])

    #result = int(elements[0])
    #operation = elements[1]
    #for element in elements[2:]:
    #    if element in ["+", "*"]:
    #        operation = element
    #    else:
    #        if operation == "+":
    #            result = result + int(element)
    #        else:
    #            result = result * int(element)
    #return result


def compute_complex_expression(expression, simplified_evaluator):
    simplified_expression = ""
    opened_parenthesis = 0
    sub_expression = ""
    for ch in expression:
        if ch == "(":
            if opened_parenthesis > 0:
                sub_expression += ch
            opened_parenthesis += 1
        elif ch == ")":
            opened_parenthesis -= 1
            if opened_parenthesis == 0:
                sub_result = compute_complex_expression(sub_expression, simplified_evaluator)
                simplified_expression += str(sub_result)
                sub_expression = ""
            if opened_parenthesis > 0:
                sub_expression += ch
        else:
            if opened_parenthesis > 0:
                sub_expression += ch
            else:
                simplified_expression += ch

    return simplified_evaluator(simplified_expression)


print(
    "Part 1:",
    sum(
        compute_complex_expression(ex, compute_simple_expression_no_precedence)
        for ex in raw_expressions
    )
)


def compute_simple_expression_plus_precedence(expression):
    elements = expression.split(" ")
    if len(elements) == 1:
        return int(elements[0])

    while "+" in elements:
        index = elements.index("+")
        elements[index - 1:index + 2] = [str(int(elements[index - 1]) + int(elements[index + 1]))]

    return math.prod(int(e) for e in elements if e != "*")

    #def compute_next_plus(expression):
    #    ex_begin = ""
    #    ex_end = ""
    #    p1, p2 = expression.split("+", 1)
    #    if "*" in p1:
    #        p0, p1 = p1.rsplit("*", 1)
    #        ex_begin = p0 + "* "
    #    p1 = int(p1.strip())
    #    if "*" in p2 or "+" in p2:
    #        operator, _ = sorted(["+", "*"], key=lambda op: p2.index(op) if op in p2 else len(p2))
    #        p2, p3 = p2.split(operator, 1)
    #        ex_end = " " + operator + p3
    #    p2 = int(p2.strip())
    #    return ex_begin + str(p1 + p2) + ex_end
    #
    #while "+" in expression:
    #    expression = compute_next_plus(expression)
    #return math.prod([int(element.strip()) for element in expression.split("*")])


print(
    "Part 2:",
    sum(
        compute_complex_expression(ex, compute_simple_expression_plus_precedence)
        for ex in raw_expressions
    )
)
