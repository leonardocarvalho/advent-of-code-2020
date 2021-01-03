with open("input.txt") as f:
    data = list(map(int, f.read().split()))


for x_index, x in enumerate(data):
    for y in data[x_index + 1:]:
        if x + y == 2020:
            print("Part 1:", x * y)


for x_index, x in enumerate(data):
    for y_index, y in enumerate(data[x_index + 1:], start=x_index + 1):
        for z in data[y_index:]:
            if x + y + z == 2020:
                print("Part 2:", x * y * z)
