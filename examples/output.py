import argparse

import numpy as np

from visdata import Table, object_vars_str


def get_example_table(n_rows=5, n_cols=5, headings=True, named_rows=False, caption=False, numpy=False):
    data = [
        [i + j * n_cols for i in range(n_cols)] for j in range(n_rows)
    ]
    if numpy:
        data = np.array(data)

    column_labels = [f"a{i}" for i in range(n_cols)] if headings else None
    row_labels = [f"A{i}" for i in range(n_rows)] if named_rows else None
    description = "Some important values" if caption else None

    return Table(data, description=description, column_labels=column_labels, row_labels=row_labels)


def get_sys_args():
    parser = argparse.ArgumentParser(description="Arguments for example table and according output.")

    parser.add_argument(
        "-d",
        "--dimensions",
        dest="dimensions",
        nargs=2,
        default=(5, 3),
        type=int,
        help="Dimensions of the example table, i.e. 'columns rows'."
    )
    parser.add_argument(
        "-f",
        "--formatter",
        dest="formatter",
        type=str,
        default="5.2f",
        help="Formatter for table values."
    )
    parser.add_argument(
        "-c",
        "--caption",
        dest="caption",
        action="store_true",
        help="Show table caption."
    )
    parser.add_argument(
        "-b",
        "--bare",
        "--no-headings",
        dest="headings",
        action="store_false",
        help="Hide column headings."
    )
    parser.add_argument(
        "-n",
        "--names",
        dest="named_rows",
        action="store_true",
        help="Show row names."
    )

    return parser.parse_args()


if __name__ == "__main__":
    # Parse and pretty print the arguments
    sys_args = get_sys_args()
    print(object_vars_str(sys_args, title="Given parameters for creation of an example table."))

    # Play a little with the example table options
    table = get_example_table(
        n_rows=sys_args.dimensions[1],
        n_cols=sys_args.dimensions[0],
        headings=sys_args.headings,
        named_rows=sys_args.named_rows,
        caption=sys_args.caption
    )

    # Before printing the table itself, we print the arguments of the object
    print(object_vars_str(table, title="Attributes of the created example table."))

    # Standard printing of the table in the terminal
    sep = f"\n{'\u2193':^64}\n"
    print(f"{'Standard output when printing':^64}", table, sep=sep)

    # Try different value formatters
    formatter = sys_args.formatter
    if formatter in ("none", "None"):
        formatter = None
    # formatter = "5.2f"
    # formatter = ".2f"
    # formatter = None

    # Standard csv uses "," as separator, no lines, and ignores the total length
    csv = table.csv(formatter=formatter)
    print(f"{'Standard CSV output':^64}", csv, sep=sep)
    # with open("test_csv.txt", "w") as file:
    #     file.write(csv)

    # Standard latex uses the scientific table format and booktabs
    latex = table.latex(formatter=formatter)
    print(f"{'Standard LaTeX output':^64}", latex, sep=sep)
    # with open("test_latex.tex", "w") as file:
    #     file.write(latex)

    # For more control of the outputformat, use 'output()' with its options
    # output_format = "base"
    # # output_format = "csv"
    # # output_format = "latex"

    # linestyle = None
    # # linestyle = "scientific"

    # print(table.output(output_format, formatter, linestyle=linestyle))
