from contextlib import contextmanager

from matplotlib import pyplot as plt


def get_colorblind_style():
    """Return a style appropriate for colorblind people."""
    return "tableau-colorblind10"


def save_plot(fig, file, **kwargs):
    """Save a figure to file with some nice presettings."""
    fig.savefig(
        file,
        transparent=kwargs.pop("transparent", True),
        bbox_inches=kwargs.pop("bbox_inches", "tight"),
        pad_inches=kwargs.pop("pad_inches", 0.05),
        **kwargs
    )


def sort_legend(fig, ax):
    """Sort legend by labels."""
    handles, labels = ax.get_legend_handles_labels()
    sorted_handles = []
    sorted_labels = []
    for l, h in sorted(zip(labels, handles), key=lambda t: t[0]):
        sorted_labels.append(l)
        sorted_handles.append(h)

    ax.legend(sorted_handles, sorted_labels)


def get_latex_preamble(font=None, try_unknown_font=True):
    """Return the latex preamble for rc parameters."""
    if font is None:
        font = "libertinus"

    packages = [
        r"\usepackage{fontspec}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{amsmath}",
        r"\usepackage{amssymb}"
    ]
    match font:
        case "libertinus":
            packages.append(r"\usepackage{libertinus}")
        case "palatino":
            packages += [
                r"\usepackage{newpxtext}",
                r"\usepackage{newpxmath}"
            ]
        case _:
            if try_unknown_font:
                packages.append(rf"\usepackage{{{font}}}")

    return "\n".join(packages)


@contextmanager
def latex_output(
    font=None, figsize=None, backend=None, latex_preamble=None, rc_params=None,
    style=None
):
    """Context manager for latex output, this will close all existing plots."""
    if figsize is None:
        figsize = (5, 3)
    if backend is None:
        backend = "pgf"
    if latex_preamble is None:
        latex_preamble = get_latex_preamble(font=font)
    if rc_params is None:
        rc_params = {
            # "backend": backend,
            "figure.figsize": figsize,
            "font.family": "serif",
            "text.usetex": True,
            "pgf.rcfonts": False,
            "pgf.preamble": latex_preamble
        }

    with plt.rc_context(rc=rc_params) as mp_latex_context_manager:
        # Like always matplolib does not work as expected, so manually switch
        # and switch back the backend
        plt.close("all")
        org_backend = plt.get_backend()
        print(f"BACKEND SWITCH: {org_backend} to {backend}")
        plt.switch_backend(backend)
        try:
            if style is not None:
                with plt.style.context(style) as mp_style_context_manager:
                    yield mp_style_context_manager, mp_latex_context_manager
            else:
                yield mp_latex_context_manager
        finally:
            print(f"BACKEND SWITCH: {backend} to {org_backend}")
            plt.switch_backend(org_backend)


if __name__ == "__main__":
    def test_plot():
        # plt.style.use("tableau-colorblind10")
        fig, ax = plt.subplots()
        x = range(1, 20, 1)[:10]
        y = range(1, 100, 3)[:10]
        y2 = range(1, 50, 2)[:10]
        y3 = range(1, 55, 5)[:10]
        ax.plot(x, y)
        ax.plot(x, y2)
        ax.plot(x, y3)
        ax.set_xlabel(r"$\mathcal{R}=2$")

        return fig, ax

    file1 = "../test1.pdf"
    fig, ax = test_plot()
    # plt.show()
    save_plot(fig, file1)
    file2 = "../test2.pdf"
    with latex_output(style=get_colorblind_style()):
        fig, ax = test_plot()
        save_plot(fig, file2)
