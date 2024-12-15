import warnings

import numpy as np

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
