import visdata
import visdata.mathtools


if __name__ == "__main__":

    # available = locals().copy()
    # for name, value in available.items():
    #     print(f"{name:32}\t{value}")

    line = f"{'':\u2500>16}"
    ignore_names = ("__builtins__", "__cached__", "__file__", "__path__", "__spec__", "__loader__", "__name__")

    tests = (visdata, visdata.mathtools)
    for test in tests:
        print(line, test.__name__, line, sep="\n")
        for name, value in vars(test).items():
            if name in ignore_names:
                continue
            print(f"{name:32}\t{value}")

    visdata.mathtools.sec(1)
