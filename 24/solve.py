input_file = "input.txt"


def parse_direction(tile):
    index = 0
    result = []
    while index < len(tile):
        ch = tile[index]
        if ch in ["w", "e"]:
            result.append(ch)
        else:
            index += 1
            result.append(ch + tile[index])
        index += 1
    return result


with open(input_file) as f:
    raw_tile_directions = f.read().strip().split("\n")
    tile_directions = [parse_direction(tile) for tile in raw_tile_directions]


def get_displacement(step):
    if step == "w":
        return (-2, 0)
    if step == "e":
        return (2, 0)
    return [
        1 if "e" in step else -1,
        1 if "n" in step else -1
    ]


black_tiles = set()
for direction in tile_directions:
    coord = [0, 0]
    for step in direction:
        displacement = get_displacement(step)
        coord = [coord[0] + displacement[0], coord[1] + displacement[1]]

    coord = tuple(coord)
    if coord in black_tiles:
        black_tiles.remove(coord)
    else:
        black_tiles.add(coord)


print("Part 1:", len(black_tiles))


def get_neighboors(tile):
    diplacements = map(get_displacement, ["w", "e", "nw", "ne", "sw", "se"])
    for dx, dy in diplacements:
        yield (tile[0] + dx, tile[1] + dy)


def should_flip_black(tile, all_black_tiles):
    black_neighboors = sum(1 for neighboor in get_neighboors(tile) if neighboor in all_black_tiles)
    return black_neighboors == 0 or black_neighboors > 2


def should_flip_white(tile, all_black_tiles):
    black_neighboors = sum(1 for neighboor in get_neighboors(tile) if neighboor in all_black_tiles)
    return black_neighboors == 2


N_STEPS = 100
for step in range(100):
    maybe_flip_black_tiles = set(black_tiles)
    maybe_flip_white_tiles = {
        neighboor
        for black_tile in black_tiles
        for neighboor in get_neighboors(black_tile)
        if neighboor not in black_tiles
    }

    blacks_to_flip = {
        black for black in maybe_flip_black_tiles
        if should_flip_black(black, black_tiles)
    }
    whites_to_flip = {
        white for white in maybe_flip_white_tiles
        if should_flip_white(white, black_tiles)
    }
    black_tiles = (black_tiles - blacks_to_flip) | whites_to_flip


print("Part 2:", len(black_tiles))
