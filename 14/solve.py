import re

input_file = "input.txt"
with open(input_file) as f:

    def parse_cmd(raw_cmd):
        set_mask_match = re.match(r"mask = (.{36})", raw_cmd)
        if set_mask_match:
            return {"op": "set_mask", "value": list(set_mask_match.group(1))}
        set_memory_match = re.match(r"mem\[(\d+)\] = (\d+)", raw_cmd)
        return {
            "op": "set_memory",
            "address": int(set_memory_match.group(1)),
            "value": int(set_memory_match.group(2)),
        }

    cmds = list(map(parse_cmd, f.read().strip().split("\n")))


def convert_to_bit(value):
    result = ["0"] * 36
    for index in range(1, 37):
        result[-index] = "1" if value % 2 == 1 else "0"
        value = value // 2
    return result


def apply_mask(bit_value, mask):
    copied_value = bit_value[:]
    for index, value in enumerate(mask):
        if value != "X":
            copied_value[index] = value
    return copied_value


def convert_to_value(bit_value):
    result = 0
    for value in bit_value:
        result = 2 * result + int(value)
    return result


memory = {}
current_mask = None
for cmd in cmds:
    if cmd["op"] == "set_mask":
        current_mask = cmd["value"]
    elif cmd["op"] == "set_memory":
        bit_value = convert_to_bit(cmd["value"])
        mod_bit_value = apply_mask(bit_value, current_mask)
        mod_value = convert_to_value(mod_bit_value)
        memory[cmd["address"]] = mod_value
    else:
        raise Exception("Bad operation")


print("Part 1:", sum(memory.values()))


def apply_address_floating_mask(bit_address, mask):
    addresses = [[]]
    for addr_value, mask_value in zip(bit_address, mask):
        if mask_value == "0":
            for addr in addresses:
                addr.append(addr_value)
        elif mask_value == "1":
            for addr in addresses:
                addr.append("1")
        elif mask_value == "X":
            addresses = [
                addr[:] + [bit]
                for addr in addresses
                for bit in ["0", "1"]
            ]
    return addresses

memory = {}
current_mask = None
for cmd in cmds:
    if cmd["op"] == "set_mask":
        current_mask = cmd["value"]
    elif cmd["op"] == "set_memory":
        bit_address = convert_to_bit(cmd["address"])
        mod_addresses = apply_address_floating_mask(bit_address, current_mask)
        for bit_address in mod_addresses:
            address = convert_to_value(bit_address)
            memory[address] = cmd["value"]
    else:
        raise Exception("Bad operation")

print("Part 2:", sum(memory.values()))
