import os
import json
import numpy as np
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, required=True)
parser.add_argument("-d", "--defs", type=str, required=True)
parser.add_argument("names", nargs="+", default=[])
args = parser.parse_args()


file_data = os.path.abspath(os.path.expanduser(args.file))
file_defs = os.path.abspath(os.path.expanduser(args.defs))


with open(file_data) as f:
    data = json.load(f)

with open(file_defs) as f:
    defs = json.load(f)


def plot_field(ax, name, field_def):
    data_filtered = [entry for entry in data if name in entry["data"]]

    dates = [entry["date"] for entry in data_filtered]
    values = [entry["data"][name] for entry in data_filtered]
    weights = [entry["quality"] for entry in data_filtered]

    x = np.array(dates, dtype="datetime64[D]")
    y = np.array(values, dtype=float)
    w = np.array(weights, dtype=float)

    desc = name

    if field_def:
        y_min = field_def["min"]
        y_max = field_def["max"]
        unit = field_def["unit"]
        desc = field_def["desc"]

        if y_min is not None and y_max is not None:
            ax.axhspan(y_min, y_max, color="green", alpha=0.125)

        ax.set_ylabel(unit)

    ax.plot(x, y, c="black", label=desc)
    ax.scatter(x, y, c="black")

    ax.legend()


fig = plt.figure(figsize=(10, 2.5 * len(args.names)))

for i, name in enumerate(args.names):
    ax = plt.subplot(len(args.names), 1, i + 1)
    if i > 0: ax.sharex(ax_prev)
    plot_field(ax, name, defs.get(name))
    ax_prev = ax

plt.tight_layout()
plt.show()
