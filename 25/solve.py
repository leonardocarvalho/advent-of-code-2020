input_file = "input.txt"
with open(input_file) as f:
    card_public, door_public = list(map(int, f.read().strip().split("\n")))

INITIAL_SUBJECT_NUMBER = 7
DIVISOR = 20201227


def perform_loop(value, subject_number):
    return (value * subject_number) % DIVISOR


def compute_loop_size(public_key, subject_number):
    result = subject_number
    loop_size = 1
    while result != public_key:
        result = perform_loop(result, subject_number)
        loop_size += 1
    return loop_size


card_loop_size = compute_loop_size(card_public, INITIAL_SUBJECT_NUMBER)
door_loop_size = compute_loop_size(door_public, INITIAL_SUBJECT_NUMBER)


result = 1
for x in range(door_loop_size):
    result = perform_loop(result, card_public)

print("Part 1:", result)
