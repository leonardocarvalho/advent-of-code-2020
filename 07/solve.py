import re
import collections

input_file = "input.txt"
with open(input_file) as f:
    text_rules = f.read().strip().split("\n")

parent_mapping = collections.defaultdict(list)
children_mapping = {}

for rule in text_rules:
    container_color = re.match(r"(.*)? bags contain", rule).group(1)
    all_contained = re.findall(r"\d+ .*? bag", rule)
    contained_colors = [re.match(r"(\d+) (.*)? bag", c).groups() for c in all_contained]

    if container_color not in children_mapping:
        children_mapping[container_color] = {}

    for quant, contained in contained_colors:
        parent_mapping[contained].append(container_color)
        children_mapping[container_color][contained] = int(quant)


def find_parents(color):
    all_parents = set()
    for parent in parent_mapping[color]:
        all_parents.add(parent)
        all_parents.update(find_parents(parent))
    return all_parents


def find_number_of_bags(color):
    total_inner_bags = 0
    for child_color, quantity in children_mapping.get(color, {}).items():
        total_inner_bags += quantity * find_number_of_bags(child_color)
    return 1 + total_inner_bags


desired_bag = "shiny gold"
all_parents = find_parents(desired_bag)
print("Part 1:", len(all_parents))

number_of_bags = find_number_of_bags(desired_bag)
# -1 to exclude the gold shiny itself
print("Part 2:", number_of_bags - 1)
