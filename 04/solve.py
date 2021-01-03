import re

input_file = "input.txt"

def parse_passports():
    with open(input_file) as f:
        passport = ""
        for line in f.read().split("\n"):
            if line:
                passport += " " + line
            else:
                yield passport.strip()
                passport = ""


required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
valid = 0

# Part 1
for passport in parse_passports():
    passport_fields = {f.split(":")[0] for f in passport.split(" ")}
    passport_fields -= {"cid"}
    valid += int(passport_fields == required_fields)
print("Part 1:", valid)


# Part 2
def int_between(value, min_, max_):
    try:
        return min_ <= int(value) <= max_
    except (ValueError, TypeError):
        return False


valid = 0
for passport in parse_passports():
    passport_fields = {f.split(":")[0] for f in passport.split(" ")}
    passport_fields -= {"cid"}
    if (passport_fields != required_fields):
        continue

    all_fields_valid = True
    for field in passport.split(" "):
        field_name, field_value = field.split(":")
        if field_name == "byr":
            all_fields_valid = int_between(field_value, 1920, 2002)
        if field_name == "iyr":
            all_fields_valid = int_between(field_value, 2010, 2020)
        if field_name == "eyr":
            all_fields_valid = int_between(field_value, 2020, 2030)
        if field_name == "hgt":
            value, unit = field_value[:-2], field_value[-2:]
            if unit == "cm":
                all_fields_valid = int_between(value, 150, 193)
            elif unit == "in":
                all_fields_valid = int_between(value, 59, 76)
            else:
                all_fields_valid = False
        if field_name == "hcl":
            all_fields_valid = re.match("#[a-f0-9]{6}", field_value) is not None
        if field_name == "ecl":
            all_fields_valid = field_value in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
        if field_name == "pid":
            all_fields_valid = len(field_value) == 9 and int_between(field_value, 0, 10**11 - 1)

        if not all_fields_valid:
            break

    valid += int(all_fields_valid)

print("Part 2:", valid)
