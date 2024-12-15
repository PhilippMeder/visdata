import warnings

import numpy as np
from matplotlib import pyplot as plt

from .binning import bin_centers, which_bin


class Profile2dPlotConfig:

    def __init__(self, quantity, err=None, **kwargs):
        self._quantity = quantity
        self._err = err
        self._options = {"linestyle": "", "barsabove": True, "label": f"{quantity} with {err}"}
        self._options.update(kwargs)

    @property
    def quantity(self):
        return self._quantity

    @property
    def err(self):
        return self._err

    @property
    def options(self):
        return self._options


class Profile2dPlotConfigMean(Profile2dPlotConfig):

    def __init__(self, **kwargs):
        # Set and patch default options
        err = kwargs.pop("err", "sem")
        options = {
            "color": "r",
            "marker": ".",
            "markersize": 5,
            "elinewidth": 1,
            "capsize": 2
        }
        options.update(kwargs)
        super().__init__("mean", err=err, **options)


class Profile2dPlotConfigMedian(Profile2dPlotConfig):

    def __init__(self, **kwargs):
        # Set and patch default options
        err = kwargs.pop("err", None)
        options = {
            "color": "deeppink",
            "marker": "s",
            "markersize": 6
        }
        options.update(kwargs)
        super().__init__("median", err=err, **options)


class Profile2d:

    def __init__(self, x, y, bins=10, **kwargs):
        """Calculate the profile for a 2d data problem."""
        self.__data_x = x
        self.__data_y = y
        self.__bins = bins

        # This will be deleted in the future
        if "numpy_bin_filter" in kwargs.keys():
            warnings.warn(
                f"{self.__class__.__name__}.__init__ keyword 'numpy_bin_filter' is deprecated and will be removed in the future!",
                DeprecationWarning,
            )
        self.__numpy_bin_filter = kwargs.pop("numpy_bin_filter", True)
        if kwargs:
            raise TypeError(
                f"{self.__class__.__name__}.__init__ got unexpected keyword arguments '{list(kwargs.keys())}'"
            )

        self.__bin_data()
        self.__calculate_statistics()

    def __bin_data(self):
        """Sort the data into the right bins."""
        x_data = self.__data_x
        y_data = self.__data_y

        if self.__numpy_bin_filter:
            # Filter using numpy, much faster
            _hist, bin_x_edges, _bin_y_edges = np.histogram2d(
                x_data, y_data, self.__bins
            )

            bin_data = [
                y_data[(bin_x_edges[idx] <= x_data) & (x_data < bin_x_edges[idx + 1])]
                for idx in range(bin_x_edges.size - 1)
            ]
            # Righthand-most bin is closed and not half-open!
            bin_data[-1] = np.append(bin_data[-1], y_data[x_data == bin_x_edges[-1]])
        else:
            # Custom filter, much slower, here for historical reasons
            _hist, bin_x_edges = np.histogram(x_data, self.__bins)

            bin_data = [[] for idx in range(len(bin_x_edges) - 1)]

            for x, y in zip(x_data, y_data):
                bin_id = which_bin(x, bin_x_edges)
                bin_data[bin_id].append(y)

        self.__binned_data = bin_data
        self.__bin_edges = bin_x_edges

    def __calculate_statistics(self):
        """Calculate the statistics for each x bin."""
        self.__means, self.__stds, self.__sems, self.__medians = [], [], [], []
        for data in self.__binned_data:
            if (self.__numpy_bin_filter and data.size > 0) or (
                not self.__numpy_bin_filter and data
            ):
                mean = np.mean(data)
                std = np.std(data, ddof=1)
                sem = std / np.sqrt(np.size(data))
                median = np.median(data)
            else:
                mean, std, sem, median = np.nan, np.nan, np.nan, np.nan
            self.__means.append(mean)
            self.__stds.append(std)
            self.__sems.append(sem)
            self.__medians.append(median)

    @property
    def bin_centers(self):
        """Return the edges for the x bins."""
        return bin_centers(self.__bin_edges)

    @property
    def bin_data(self):
        """Return the data for the x bins."""
        return self.__binned_data

    @property
    def bin_edges(self):
        """Return the edges for the x bins."""
        return self.__bin_edges

    @property
    def bin_means(self):
        """Return the means for each x bin."""
        return self.__means

    @property
    def bin_medians(self):
        """Return the medians for each x bin."""
        return self.__medians

    @property
    def bin_stds(self):
        """Return the standard deviations for each x bin."""
        return self.__stds

    @property
    def bin_sems(self):
        """Return the standard error of the mean for each x bin."""
        return self.__sems

    def add_to_axis(self, ax, *configs: Profile2dPlotConfig):
        """Add the profile to the given axis."""
        add_profile2d_to_axis(
            ax,
            self.bin_centers,
            self.bin_means,
            self.bin_sems,
            self.bin_stds,
            self.bin_medians,
            *configs,
        )


