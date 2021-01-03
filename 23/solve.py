test_input = "389125467"
actual_input = "198753462"
run_input = actual_input


def make_linked_list(l):
    v0 = l[0]
    node_by_value = {}
    last = None
    for v in l:
        next_ = {
            "value": v,
            "next": None,
        }
        node_by_value[v] = next_
        if last is not None:
            last["next"] = next_
        last = next_
    last["next"] = node_by_value[v0]
    return node_by_value[v0], node_by_value


def find_value(linked_list, f):
    start = linked_list
    value = linked_list["value"]
    while linked_list["next"] is not start:
        linked_list = linked_list["next"]
        value = f(value, linked_list["value"])

    return value


def pick_range(linked_list, start_index, end_index):
    index = 0
    range_ = []
    while index < end_index:
        if index >= start_index:
            range_.append(linked_list["value"])
        linked_list = linked_list["next"]
        index += 1
    return range_


def delete_range(linked_list, start_index, end_index):
    if start_index >= end_index:
        return

    index = 0
    last = None
    while index < end_index:
        if index < start_index:
            last = linked_list
        else:
            del node_by_value[linked_list["value"]]
        index += 1
        linked_list = linked_list["next"]

    last["next"] = linked_list


def insert_values(root, node_by_value, values):
    next_ = root["next"]
    last = root
    for v in values:
        node = {
            "value": v,
            "next": next_
        }
        node_by_value[v] = node
        last["next"] = node
        last = node


def get_value(linked_list, pick_index):
    index = 0
    while index < pick_index:
        index += 1
        linked_list = linked_list["next"]

    return linked_list["value"]


def to_array(linked_list):
    start = linked_list
    array = [linked_list["value"]]
    linked_list = linked_list["next"]
    while linked_list is not start:
        array.append(linked_list["value"])
        linked_list = linked_list["next"]
    return array


def mix_the_cups(current_state, node_by_value, number_of_moves):
    MIN_CUP = find_value(current_state, min)
    MAX_CUP = find_value(current_state, max)
    current_cup = get_value(current_state, 0)

    for step in range(number_of_moves):
        if step % 100000 == 0:
            print(step)

        picked = pick_range(current_state, 1, 4)
        delete_range(current_state, 1, 4)
        destination_cup = current_cup - 1
        while destination_cup in picked or destination_cup < MIN_CUP:
            destination_cup -= 1
            if destination_cup < MIN_CUP:
                destination_cup = MAX_CUP
        destination = node_by_value[destination_cup]
        insert_values(destination, node_by_value, picked)

        current_cup = get_value(current_state, 1)
        current_state = node_by_value[current_cup]

    return current_state


initial_state, node_by_value = make_linked_list(list(map(int, run_input)))
final_state = mix_the_cups(initial_state, node_by_value, 100)
print("aqui")
final_state = node_by_value[1]
print("ok")
print("Part 1:", "".join(map(str, to_array(final_state)[1:])))


one_million = 10 ** 6
initial_state, node_by_value = make_linked_list(
    list(map(int, run_input)) + list(range(10, one_million + 1))
)
final_state = mix_the_cups(initial_state, node_by_value, 10 * one_million)
final_state = node_by_value[1]
print("Part 2:", final_state["next"]["value"] * final_state["next"]["next"]["value"])
