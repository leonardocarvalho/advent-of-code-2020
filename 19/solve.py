import re

input_file = "input.txt"
with open(input_file) as f:
    raw_rules, raw_messages = f.read().strip().split("\n\n")

    text_rules = raw_rules.split("\n")
    messages = raw_messages.split("\n")

    rule_map = {}
    for text_rule in text_rules:
        rule_number, text_rule = text_rule.split(":")
        if '"' in text_rule:
            rule_map[rule_number] = {
                "type": "base",
                "data": re.search("([a-z]+)", text_rule).group(1),
            }
        else:
            rule_map[rule_number] = {
                "type": "composite",
                "data": [
                    [sub_rule for sub_rule in rule.strip().split(" ")]
                    for rule in text_rule.split(" | ")
                ]
            }


cache = {}
# FTR: I don't think this code can process any grammar...
# I was lucky because:
#   1. The provided grammar doesn't accept empty messages
#   2. The rule loop doesn't have the same rule as the first element
# Both of the issues can be fixed with current approach, but in this case it is not worthy
def match_rule(message, rule_ids):
    if len(rule_ids) == 1:
        if (message, rule_ids[0]) in cache:
            return cache[(message, rule_ids[0])]
        rule = rule_map[rule_ids[0]]
        if rule["type"] == "base":
            return message == rule["data"]
        is_a_match = any(
            match_rule(message, rule_set)
            for rule_set in rule["data"]
        )
        cache[(message, rule_ids[0])] = is_a_match
        return is_a_match

    return any((
        match_rule(message[:index], rule_ids[:1]) and
        match_rule(message[index:], rule_ids[1:])
    ) for index in range(len(message) + 1))


print("Part 1:", sum(1 for m in messages if match_rule(m, ["0"])))


rule_map["8"]["data"].append(["42", "8"])
rule_map["11"]["data"].append(["42", "11", "31"])
cache = {}


print("Part 2:", sum(1 for m in messages if match_rule(m, ["0"])))
