input_file = "input.txt"
with open(input_file) as f:
    cmds = [
        {"action": cmd_line[0], "value": int(cmd_line[1:])}
        for cmd_line in f.read().strip().split("\n")
    ]


def move(value, direction, previous_position):
    base_displacements = {"N": (1, 0), "S": (-1, 0), "E": (0, 1), "W": (0, -1)}
    return (
        previous_position[0] + base_displacements[direction][0] * value,
        previous_position[1] + base_displacements[direction][1] * value,
    )


def compute_new_direction(action, value, current_direction):
    DIRECTION_CONVERSION = {
        "L": {
            "N": "W",
            "S": "E",
            "E": "N",
            "W": "S",
        },
        "R": {
            "N": "E",
            "S": "W",
            "E": "S",
            "W": "N",
        }
    }
    number_of_turns = value // 90
    while number_of_turns > 0:
        current_direction = DIRECTION_CONVERSION[action][current_direction]
        number_of_turns -= 1
    return current_direction


current_direction = "E"
current_position = (0, 0)
for cmd in cmds:
    if cmd["action"] in ("N", "S", "E", "W"):
        current_position = move(cmd["value"], cmd["action"], current_position)
    elif cmd["action"] == "F":
        current_position = move(cmd["value"], current_direction, current_position)
    elif cmd["action"] in ("L", "R"):
        current_direction = compute_new_direction(cmd["action"], cmd["value"], current_direction)
    else:
        raise Exception("Bad Parsing")


print("Part 1:", abs(current_position[0]) + abs(current_position[1]))


def compute_new_waypoint_direction(action, value, waypoint):
    number_of_turns = value // 90
    while number_of_turns > 0:
        if action == "L":
            waypoint = (waypoint[1], -waypoint[0])
        if action == "R":
            waypoint = (-waypoint[1], waypoint[0])
        number_of_turns -= 1
    return waypoint


waypoint = (1, 10)
current_position = (0, 0)
for cmd in cmds:
    if cmd["action"] in ("N", "S", "E", "W"):
        waypoint = move(cmd["value"], cmd["action"], waypoint)
    elif cmd["action"] == "F":
        current_position = (
            current_position[0] + waypoint[0] * cmd["value"],
            current_position[1] + waypoint[1] * cmd["value"],
        )
    elif cmd["action"] in ["L", "R"]:
        waypoint = compute_new_waypoint_direction(cmd["action"], cmd["value"], waypoint)
    else:
        raise Exception("Bad Parsing")

print("Part 2:", abs(current_position[0]) + abs(current_position[1]))
