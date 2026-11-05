import os
import json
import numpy as np
import matplotlib.pyplot as plt


def plot_field(ax, data, name, field_def):
    dates = [entry["date"] for entry in data]
    values = [entry["data"][name] for entry in data]
    weights = [entry["quality"] for entry in data]

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


def main(args):
    file_data = os.path.abspath(os.path.expanduser(args.file))
    file_defs = os.path.abspath(os.path.expanduser(args.defs))

    with open(file_data) as f:
        data = json.load(f)

    with open(file_defs) as f:
        defs = json.load(f)

    fig = plt.figure(figsize=(10, 2.5 * len(args.names)))

    for i, name in enumerate(args.names):
        ax = plt.subplot(len(args.names), 1, i + 1)
        if i > 0: ax.sharex(ax_prev)
        data_filtered = [entry for entry in data if name in entry["data"]]
        plot_field(ax, data_filtered, name, defs.get(name))
        ax_prev = ax

    plt.tight_layout()
    plt.show()
