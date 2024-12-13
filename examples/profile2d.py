import numpy as np
from matplotlib import pyplot as plt

from visdata.decorators import timer
from visdata import Profile2d, Profile2dPlotConfigMean, Profile2dPlotConfigMedian


def create_hist2d_data(n=1000):
    """Create a random test data set."""
    x = 2 * np.pi *np.random.rand(n)
    y = 0.05 * np.cos(x)
    y += np.random.normal(0, 0.1, n) + np.random.normal(0, 0.2, n) * y

    return x, y


def create_fixed_hist2d_data(range_pos=None):
    """Create some test data x, y for a 2d histogram."""
    if range_pos is True:
        x = np.linspace(1, 100, 200)
    else:
        x = np.linspace(-100, 100, 200)
    y = x**2
    displace = (5, 55, 75)
    for i in displace:
        y[i] += i * 500
    for i in range (140, 180):
        x = np.append(x, [i])
        y = np.append(y, [i**2])
    # x = np.append(x, [0] * 40)
    # y = np.append(y, [0] * 40)
    x = np.append(x, [220] * 2)
    y = np.append(y, [500, 10000])

    return x, y


@timer
def make_and_add_profile(*args, **kwargs):
    profile = Profile2d(*args, **kwargs)

    return profile


def test_profile_plot(x, y, bins_hist=20, bins_profile=20, compare_to_old_filter=False):
    fig, ax = plt.subplots()
    hist, xedges, yedges, image = ax.hist2d(x, y, bins=bins_hist, cmap="cividis_r", cmin=1)
    fig.colorbar(image, ax=ax, label=r"$n_\text{events}$")

    profile = make_and_add_profile(x, y, bins=bins_profile)
    # Default plot configs
    profile.add_to_axis(ax)
    # Custom plot configs
    # profile.add_to_axis(ax, Profile2dPlotConfigMedian(yerr="std"), Profile2dPlotConfigMean())

    # The old filter is horribly slow and will be removed in the future
    if compare_to_old_filter:
        profile_old_filter = make_and_add_profile(x, y, bins=bins_profile, numpy_bin_filter=False)
        profile_old_filter.add_to_axis(ax)

        properties = ("bin_means", "bin_sems", "bin_stds", "bin_medians")
        for property in properties:
            print(property)
            a_vals = getattr(profile, property)
            b_vals = getattr(profile_old_filter, property)
            for a, b in zip(a_vals, b_vals, strict=True):
                if a != b and not (np.isnan(a) and np.isnan(b)):
                    print(f"\tFALSE\t{a}\t{b}")

    return fig, ax


if __name__ == "__main__":

    bins_hist = 20
    bins_profile = 20
    compare_to_old_filter = False

    # from visdata.plotting.matplotlib_util import latex_output, save_plot
    # with latex_output(style="tableau-colorblind10"):

    # Example with random data
    n_events = 500
    x, y = create_hist2d_data(n_events)
    fig, ax = test_profile_plot(x, y, bins_hist=bins_hist, bins_profile=bins_profile, compare_to_old_filter=compare_to_old_filter)
    ax.set_xlabel(r"$\phi/\text{rad}$")
    ax.set_ylabel(r"$(h - h_0)/\text{m}$")
    ax.axhline(0, color="black", linestyle="--", linewidth=1)
    ax.set_ylim(-0.3, 0.3)

    plt.show()
    # save_plot(fig, "./doc/figs/profile2d_example_1.pdf", transparent=False)
    # save_plot(fig, "./doc/figs/profile2d_example_1.png", transparent=False)

    # Example with predefined data
    x, y = create_fixed_hist2d_data()
    fig, ax = test_profile_plot(x, y, bins_hist=bins_hist, bins_profile=bins_profile, compare_to_old_filter=compare_to_old_filter)
    ax.set_xlabel(r"$(x - x_0)/\text{m}$")
    ax.set_ylabel(r"$(S_\text{meas} - S_\text{mod})/\text{mV}$")

    plt.show()
    # save_plot(fig, "./doc/figs/profile2d_example_2.pdf", transparent=False)
    # save_plot(fig, "./doc/figs/profile2d_example_2.png", transparent=False)