def add_profile2d_to_axis(
    ax, xcenter, mean, sem, std, median, *configs: Profile2dPlotConfig
):
    """Add profile2d plot to given axis."""
    if not len(configs):
        configs = (Profile2dPlotConfigMedian(), Profile2dPlotConfigMean())

    for config in configs:
        match config.quantity:
            case "mean":
                data = mean
            case "median":
                data = median
            case _:
                raise ValueError(f"Unknown quantity '{config.quantity}'!")

        match config.err:
            case "sem" | "standard error on the mean":
                yerr = sem
            case "std" | "standard deviation":
                yerr = std
            case 0 | None | False:
                yerr = None
            case _:
                raise ValueError(f"Unknown error quantity '{config.err}'!")

        ax.errorbar(xcenter, data, yerr=yerr, **config.options)


class Histogram2d:

    def __init__(self, x, y, bins=10, xlabel=None, ylabel=None, clabel=None):
        self._x = x
        self._y = y
        self._bins = bins

        self.xlabel = xlabel if xlabel is not None else "$x$-data"
        self.ylabel = ylabel if ylabel is not None else "$y$-data"
        self.clabel = clabel if clabel is not None else "$n$"

        self.configure_marginal()
        self.configure_marginal_grid()
        self.configure_profile()

    def configure_marginal(self, **kwargs):
        self._marginal_kwargs = kwargs

    def configure_marginal_grid(self, **kwargs):
        self._marginal_grid = {
            "main_width_ratio": 5,
            "main_height_ratio": 5,
            "cbar_width_ratio": 0.5,
            "cbar_spacing": 1
        }
        self._marginal_grid.update(kwargs)

    def configure_profile(self, *args, **kwargs):
        self._profile_args = args
        self._profile_kwargs = kwargs

    @staticmethod
    def get_subplot(subplot):
        if subplot is None:
            fig, ax = plt.subplots()
        else:
            fig, ax = subplot

        return fig, ax

    def hist2d(self, subplot=None, colorbar_ax=None, colorbar_ratio=None,**kwargs):
        fig, ax = self.get_subplot(subplot)
        hist, xedges, yedges, image = ax.hist2d(self._x, self._y, bins=self._bins, **kwargs)
        # print(colorbar_ratio)
        # for name, spine in colorbar_ax.spines.items():
        #     spine.set_visible(False)
        # colorbar_ax.xaxis.set_visible(False)
        # colorbar_ax.yaxis.set_visible(False)
        # for name, val in vars(colorbar_ax).items():
        #     print(name, val, sep="\t")
        fig.colorbar(image, cax=colorbar_ax)#, fraction=1, shrink=colorbar_ratio, label=self.clabel)

        return fig, ax, image

    def hist(self, dimension: str, subplot=None, **kwargs):
        fig, ax = self.get_subplot(subplot)
        # Get correct data
        match dimension:
            case "x" | "X" | 0:
                data = self._x
                bin_dim = 0
            case "y" | "Y" | 1:
                data = self._y
                bin_dim = 1
            case _:
                raise ValueError(f"Dimension '{dimension}' unkown, should be 'x' or 'y'!")

        # Get correct bins
        try:
            bins = self._bins[bin_dim]
        except TypeError:
            bins = self._bins

        # Draw histogram
        ax.hist(data, bins=bins, **kwargs)

        return fig, ax

    def _setup_marginal_subplots(self):
        """Create subplots so that width(marginal(y))=height(marginal(x))."""
        fig = plt.figure()

        ratio_par_cbar = 30
        ratio_par_main = 5

        outer_a, outer_b = ratio_par_cbar, 1
        a, b, d = ratio_par_main, 1 , ratio_par_main
        c = 0.5

        figsize = fig.get_size_inches()
        fig_ratio = figsize[0] / figsize[1]
        subgrid_ratio = 1 # outer_a / (outer_a + outer_b)
        main_ratio = b / (a + b + c)

        factor = main_ratio * subgrid_ratio * fig_ratio
        fix_ratio = d * factor / (1 - factor)

        # outer_grid = fig.add_gridspec(1, 2, wspace=0.05, hspace=0, width_ratios=(outer_a, outer_b))
        # grid_spec = outer_grid[0].subgridspec(2, 2, wspace=0, hspace=0, width_ratios=(a, b), height_ratios=(fix_ratio, d))
        grid_spec = fig.add_gridspec(2, 3, wspace=0, hspace=0, width_ratios=(a, b, c), height_ratios=(fix_ratio, d))
        ax_hist2d = fig.add_subplot(grid_spec[1, 0])
        ax_hist_x = fig.add_subplot(grid_spec[0, 0], sharex=ax_hist2d)
        ax_hist_y = fig.add_subplot(grid_spec[1, 1], sharey=ax_hist2d)
        # colorbar_ax = fig.add_subplot(outer_grid[1])
        # colorbar_ax = fig.add_subplot(grid_spec[1, 2])
        colorbar_ax = ax_hist_y.inset_axes([1.05, 0, c / (a + b + c) * figsize[0] - 0.05, 1])

        # ax_hist2d = fig.add_gridspec(top=0.75, right=0.75).subplots()
        # ax_hist_x = ax_hist2d.inset_axes([0, 1, 1, 0.25], sharex=ax_hist2d)
        # ax_hist_y = ax_hist2d.inset_axes([1, 0, 0.25, 1], sharey=ax_hist2d)
        # colorbar_ax = ax_hist2d.inset_axes([1.3, 0, 0.2, 1])

        return fig, ax_hist2d, ax_hist_x, ax_hist_y, colorbar_ax, 1#d / (fix_ratio + d)

    def plot(self, marginal=False, profile=False, **kwargs):
        if marginal:
            fig, ax_hist2d, ax_hist_x, ax_hist_y, colorbar_ax, colorbar_ratio = self._setup_marginal_subplots()
            axs = (ax_hist2d, ax_hist_x, ax_hist_y)
        else:
            fig, ax_hist2d = plt.subplots()
            colorbar_ax = None
            axs = ax_hist2d

        # Create plots
        self.hist2d(subplot=(fig, ax_hist2d), colorbar_ax=colorbar_ax, colorbar_ratio=colorbar_ratio, **kwargs)
        ax_hist2d.set_xlabel(self.xlabel)
        ax_hist2d.set_ylabel(self.ylabel)

        # Add marginal histograms
        if marginal:
            self.hist("x", subplot=(fig, ax_hist_x), **self._marginal_kwargs)
            self.hist("y", subplot=(fig, ax_hist_y), orientation="horizontal", **self._marginal_kwargs)
            # Set marginal axis properties
            ax_hist_x.set_yticks(ax_hist_x.get_yticks()[1:])
            ax_hist_y.set_xticks(ax_hist_y.get_xticks()[1:])
            ax_hist_x.xaxis.set_visible(False)
            ax_hist_y.yaxis.set_visible(False)
            ax_hist_x.set_ylabel(self.clabel)
            ax_hist_y.set_xlabel(self.clabel)

        # Add profile
        if profile:
            profile = Profile2d(self._x, self._y, self._bins)
            profile.add_to_axis(ax_hist2d, *self._profile_args, **self._profile_kwargs)

        # axs = fig.get_axes()
        for ax in fig.get_axes():
            bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            print(f"{bbox.width:5.2f}\t{bbox.height:5.2f}")

        return fig, axs
