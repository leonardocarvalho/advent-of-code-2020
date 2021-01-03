import re

with open("input.txt") as f:
    lines = f.read().split("\n")

# Part 1
valid = 0
for line in lines:
    if not line: continue
    result = re.match(r"(\d+)-(\d+) ([a-z]): ([a-z]+)", line)
    min_, max_, ch, password = result.groups()
    count = sum(1 for c in password if c == ch)
    valid += int(int(min_) <= count <= int(max_))
print("Part 1:", valid)


# Part 2
valid = 0
for line in lines:
    if not line: continue
    result = re.match(r"(\d+)-(\d+) ([a-z]): ([a-z]+)", line)
    pos1, pos2, ch, password = result.groups()
    ch1, ch2 = password[int(pos1) - 1], password[int(pos2) - 1]
    valid += int((ch1 == ch) ^ (ch2 == ch))
print("Part 2:", valid)
