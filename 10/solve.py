MAX_DIFF = 3
input_file = "input.txt"
with open(input_file) as f:
    adapters = sorted(map(int, f.read().strip().split("\n")))
    adapters.append(adapters[-1] + 3)


differences = {1: 0, 2: 0, 3: 0}
jolt_value = 0
for adapter in adapters:
    differences[adapter - jolt_value] += 1
    jolt_value = adapter

print("Part 1:", differences[1] * differences[3])

adapters = [0] + adapters
combinations_smaller_than = {0: 1}


def compute_combinations_smaller_than(value):
    if value in combinations_smaller_than:
        return combinations_smaller_than[value]
    combinations = 0
    index = adapters.index(value)
    while index - 1 >= 0 and value - adapters[index - 1] <= MAX_DIFF:
        combinations += compute_combinations_smaller_than(adapters[index - 1])
        index -= 1
    combinations_smaller_than[value] = combinations
    return combinations


combinations = compute_combinations_smaller_than(adapters[-1])
print("Part 2:", combinations)
