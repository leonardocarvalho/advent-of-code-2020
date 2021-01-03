import collections
input_file = "input.txt"


def parse_answers():
    with open(input_file) as f:
        data = f.read().split("\n")
        group_info = ""
        for line in data:
            if line:
                group_info += " " + line
            else:
                yield group_info
                group_info = ""


# Part 1
count = 0
for group_info in parse_answers():
    single_ans = set(group_info) - {" "}
    count += len(single_ans)
print("Part 1:", count)


# Part 2:
count = 0
for group_info in parse_answers():
    group_counter = collections.Counter()
    people_answers = list(filter(None, group_info.split(" ")))
    number_people = len(people_answers)
    for ans in people_answers:
        group_counter.update(ans)
    for v in group_counter.values():
        if v == number_people:
            count += 1
print("Part 2:", count)
