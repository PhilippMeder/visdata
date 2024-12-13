import numpy as np


def logbins(values, n_bins, log_func=None):
    """Create logaritmic bins (default log10)."""
    if log_func is None:
        log_func = np.log10

    return np.logspace(
        log_func(min(values)), log_func(max(values)), n_bins + 1
    )


def bin_centers(bin_edges):
    """Return bin centers for given bin edges supporting unequal bins."""
    bin_centers = [
        (bin_edges[idx] + bin_edges[idx + 1]) / 2 for idx in range(len(bin_edges) - 1)
    ]

    return bin_centers


def which_bin(data, bin_edges):
    """Select bin id for given data."""
    bin_id = None
    for idx in range(len(bin_edges) - 1):
        if data >= bin_edges[idx]:
            bin_id = idx
        else:
            break

    if bin_id is None:
        raise ValueError(f"DATA OUT OF RANGE! {data} not in {bin_edges}!")

    return bin_id
