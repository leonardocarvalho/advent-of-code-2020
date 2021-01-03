import collections
import datetime

input_file = "input.txt"
with open(input_file) as f:
    starting_numbers = list(map(int, f.read().strip().split("\n")[0].split(",")))


def compute_turn_number_for_turn(max_turn):
    spoken_turns = {}
    turn = 0
    last_spoken = None
    while turn < max_turn:
        turn += 1
        if turn <= len(starting_numbers):
            last_spoken = starting_numbers[turn - 1]
        else:
            if spoken_turns[last_spoken][0] is None:
                last_spoken = 0
            else:
                last_spoken = spoken_turns[last_spoken][-1] - spoken_turns[last_spoken][-2]
        if last_spoken not in spoken_turns:
            spoken_turns[last_spoken] = (None, turn)
        else:
            spoken_turns[last_spoken] = (spoken_turns[last_spoken][1], turn)

    return last_spoken


print("Part 1:", compute_turn_number_for_turn(2020))
print("Part 2:", compute_turn_number_for_turn(30000000))
