import collections

input_file = "input.txt"


class NoMatch(Exception): pass


labels = []
with open(input_file) as f:
    raw_labels = f.read().strip().split("\n")
    for label in raw_labels:
        raw_ingredients, raw_allergens = label.split("(")
        ingredients = raw_ingredients.strip().split(" ")
        allergens = raw_allergens[len("contains "):-1].split(", ")
        labels.append({
            "ingredients": ingredients,
            "allergens": allergens,
        })


possible_allergen_map = {}
for label in labels:
    for allergen in label["allergens"]:
        if allergen not in possible_allergen_map:
            possible_allergen_map[allergen] = set(label["ingredients"])
        else:
            possible_allergen_map[allergen] = (
                possible_allergen_map[allergen].intersection(label["ingredients"])
            )


def find_allergen_allocation(allergen_map, restricted_ingridients):
    if len(allergen_map) == 0:
        return {}

    next_allergen = next(iter(allergen_map.keys()))
    for ingredient in allergen_map[next_allergen]:
        if ingredient in restricted_ingridients:
            continue
        try:
            allocations = find_allergen_allocation({
                k: v
                for k, v in allergen_map.items()
                if k != next_allergen
            }, {ingredient} | restricted_ingridients)
            allocations[next_allergen] = ingredient
            return allocations
        except NoMatch:
            continue
    raise NoMatch


unique_allergen = find_allergen_allocation(possible_allergen_map, set())
allergenic_ingredients = set(unique_allergen.values())
print("Part 1:", sum(
    1
    for label in labels
    for ingredient in label["ingredients"]
    if ingredient not in allergenic_ingredients
))


sorted_ingridients = sorted(unique_allergen.items(), key=lambda x: x[0])
print("Part 2:", ",".join(i for _, i in sorted_ingridients))
