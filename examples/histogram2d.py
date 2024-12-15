import numpy as np
from matplotlib import pyplot as plt
from visdata import Profile2d
from visdata.binned_data import bin_centers
from profile2d import create_hist2d_data, create_fixed_hist2d_data
from visdata.binned_data.histogram2d import Histogram2d


def test(x_data, y_data, bins=10):

    fig, axs = plt.subplots(nrows=3)
    ax, ax_x, ax_y = axs
    hist, bin_x_edges, bin_y_edges, image = ax.hist2d(x_data, y_data, bins=bins)

    bin_x_data = [
        y_data[(bin_x_edges[idx] <= x_data) & (x_data < bin_x_edges[idx + 1])]
        for idx in range(bin_x_edges.size - 1)
    ]
    # Righthand-most bin is closed and not half-open!
    bin_x_data[-1] = np.append(bin_x_data[-1], y_data[x_data == bin_x_edges[-1]])

    print(bin_x_data)
    ax_x.step(bin_x_edges[:-1], bin_x_data)
    ax_x.sharex(ax)
    # ax_x.set_ylim(0, 10)
    ax_y.step(bin_x_edges[:-1], hist[0])
    ax_y.sharex(ax)

    # print(hist)

    # hist_2, xedges_2, yedges_2 = np.histogram2d(x, y, bins=bins)
    # print(xedges, bin_centers(xedges), sep="\n")
    # print(xedges_2, bin_centers(xedges_2), sep="\n")

    return fig, axs


def test2(x, y, bins=20, marginal=False, profile=False):
    hist = Histogram2d(x, y, bins=bins)
    hist.configure_marginal(color="C1")
    fig, axs = hist.plot(marginal=marginal, profile=profile, cmap="cividis_r", cmin=1)

    return fig, axs


if __name__ == "__main__":
    x, y = create_hist2d_data(500)
    # x, y = create_fixed_hist2d_data()
    # x = np.linspace(0, 10, 1000) ** 3
    # y = np.linspace(0, 1, 1000) ** 2

    test2(x, y, marginal=True, profile=True)
    plt.show()
