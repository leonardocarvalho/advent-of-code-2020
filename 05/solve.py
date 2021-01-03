input_file = "input.txt"
with open(input_file) as f:
    boarding_passes = f.read().strip().split("\n")


COLS_INDEX = {"LLL": 0, "LLR": 1, "LRL": 2, "LRR": 3, "RLL": 4, "RLR": 5, "RRL": 6, "RRR": 7}


def compute_pass(b_pass):
    min_row = 0
    max_row = 127

    row_data = b_pass[:7]
    col_data = b_pass[-3:]

    for letter in row_data:
        if letter == "F":
            max_row = (max_row + min_row) // 2
        else:
            min_row = (max_row + min_row) // 2 + 1

    assert min_row == max_row
    return {
        "row": min_row,
        "col": COLS_INDEX[col_data],
        "id": min_row * 8 + COLS_INDEX[col_data],
    }


# Part 1:
max_id = -1
all_ids = []
for b_pass in boarding_passes:
    data = compute_pass(b_pass)
    all_ids.append(data["id"])
    if data["id"] > max_id:
        max_id = data["id"]

print("Part 1:", max_id)

# Part 2
sorted_ids = sorted(all_ids)
for index, id_ in enumerate(sorted_ids, start=sorted_ids[0]):
    if index != id_:
        print("Part 2:", index)
        break
