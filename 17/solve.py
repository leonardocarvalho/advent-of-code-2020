import copy

input_file = "input.txt"

with open(input_file) as f:
    rows = f.read().strip().split("\n")
    # z, y, x
    grid = [list(map(list, rows))]


displacements = (-1, 0, 1)
NEIGHBOORS_DISPLACEMENTS = {
    (dx, dy, dz)
    for dz in displacements
    for dy in displacements
    for dx in displacements
} - {(0, 0, 0)}


def add_layers(grid):
    # Always keep at least one last layer of inactive cubes
    size_y = len(grid[0])
    size_x = len(grid[0][0])

    return (
        [[["." for x in range(size_x + 2)] for y in range(size_y + 2)]] +
        [
            [["." for x in range(size_x + 2)]] +
            [
                ["."] + row + ["."]
                for row in plane
            ] +
            [["." for x in range(size_x + 2)]]
            for plane in grid
        ] +
        [[["." for x in range(size_x + 2)] for y in range(size_y + 2)]]
    )


def is_active(grid, z, y, x):
    try:
        return grid[z][y][x] == "#"
    except IndexError:
        return False


def perform_cycle(grid):
    new_grid = copy.deepcopy(grid)

    max_z = len(grid)
    max_y = len(grid[0])
    max_x = len(grid[0][0])

    for z in range(max_z):
        for y in range(max_y):
            for x in range(max_x):
                active = is_active(grid, z, y, x)
                active_neighboors = sum(
                    1 for dn in NEIGHBOORS_DISPLACEMENTS
                    if is_active(grid, z + dn[0], y + dn[1], x + dn[2])
                )

                if active and active_neighboors not in (2, 3):
                    new_grid[z][y][x] = "."
                elif not active and active_neighboors == 3:
                    new_grid[z][y][x] = "#"
                else:
                    new_grid[z][y][x] = grid[z][y][x]
    return new_grid


for cycle in range(6):
    grid = add_layers(grid)
    grid = perform_cycle(grid)

active = sum(
    1
    for plane in grid
    for line in plane
    for point in line
    if point == "#"
)
print("Part 1:", active)


with open(input_file) as f:
    rows = f.read().strip().split("\n")
    # w, z, y, x
    grid = [[list(map(list, rows))]]


NEIGHBOORS_DISPLACEMENTS4 = {
    (dw, dy, dz, dx)
    for dw in displacements
    for dz in displacements
    for dy in displacements
    for dx in displacements
} - {(0, 0, 0, 0)}


def add_layers4(grid):
    # Always keep at least one last layer of inactive cubes
    size_z = len(grid[0])
    size_y = len(grid[0][0])
    size_x = len(grid[0][0][0])

    return (
        [[[["." for x in range(size_x + 2)] for y in range(size_y + 2)] for z in range(size_z + 2)]] +
        [
            [[["." for x in range(size_x + 2)] for y in range(size_y + 2)]] +
            [
                [["." for x in range(size_x + 2)]] +
                [
                    ["."] + row + ["."]
                    for row in plane
                ] +
                [["." for x in range(size_x + 2)]]
                for plane in hiper_plane
            ] +
            [[["." for x in range(size_x + 2)] for y in range(size_y + 2)]]
            for hiper_plane in grid
        ] +
        [[[["." for x in range(size_x + 2)] for y in range(size_y + 2)] for z in range(size_z + 2)]]
    )


def is_active4(grid, w, z, y, x):
    try:
        return grid[w][z][y][x] == "#"
    except IndexError:
        return False


def perform_cycle4(grid):
    new_grid = copy.deepcopy(grid)

    max_w = len(grid)
    max_z = len(grid[0])
    max_y = len(grid[0][0])
    max_x = len(grid[0][0][0])

    for w in range(max_w):
        for z in range(max_z):
            for y in range(max_y):
                for x in range(max_x):
                    active = is_active4(grid, w, z, y, x)
                    active_neighboors = sum(
                        1 for dn in NEIGHBOORS_DISPLACEMENTS4
                        if is_active4(grid, w + dn[0], z + dn[1], y + dn[2], x + dn[3])
                    )

                    if active and active_neighboors not in (2, 3):
                        new_grid[w][z][y][x] = "."
                    elif not active and active_neighboors == 3:
                        new_grid[w][z][y][x] = "#"
                    else:
                        new_grid[w][z][y][x] = grid[w][z][y][x]
    return new_grid


for cycle in range(6):
    grid = add_layers4(grid)
    grid = perform_cycle4(grid)


active = sum(
    1
    for hiper_plane in grid
    for plane in hiper_plane
    for line in plane
    for point in line
    if point == "#"
)
print("Part 2:", active)
