import math

input_file = "input.txt"
with open(input_file) as f:
    station_arrival_timestamp, bus_schedule = f.read().strip().split("\n")
    station_arrival_timestamp = int(station_arrival_timestamp)
    bus_ids = [int(t) for t in bus_schedule.split(",") if t != "x"]
    all_ordered_ids = [int(t) if t != "x" else "x" for t in bus_schedule.split(",")]


earliest_departure = float("inf")
earliest_bus_id = None
for bus_id in bus_ids:
    bus_earlist_departure = math.ceil(station_arrival_timestamp / bus_id) * bus_id
    if bus_earlist_departure < earliest_departure:
        earliest_departure = bus_earlist_departure
        earliest_bus_id = bus_id

print("Part 1:", earliest_bus_id * (earliest_departure - station_arrival_timestamp))


def find_solution(ai, ni, const, prog):
    k = 1
    while True:
        if (const + prog * k + ai) % ni == 0:
            return const + prog * k
        k += 1


const = 0
prog = 1
for offset, bus_id in enumerate(all_ordered_ids):
    if bus_id == "x":
        continue
    const = find_solution(offset, bus_id, const, prog)
    prog *= bus_id

print("Part 2:", const)
