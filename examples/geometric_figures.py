from matplotlib import pyplot as plt

from visdata.plotting.geometric_figures import RegularHexagon, RegularSquare, RegularTriangle


if __name__ == "__main__":
    fig, ax = plt.subplots()
    ax.set_aspect("equal")

    for polygon_class in (RegularTriangle, RegularSquare, RegularHexagon):
        polygon = polygon_class((0.5, 0.5), 0.2, fill=False)
        ax.add_patch(polygon)
        print(polygon)
        print(polygon.xy)
    plt.show()

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    polygon = RegularHexagon((0.5, 0.5), 0.2, fill=True, color="cornflowerblue")
    ax.add_patch(polygon)
    polygon_inner = RegularHexagon((0.5, 0.5), 0.15, fill=True, color="white")
    ax.add_patch(polygon_inner)

    plt.show()
