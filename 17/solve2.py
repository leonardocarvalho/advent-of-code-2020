import copy
import collections

input_file = "test_input.txt"
BASE_DISPLACEMENTS = (-1, 0, 1)


def create_multi_dimensional_space(dimensions):
    if dimensions == 0:
        return {
            "space": ".",
            "dimensions": dimensions,
        }
    return {
        "space": collections.defaultdict(lambda: create_multi_dimensional_space(dimensions - 1)),
        "dimensions": dimensions,
    }


def get_point(space, coord):
    if space["dimensions"] == 0:
        return space["space"]
    return get_point(space["space"][coord[0]], coord[1:])


def set_point(space, coord, value):
    if space["dimensions"] == 1:
        space["space"][coord[0]]["space"] = value
        return
    set_point(space["space"][coord[0]], coord[1:], value)


def feed_space_with(space, input_file):
    with open(input_file) as f:
        rows = f.read().strip().split("\n")
    grid = list(map(list, rows))

    origin_two_dimensional = space
    for _ in range(space["dimensions"] - 2):
        origin_two_dimensional = origin_two_dimensional["space"][0]
    assert origin_two_dimensional["dimensions"] == 2

    for y, line in enumerate(grid):
        for x, point in enumerate(line):
            set_point(origin_two_dimensional, [y, x], point)


def compute_active(space):
    if space["dimensions"] == 0:
        return int(space["space"] == "#")
    return sum(compute_active(subspace) for subspace in space["space"].values())


def create_multi_dimensional_neighboors_displacements(dimensions):
    if dimensions == 0:
        return [[]]
    sub_displacements = create_multi_dimensional_neighboors_displacements(dimensions - 1)
    return [
        [d] + sub
        for d in BASE_DISPLACEMENTS
        for sub in sub_displacements
    ]


def traverse_space(space):
    if space["dimensions"] == 0:
        yield [], space["space"]
        return

    #### Attetion
    # This two lines are not right. New spaces are created empty, while the should
    # keep the range of values already visited for that dimension
    min_visited_value = min(space["space"].keys())
    max_visited_value = max(space["space"].keys())
    for space_coord in range(min_visited_value - 1, max_visited_value + 2):
        for coord, value in traverse_space(space["space"][space_coord]):
            yield [space_coord] + coord, value


def perform_cycle(space, neighboors_displacements):
    new_space = copy.deepcopy(space)

    for coord, value in traverse_space(space):
        active = value == "#"
        active_neighboors = sum(
            1 for dn in neighboors_displacements
            if get_point(space, [x + dx for x, dx in zip(coord, dn)]) == "#"
        )

        if active and active_neighboors not in (2, 3):
            value_to_set = "."
        elif not active and active_neighboors == 3:
            value_to_set = "#"
        else:
            value_to_set = value
        set_point(new_space, coord, value_to_set)

    return new_space


for index, dimensions in enumerate([3, 4], start=1):
    space = create_multi_dimensional_space(dimensions)
    neighboors_displacements = create_multi_dimensional_neighboors_displacements(dimensions)
    neighboors_displacements = [
        d for d in neighboors_displacements if not all(x == 0 for x in d)
    ]
    feed_space_with(space, input_file)
    for _ in range(6):
        space = perform_cycle(space, neighboors_displacements)

    active = compute_active(space)
    print("Part {}:".format(index), active)
