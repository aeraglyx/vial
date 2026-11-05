import argparse
import list
import plot


parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", type=str, required=True)
parser.add_argument("-d", "--defs", type=str, required=True)

sub = parser.add_subparsers(dest="cmd")

parser_list = sub.add_parser("list")
parser_list.add_argument("n", type=int, default=1, nargs="?")

parser_plot = sub.add_parser("plot")
parser_plot.add_argument("names", nargs="+", default=[])

args = parser.parse_args()


match args.cmd:
    case "list":
        list.main(args)
    case "plot":
        plot.main(args)
