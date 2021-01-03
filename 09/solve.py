input_file = "input.txt"
PREAMBLE_SIZE = 5 if "test" in input_file else 25
with open(input_file) as f:
    numbers = list(map(int, f.read().strip().split("\n")))


def compute_sums(numbers_to_sum):
    sums = set()
    for x_index, x in enumerate(numbers_to_sum):
        for y in numbers_to_sum[x_index + 1:]:
            sums.add(x + y)
    return sums


invalid_value = None
for index, next_number in enumerate(numbers[PREAMBLE_SIZE:], start=PREAMBLE_SIZE):
    sums = compute_sums(numbers[index - PREAMBLE_SIZE:index])
    if next_number not in sums:
        print("Part 1:", next_number)
        invalid_value = next_number
        break

weakness = None
for start_index, start_value in enumerate(numbers):
    sum_ = start_value
    for index, value in enumerate(numbers[start_index + 1:], start=start_index + 1):
        sum_ += value
        if sum_ == invalid_value:
            min_ = min(numbers[start_index:index + 1])
            max_ = max(numbers[start_index:index + 1])
            weakness = min_ + max_
            break
    if weakness is not None:
        break


print("Part 2:", weakness)
