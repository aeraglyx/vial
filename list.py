import os
import json
from math import floor, inf
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("n", type=int, default=1, nargs="?")
args = parser.parse_args()


# TODO: pass filepaths
data_path = os.path.expanduser("~")
file_data = os.path.join(data_path, "data.json")
file_defs = os.path.join(data_path, "defs.json")

class colors():
    BLACK = '\033[30m'
    WHITE = '\033[37m'

    RED = '\033[31m'
    YELLOW = '\033[33m'
    GREEN = '\033[32m'
    CYAN = '\033[36m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'

    BLACK_BRIGHT = '\033[90m'

    RESET = '\033[0m'

urgency_map = [colors.BLACK, colors.BLACK_BRIGHT, colors.RESET, colors.YELLOW, colors.RED]


def get_indicator_and_color(value, val_min, val_max):
    bound = colors.BLACK + "|" + colors.RESET
    indicator = [" ", bound, " ", " ", " ", bound, " "]
    value_color = colors.BLACK

    if val_min is not None and val_max is not None and isinstance(value, float):
        t = (value - val_min) / (val_max - val_min)

        id = round(4 * t) + 1
        id_center = min(abs(id - 3), 4)

        # min == 0 probably means "lower is better", so skip coloring
        if val_min != 0 or t > 0.5:
            value_color = urgency_map[id_center]

        id_clamped = min(max(id, 0), 6)
        indicator[id_clamped] = f"{value_color}*{colors.RESET}"

    indicator = "".join(indicator)
    return indicator, value_color


def shorten_string(string: str, length: int) -> str:
    if len(string) > length:
        ellipsis = "…"
        string = (string[:length-len(ellipsis)] + ellipsis)
    return string.ljust(length)


def get_field_line(field_key, value, value_last, field_def) -> str:
    unit = "--"
    desc = "--"
    val_min = None
    val_max = None
    change = None
    change_color = ""

    if field_def:
        unit = field_def["unit"]
        desc = field_def["desc"]
        val_min = field_def["min"]
        val_max = field_def["max"]

    if value_last is not None:
        if value_last == 0:
            change = 1 if value == 0 else inf
        else:
            change = value / value_last

        # TODO: change per time

        change_norm = change if change < 1.0 else 1.0 / change
        color_id = min(max(floor(5 * (1 - change_norm)), 0), len(urgency_map) - 1)

        change_color = urgency_map[color_id]

    indicator, value_color = get_indicator_and_color(value, val_min, val_max)

    field_line = "".join([
        value_color + shorten_string(field_key, 14),
        value_color + str(value).rjust(6) + " ",
        colors.BLACK + shorten_string(unit, 8) + colors.RESET + " ",
        indicator + "  ",
        value_color + str(val_min).rjust(6),
        colors.BLACK + " - " + colors.RESET,
        value_color + str(val_max).ljust(7),
        change_color + f"{change:.2f}".rjust(6) if change is not None else colors.BLACK + " -- ".rjust(6),
        "    ",
        value_color + desc + colors.RESET,
    ])

    return field_line


def get_header_line():
    header_line = "".join([
        "key".ljust(14),
        "value".rjust(6) + " "
        "unit".ljust(9),
        "indicator".ljust(15),
        "range".ljust(12),
        "change".ljust(9),
        "description",
    ])
    header_line = colors.BLACK_BRIGHT + header_line.upper() + colors.RESET
    return header_line


def get_last_value(data, key):
    for entry in data:
        if key in entry["data"]:
            return entry["data"][key]
    return None


with open(file_data) as f:
    data = json.load(f)

with open(file_defs) as f:
    defs = json.load(f)


entry_id = -args.n
entry = data[entry_id]
data_old = data[entry_id-1::-1]

date_str = "\n" + colors.BLACK_BRIGHT + entry["date"] + colors.RESET
first_line = f"{date_str} {entry["note"]}\n"
print(first_line)

header_line = get_header_line()
print(header_line)


for key, value in entry["data"].items():

    value_last = get_last_value(data_old, key)
    field_def = defs.get(key)

    field_line = get_field_line(key, value, value_last, field_def)
    print(field_line)
