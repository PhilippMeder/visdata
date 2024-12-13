import numpy as np
from matplotlib import pyplot as plt


class MeasurementResultPlotConfig:

    default_value = {"zorder": 4}
    default_statistical = {"elinewidth": 3, "zorder": 2}
    default_systematic = {"capsize": 6, "zorder": 3}
    default_total = {"elinewidth": 12, "alpha": 0.4, "zorder": 1}

    def __init__(
        self,
        value: dict = None,
        statistical: dict = None,
        systematic: dict = None,
        total: dict = None,
    ):
        self.value = self.patch_with_default(
            value, self.default_value, allow_turn_off=False
        )
        self.statistical = self.patch_with_default(
            statistical, self.default_statistical
        )
        self.systematic = self.patch_with_default(systematic, self.default_systematic)
        self.total = self.patch_with_default(total, self.default_total)

    @staticmethod
    def patch_with_default(settings, defaults, allow_turn_off=True):
        match settings:
            case None:
                new = defaults
            case False:
                if allow_turn_off:
                    new = None
                else:
                    new = defaults
            case _:
                new = defaults.copy()
                new.update(settings)

        return new


class MeasurementResult:

    def __init__(
        self,
        value,
        statistical: float | tuple[float] = np.nan,
        systematic: float | tuple[float] = np.nan,
    ):
        self._value = value
        self._statistical = statistical
        self._systematic = systematic

        try:
            self._stat_uncertainty = self.combine_uncertainties(statistical)
        except TypeError:
            self._stat_uncertainty = statistical

        try:
            self._sys_uncertainty = self.combine_uncertainties(systematic)
        except TypeError:
            self._sys_uncertainty = systematic

    @staticmethod
    def combine_uncertainties(uncertainties):
        """Combine uncertainties as ''sqrt(x1^2 + x2^2 + ...)."""
        return np.sqrt(np.sum([value**2 for value in uncertainties]))

    @property
    def value(self):
        return self._value

    @property
    def statistical_uncertainty(self):
        return self._stat_uncertainty

    @property
    def stat(self):
        return self.statistical_uncertainty

    @property
    def systematic_uncertainty(self):
        return self._sys_uncertainty

    @property
    def sys(self):
        return self.systematic_uncertainty

    @property
    def total_uncertainty(self):
        """Return quadratic combination of stat. and sys. uncertainties (Shady!)."""
        return self.combine_uncertainties((self.stat, self.sys))

    @property
    def tot(self):
        """Return quadratic combination of stat. and sys. uncertainties (Shady!)."""
        return self.total_uncertainty

    def add_to_axis(
        self, ax, position, label, color, marker, config: MeasurementResultPlotConfig
    ):
        scatter = ax.scatter(
            position,
            self.value,
            label=label,
            color=color,
            marker=marker,
            **config.value,
        )
        color = scatter.get_facecolors()[0]
        if self.stat and config.statistical:
            ax.errorbar(
                position,
                self.value,
                yerr=self.stat,
                label=label,
                color=color,
                marker="",
                **config.statistical,
            )
        if self.sys and config.systematic:
            ax.errorbar(
                position,
                self.value,
                yerr=self.sys,
                label=label,
                color=color,
                marker="",
                **config.systematic,
            )
        if self.tot and config.total:
            ax.errorbar(
                position,
                self.value,
                yerr=self.tot,
                label=label,
                color=color,
                marker="",
                **config.total,
            )


class Measurement:

    def __init__(
        self,
        name: str,
        results: dict[str, MeasurementResult],
        color: str = None,
        marker: str = None,
    ):
        self.name = name
        self.results = results
        self.color = color
        self.marker = marker


class CompareMeasurementsPlot:

    def __init__(
        self, *measurements: Measurement, config: MeasurementResultPlotConfig = None
    ):
        self.measurements = measurements
        if config is None:
            self.config = MeasurementResultPlotConfig()
        else:
            self.config = config

        self.n_measurements = len(self.measurements)
        self.get_all_parameters()

    def get_all_parameters(self):
        names = []
        taken_colors = []
        col_idx = 0
        for measurement in self.measurements:
            names += measurement.results.keys()
            if measurement.color is None:
                while (_color := f"C{col_idx}") in taken_colors:
                    col_idx += 1
                measurement.color = _color
            taken_colors.append(measurement.color)
        # Get rid of duplicates, can't use normal set conversion since it destroys the ordering
        _seen_names = set()
        self.parameter_names = [
            name for name in names if not (name in _seen_names or _seen_names.add(name))
        ]
        self.n_parameters = len(self.parameter_names)
        self._taken_colors = taken_colors

    def __get_subplots(self, ncols, subplots, kwargs):
        """Setup plot or use given subplots and make sure the amount fits."""
        if subplots is not None:
            fig, axs = subplots
        elif self.n_parameters <= ncols:
            fig, axs = plt.subplots(ncols=self.n_parameters, **kwargs)
        else:
            nrows = self.n_parameters // ncols
            if self.n_parameters % ncols:
                nrows += 1
            fig, axs = plt.subplots(nrows=nrows, ncols=ncols, **kwargs)

        # Check if there are enough subplots
        if (_n_axs := len(axs.flat)) < self.n_parameters:
            raise ValueError(
                f"Number of axes smaller than number of parameters: {_n_axs} < {self.n_parameters}"
            )

        return fig, axs

    def plot(
        self,
        subplots: tuple = None,
        spacing: float = 1,
        start_position: float = 1,
        ncols: int = 3,
        delete_unused_axes=True,
        **kwargs,
    ):
        # Create correct amount of subplots or use given ones
        fig, axs = self.__get_subplots(ncols, subplots, kwargs)

        # Plot all parameters
        for ax, name in zip(axs.flat, self.parameter_names):
            # Add measurements
            position = start_position
            for measurment in self.measurements:
                try:
                    measurment.results[name].add_to_axis(
                        ax,
                        position,
                        measurment.name,
                        measurment.color,
                        measurment.marker,
                        self.config,
                    )
                except KeyError:
                    pass
                position += spacing
            # Set axis properties
            ax.set_ylabel(name)
            ax.xaxis.set_visible(False)
            ax.set_xlim(start_position - spacing / 2, position - spacing / 2)

        # Take care of legend elements and delete unused plots (if wanted)
        handles, labels = [], []
        for idx, ax in enumerate(axs.flat):
            if delete_unused_axes and idx > self.n_parameters - 1:
                fig.delaxes(ax)
            for handle, label in zip(*ax.get_legend_handles_labels()):
                if label not in labels:
                    handles.append(handle)
                    labels.append(label)

        return fig, axs, handles, labels
