import numpy as np
from matplotlib import pyplot as plt
from profile2d import create_hist2d_data, create_fixed_hist2d_data
from visdata import Histogram2d, Profile2dPlotConfigMean


def test(x, y, bins=20, marginal=False, profile=False):
    hist = Histogram2d(x, y, bins=bins)
    # Configure the marginal histograms if wanted, e.g. the color
    hist.configure_marginal(color="C2")
    # Configure the profile with a set of configs, e.g. only plot the mean but change the marker
    hist.configure_profile(Profile2dPlotConfigMean(marker="v"))
    fig, axs = hist.plot(marginal=marginal, profile=profile, cmap="cividis_r", cmin=1)

    # Change lables etc.
    try:
        ax = axs[0]
    except TypeError:
        ax = axs
    ax.set_xlabel(r"$\phi/\text{rad}$")
    ax.set_ylabel(r"$(h - h_0)/\text{m}$")
    ax.axhline(0, color="black", linestyle="--", linewidth=1)
    ax.set_ylim(-0.3, 0.3)

    return fig, axs


if __name__ == "__main__":
    x, y = create_hist2d_data(1000)

    # from visdata.plotting.matplotlib_util import latex_output, save_plot
    # with latex_output():
    with plt.rc_context(rc={"figure.figsize": (5, 3)}):
        fig, axs = test(x, y, marginal=True, profile=True)
        # save_plot(fig, "./doc/figs/histogram2d_example.pdf", transparent=False)
        # save_plot(fig, "./doc/figs/histogram2d_example.png", transparent=False, dpi=200)

    plt.show()
