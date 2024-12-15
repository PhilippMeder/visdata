from matplotlib import pyplot as plt

from visdata import Profile2d


class Histogram2d:

    def __init__(self, x, y, bins=10, xlabel=None, ylabel=None, clabel=None):
        self._x = x
        self._y = y
        self._bins = bins

        self.xlabel = xlabel if xlabel is not None else "$x$-data"
        self.ylabel = ylabel if ylabel is not None else "$y$-data"
        self.clabel = clabel if clabel is not None else "$n$"

        self.configure_marginal()
        self.configure_profile()

    def configure_marginal(self, **kwargs):
        self._marginal_kwargs = kwargs

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

    def hist2d(self, subplot=None, colorbar_ax=None ,**kwargs):
        fig, ax = self.get_subplot(subplot)
        hist, xedges, yedges, image = ax.hist2d(self._x, self._y, bins=self._bins, **kwargs)
        fig.colorbar(image, ax=colorbar_ax, label=self.clabel)

        return fig, ax

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

    def plot(self, marginal=False, profile=False, **kwargs):
        if marginal:
            # TODO: Maybe we can use something better, e.g. subplot2grid
            fig = plt.figure()
            grid_spec = fig.add_gridspec(3, 3, wspace=0, hspace=0)
            ax_hist2d = fig.add_subplot(grid_spec[1:, :-1])
            ax_hist_x = fig.add_subplot(grid_spec[0, :-1], sharex=ax_hist2d)
            ax_hist_y = fig.add_subplot(grid_spec[1:, -1], sharey=ax_hist2d)
            colorbar_ax = ax_hist_y
            axs = (ax_hist2d, ax_hist_x, ax_hist_y)
        else:
            fig, ax_hist2d = plt.subplots()
            colorbar_ax = None
            axs = ax_hist2d

        # Create plots
        self.hist2d(subplot=(fig, ax_hist2d), colorbar_ax=colorbar_ax, **kwargs)
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
        return fig, axs
