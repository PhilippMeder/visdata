from matplotlib import pyplot as plt
from visdata import Measurement, MeasurementResult, MeasurementResultPlotConfig, CompareMeasurementsPlot, object_vars_str
from visdata.decorators import timer


@timer
def get_example_measurements():
    own_measurement = Measurement(
        "Own measurement",
        {
            r"$\alpha$": MeasurementResult(1, statistical=0.1, systematic=0.05),
            r"$\beta$": MeasurementResult(9.3, statistical=0.05, systematic=0.1),
            r"$\gamma$": MeasurementResult(3, statistical=0.2, systematic=0.3),
            r"$\delta$": MeasurementResult(2, statistical=0.3, systematic=0.35),
        }
    )

    publication_1 = Measurement(
        "Publication 1",
        {
            r"$\alpha$": MeasurementResult(1.3, statistical=0.1, systematic=0.4),
            r"$\gamma$": MeasurementResult(3.5, statistical=0.2, systematic=0.3),
        }
    )

    publication_2 = Measurement(
        "Publication 2",
        {
            r"$\alpha$": MeasurementResult(0.9, statistical=0.08, systematic=0.1),
            r"$\beta$": MeasurementResult(8, statistical=0.8, systematic=0.9),
            r"$\delta$": MeasurementResult(2.2, statistical=0.08, systematic=0.15),
        }
    )

    return own_measurement, publication_1, publication_2


@timer
def make_plot(measurements, **kwargs):
    compare_plot = CompareMeasurementsPlot(*measurements, **kwargs)
    fig, axs, handles, labels = compare_plot.plot(ncols=3)
    fig.legend(handles, labels, loc="lower right", bbox_to_anchor=(0.985, 0.035), frameon=False)
    fig.tight_layout()

    return fig


if __name__ == "__main__":
    # from visdata.plotting.matplotlib_util import latex_output, save_plot
    # with latex_output():
    measurements = get_example_measurements()
    fig = make_plot(measurements)
    # save_plot(fig, "compare_measurements.pdf")
    # save_plot(fig, "compare_measurements.png")
    plt.show()

    # config = MeasurementResultPlotConfig()
    # print(object_vars_str(config))

    # config2 = MeasurementResultPlotConfig(total={"alpha": 0.7})
    # print(object_vars_str(config2))

    # config = MeasurementResultPlotConfig()
    # print(object_vars_str(config))
