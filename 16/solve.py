# The solution to this problem still case use some iteration for more complex inputs.
# Examples of more complex cases:
#  1. invalid tickets because 2 values both match a single rule (or 3 values matching 2 rules...)
#  2. At some moment there's an index of the ticket that could (apparently) have more than 1 possible match (a search would be necessary)

input_file = "input.txt"
with open(input_file) as f:
    rules_part, my_ticket_part, nearby_tickets_part = f.read().strip().split("\n\n")

    rules = []
    for line in rules_part.split("\n"):
        field_name, raw_ranges = line.split(":")
        ranges = [r.strip() for r in raw_ranges.split("or")]
        rules.append({
            "field":  field_name,
            "ranges": [
                {"start": int(r.split("-")[0]), "end": int(r.split("-")[1])}
                for r in ranges
            ]
        })

    my_ticket = list(map(int, my_ticket_part.split("\n")[1].split(",")))
    nearby_tickets = [
        list(map(int, line.split(",")))
        for line in nearby_tickets_part.split("\n")[1:]
    ]


def is_impossible_value(rule, value):
    return all(
        not (range_["start"] <= value <= range_["end"])
        for range_ in rule["ranges"]
    )


problematic_values = [
    value
    for ticket in nearby_tickets
    for value in ticket
    if all(is_impossible_value(rule, value) for rule in rules)
]
print("Part 1:", sum(problematic_values))


valid_nearby_tickets = [
    ticket
    for ticket in nearby_tickets
    if not any(
        all(is_impossible_value(rule, value) for rule in rules)
        for value in ticket
    )
]


def compute_possible_rules(tickets, index):
    return [
        rule
        for rule in rules
        if all(
            not is_impossible_value(rule, ticket[index])
            for ticket in tickets
        )
    ]

possible_rules_by_position = [{
    "position": index,
    "rules": compute_possible_rules(valid_nearby_tickets, index),
} for index in range(len(my_ticket))]
possible_rules_by_position.sort(key=lambda v: len(v["rules"]))

# Easy input try:
fixed_rules_with_positions = {}
while len(fixed_rules_with_positions) < len(rules):
    next_set = [
        rule
        for rule in possible_rules_by_position[0]["rules"]
        if rule not in fixed_rules_with_positions.values()
    ]
    assert len(next_set) == 1  # Could this not be true? :thinking_face:
    fixed_rules_with_positions[possible_rules_by_position[0]["position"]] = next_set[0]
    possible_rules_by_position = possible_rules_by_position[1:]

departure_indexes = [
    position
    for position, rule in fixed_rules_with_positions.items()
    if rule["field"].startswith("departure")
]
result = 1
for index in departure_indexes:
    result *= my_ticket[index]
print("Part 2:", result)


#
