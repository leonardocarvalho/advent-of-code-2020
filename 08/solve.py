input_file = "input.txt"


def parse_operation(op_line):
    return {
        "op": op_line[:3],
        "value": (1 if op_line[4] == "+" else -1) * int(op_line[5:])
    }


with open(input_file) as f:
    operations = list(map(parse_operation, f.read().strip().split("\n")))


class InfiniteLoop(Exception):

    def __init__(self, acc_value):
        self.acc = acc_value


def run_code(operations):
    executed_lines = set()
    acc = 0
    current_line = 0
    while current_line < len(operations):
        if current_line in executed_lines:
            raise InfiniteLoop(acc)
        executed_lines.add(current_line)
        operation = operations[current_line]
        if operation["op"] == "nop":
            current_line += 1
        if operation["op"] == "acc":
            acc += operation["value"]
            current_line += 1
        if operation["op"] == "jmp":
            current_line += operation["value"]

    return acc

try:
    run_code(operations)
except InfiniteLoop as e:
    print("Part 1:", e.acc)
else:
    raise Exception("unexpected termination")


for line_to_change in range(len(operations)):
    new_operations = list(operations)
    operation_to_change = new_operations[line_to_change]

    if operation_to_change["op"] == "acc":
        continue

    new_operations[line_to_change] = dict(
        operation_to_change,
        op="jmp" if operation_to_change["op"] == "nop" else "nop",
    )
    try:
        acc = run_code(new_operations)
        print("Part 2:", acc)
        break
    except InfiniteLoop:
        pass
