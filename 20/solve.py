import collections
import math

input_file = "input.txt"
with open(input_file) as f:
    raw_tiles = f.read().strip().split("\n\n")
    tile_map = {}
    for raw_tile in raw_tiles:
        id_line, *rest = raw_tile.split("\n")
        id = int(id_line[len("Tile "):-1])
        tile_map[id] = list(map(list, rest))


TOP, RIGHT, BOTTOM, LEFT = 0, 1, 2, 3
NOP = lambda x: x


def find_borders(tile):
    return [
        (TOP, tile[0]),
        (RIGHT, [line[-1] for line in tile]),
        (BOTTOM, tile[-1]),
        (LEFT, [line[0] for line in tile]),
    ]


def rotate(tile):  # TOP -> LEFT. (border_id - 1) % 4
    new_tile = [[] for x in range(len(tile[0]))]
    for row in tile:
        for index, pixel in enumerate(reversed(row)):
            new_tile[index].append(pixel)
    return new_tile


def flip(tile):  # RIGHT -> LEFT
    return [list(reversed(row)) for row in tile]


possible_matches = collections.defaultdict(list)
for outer_id, outer_tile in tile_map.items():
    for outer_border_id, outer_border in find_borders(outer_tile):
        possible_matches[(outer_id, outer_border_id)]
        for inner_id, inner_tile in tile_map.items():
            if outer_id == inner_id:
                continue
            for inner_border_id, inner_border in find_borders(inner_tile):
                if outer_border in [inner_border, list(reversed(inner_border))]:
                    possible_matches[(outer_id, outer_border_id)].append((inner_id, inner_border_id))


# This condition greatly simplifies the problem once each side has at most one possible match.
# For this reason we can make a greedy solution instead of combining different possible matches.
assert max(map(len, possible_matches.values())) == 1


# Find tiles with 2 borders without matches to get the corners
no_match_counter = collections.Counter()
for (tile_id, _), matches in possible_matches.items():
    if len(matches) == 0:
        no_match_counter[tile_id] += 1


corners = [tile_id for tile_id, counter in no_match_counter.items() if counter == 2]
assert len(corners) == 4
print("Part 1:", math.prod(corners))


def place_top_left(tile_id):
    no_match_borders = [
        border_id
        for (search_tile_id, border_id), matches in possible_matches.items()
        if search_tile_id == tile_id and len(matches) == 0
    ]
    assert len(no_match_borders) == 2
    while set(no_match_borders) != {TOP, LEFT}:
        tile_map[tile_id] = rotate(tile_map[tile_id])
        no_match_borders = [(no_match_borders[0] - 1) % 4, (no_match_borders[1] - 1) % 4]


def find_matched_tiles(tile_id):
    return {
        match_id
        for border_id in (TOP, RIGHT, BOTTOM, LEFT)
        for match_id, _ in possible_matches[(tile_id, border_id)]
    }


place_top_left(corners[0])
ordered_tiles = [[corners[0]]]
allocated_tiles = {corners[0]}
ALL_COMBINATION_OPERATIONS = [NOP, rotate, rotate, rotate, flip, rotate, rotate, rotate]


def find_next_tile_to_place(placed_tile_id, placed_border_id, candidate_border_id):
    placed_border = find_borders(tile_map[placed_tile_id])[placed_border_id][1]
    for match_candidate_id in find_matched_tiles(placed_tile_id):
        if match_candidate_id in allocated_tiles:
            continue
        for operation in ALL_COMBINATION_OPERATIONS:
            tile_map[match_candidate_id] = operation(tile_map[match_candidate_id])
            candidate_border = find_borders(tile_map[match_candidate_id])[candidate_border_id][1]
            if candidate_border == placed_border:
                return match_candidate_id
    raise Exception("No match")


IMAGE_SIZE = math.sqrt(len(raw_tiles))
while True:
    # Insert next in same row
    match_tile_id = find_next_tile_to_place(
        placed_tile_id=ordered_tiles[-1][-1],
        placed_border_id=RIGHT,
        candidate_border_id=LEFT,
    )

    ordered_tiles[-1].append(match_tile_id)
    allocated_tiles.add(match_tile_id)

    if len(allocated_tiles) == len(raw_tiles):
        break

    if len(ordered_tiles[-1]) == IMAGE_SIZE:
        # Find the tile that matches the bottom border of the first element in the last row
        new_row_tile_id = find_next_tile_to_place(
            placed_tile_id=ordered_tiles[-1][0],
            placed_border_id=BOTTOM,
            candidate_border_id=TOP,
        )
        ordered_tiles.append([new_row_tile_id])  # Next row
        allocated_tiles.add(new_row_tile_id)


# Remove borders
tile_map = {
    tile_id: [
        line[1:-1]
        for line in tile[1:-1]
    ]
    for tile_id, tile in tile_map.items()
}


FULL_IMAGE = []
for row_tile_ids in ordered_tiles:
    n_lines = len(tile_map[row_tile_ids[0]])
    for line_index in range(n_lines):
        FULL_IMAGE.append([])
        for tile_id in row_tile_ids:
            tile = tile_map[tile_id]
            FULL_IMAGE[-1].extend(tile[line_index])


monster_profile = [
    list("                  # "),
    list("#    ##    ##    ###"),
    list(" #  #  #  #  #  #   "),
]
maybe_monster_coord = set()
for op in ALL_COMBINATION_OPERATIONS:
    monster_profile = op(monster_profile)
    for top_left_x in range(len(FULL_IMAGE[0])):
        for top_left_y in range(len(FULL_IMAGE)):

            def can_match(monster_x, monster_y):
                try:
                    return (
                        monster_profile[monster_y][monster_x] != "#" or
                        FULL_IMAGE[top_left_y + monster_y][top_left_x + monster_x] == "#"
                    )
                except IndexError:
                    return False

            match = all(
                can_match(monster_x, monster_y)
                for monster_x in range(len(monster_profile[0]))
                for monster_y in range(len(monster_profile))
            )

            if match:
                maybe_monster_coord.update([
                    (top_left_x + monster_x, top_left_y + monster_y)
                    for monster_x in range(len(monster_profile[0]))
                    for monster_y in range(len(monster_profile))
                    if monster_profile[monster_y][monster_x] == "#"
                ])


print("Part 2:", sum(
    1
    for y in range(len(FULL_IMAGE))
    for x in range(len(FULL_IMAGE[0]))
    if FULL_IMAGE[y][x] == "#" and (x, y) not in maybe_monster_coord
))
