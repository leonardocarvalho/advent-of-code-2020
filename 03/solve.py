with open("input.txt") as f:
    tree_map = f.read().strip().split("\n")

width = len(tree_map[0])

# Part 1:
n_trees = 0
col = 0
for line in tree_map[1:]:
    col = (col + 3) % width
    n_trees += int(line[col] == "#")
print("Part 1:", n_trees)


# Part 2:
slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
prod = 1
for right, down in slopes:
    n_trees = 0
    col = 0
    for line in tree_map[down:][::down]:
        col = (col + right) % width
        n_trees += int(line[col] == "#")
    prod *= n_trees
print("Part 2:", prod)
