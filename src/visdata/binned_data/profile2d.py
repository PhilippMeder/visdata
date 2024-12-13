from dataclasses import dataclass
import warnings

import numpy as np

from .binning import bin_centers, which_bin


@dataclass(kw_only=True)
class Profile2dPlotConfigBase:

    quantity: str | None = None
    label: str | None = None
    xerr: str | int | float | None = None
    yerr: str | int | float | None = None
    color: str | None = None
    marker: str | None = None
    markersize: int | None = None
    linewidth: int | None = None
    capsize: int | None = None

    def __post_init__(self):
        if self.label is None:
            self.label = f"{self.quantity} ({self.xerr}, {self.yerr})"


@dataclass(kw_only=True)
class Profile2dPlotConfigMean(Profile2dPlotConfigBase):

    quantity: str | None = "mean"
    yerr: str | int | None = "sem"
    color: str | None = "r"
    marker: str | None = "."
    markersize: int | None = 5
    linewidth: int | None = 1
    capsize: int | None = 2


@dataclass(kw_only=True)
class Profile2dPlotConfigMedian(Profile2dPlotConfigBase):
    quantity: str | None = "median"
    color: str | None = "deeppink"
    marker: str | None = "s"
    markersize: int | None = 6


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

    def add_to_axis(self, ax, *configs: Profile2dPlotConfigBase):
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
    ax, xcenter, mean, sem, std, median, *configs: Profile2dPlotConfigBase
):
    """Add profile2d plot to given axis."""
    if not len(configs):
        configs = (Profile2dPlotConfigMean(), Profile2dPlotConfigMedian())

    for config in configs:
        match config.quantity:
            case "mean":
                data = mean
            case "median":
                data = median
            case _:
                raise ValueError(f"Unknown quantity '{config.quantity}'!")

        match config.yerr:
            case "sem" | "standard error on the mean":
                yerr = sem
            case "std" | "standard deviation":
                yerr = std
            case 0 | None | False:
                yerr = None
            case _:
                raise ValueError(f"Unknown error quantity '{config.yerr}'!")

        if yerr is not None or config.xerr is not None:
            ax.errorbar(
                xcenter,
                data,
                xerr=config.xerr,
                yerr=yerr,
                color=config.color,
                linestyle="",
                marker=config.marker,
                markersize=config.markersize,
                elinewidth=config.linewidth,
                capsize=config.capsize,
                label=config.label,
            )
        else:
            ax.scatter(
                xcenter,
                data,
                c=config.color,
                marker=config.marker,
                s=config.markersize**2,  # markersize definition differs from errorbar
                label=config.label,
            )
