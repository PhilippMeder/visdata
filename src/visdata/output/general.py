def object_vars_str(
    obj: object,
    title: str = None,
    tab: str = None,
    line: str = None,
    newline: str = None,
):
    """Return formatted string of vars(object), e.g. argparse object."""
    if title is None:
        title = "Attributes"
    if tab is None:
        tab = f"{'':4}"
    if line is None:
        line = f"{'':\u2500<80}"
    if newline is None:
        newline = "\n"

    attributes_dict = vars(obj)
    name_column_width = max([len(name) for name in attributes_dict.keys()])

    heading = newline.join((line, title, line))
    attributes_str = [
        f"{tab}{name:<{name_column_width}}:{tab}{value}"
        for name, value in attributes_dict.items()
    ]

    return heading + newline + newline.join(attributes_str) + newline + line

    args_dict = vars(args)
    n = max([len(arg_name) for arg_name in args_dict.keys()])

    print(f"{line}\n{title}\n{line}")
    for arg_name, arg_value in args_dict.items():
        print(f"{tab}{arg_name:<{n}}:{tab}{arg_value}")
    print(line)
