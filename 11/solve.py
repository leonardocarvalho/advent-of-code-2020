import copy
input_file = "input.txt"

original_seat_mapping = []
with open(input_file) as f:
    for row in f.read().strip().split("\n"):
        original_seat_mapping.append([])
        for col in row:
            original_seat_mapping[-1].append(col)


def perform_step_rule(mapping, is_occupied_rule, max_adjacent):
    STEP_COMBINATIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    new_state = copy.deepcopy(mapping)
    max_row_index = len(mapping) - 1
    max_col_index = len(mapping[0]) - 1

    for row_index, row in enumerate(mapping):
        for col_index, col in enumerate(row):
            adjacent_occupied = sum(
                1
                for comb in STEP_COMBINATIONS
                if is_occupied_rule(comb, row_index, col_index)
            )
            if mapping[row_index][col_index] == "#" and adjacent_occupied >= max_adjacent:
                new_state[row_index][col_index] = "L"
            elif mapping[row_index][col_index] == "L" and adjacent_occupied == 0:
                new_state[row_index][col_index] = "#"

    return new_state


def perform_step_rule1(mapping):
    max_row_index = len(mapping) - 1
    max_col_index = len(mapping[0]) - 1

    def is_occupied(combination, row_index, col_index):
        comb_row = row_index + combination[0]
        comb_col = col_index + combination[1]

        if comb_row < 0 or comb_row > max_row_index or comb_col < 0 or comb_col >  max_col_index:
            return False
        return mapping[comb_row][comb_col] == "#"

    return perform_step_rule(mapping, is_occupied, 4)


stable = False
seat_mapping = copy.deepcopy(original_seat_mapping)
while not stable:
    next_state = perform_step_rule1(seat_mapping)
    stable = next_state == seat_mapping
    seat_mapping = next_state

print("Part 1:", sum(1 for row in seat_mapping for col in row if col == "#"))


def perform_step_rule2(mapping):
    max_row_index = len(mapping) - 1
    max_col_index = len(mapping[0]) - 1

    def is_direction_occupied(combination, row_index, col_index):
        comb_row = row_index + combination[0]
        comb_col = col_index + combination[1]

        if comb_row < 0 or comb_row > max_row_index or comb_col < 0 or comb_col >  max_col_index:
            return False
        if mapping[comb_row][comb_col] == ".":
            return is_direction_occupied(combination, comb_row, comb_col)
        return mapping[comb_row][comb_col] == "#"

    return perform_step_rule(mapping, is_direction_occupied, 5)


stable = False
seat_mapping = copy.deepcopy(original_seat_mapping)
while not stable:
    next_state = perform_step_rule2(seat_mapping)
    stable = next_state == seat_mapping
    seat_mapping = next_state

print("Part 2:", sum(1 for row in seat_mapping for col in row if col == "#"))
