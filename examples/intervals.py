from visdata.mathtools import Interval


if __name__ == "__main__":
    boundaries = (1, 2)
    for kind in ("both", "left", "right", "neither"):
        interval = Interval(*boundaries, kind)
        print(
            f"{interval}\t{type(interval)}\n\t{interval.midpoint=}\n"
            f"\t{boundaries[0] in interval=}\n\t{boundaries[1] in interval=}\n"
            f"\t{max(interval)=}\t{min(interval)=}\n"
            f"\t{interval.closed=}\n\t{interval.opened=}\n"
            f"\t{interval.half_open=}\n"
            f"\t{interval.closed_left=}\n\t{interval.closed_right=}\n"
            f"\t{interval.open_left=}\n\t{interval.open_right=}\n"
        )
