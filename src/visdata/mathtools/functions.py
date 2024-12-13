import numpy as np


def sec(*args, **kwargs):
    """Return the secans of an angle (see numpy.cos for docs)."""
    return 1 / np.cos(*args, **kwargs)

def sin2(*args, **kwargs):
    """Return the sin^2 of an angle (see numpy.sin for docs)."""
    return np.sin(*args, **kwargs) ** 2

def cos2(*args, **kwargs):
    """Return the cos^2 of an angle (see numpy.cos for docs)."""
    return np.cos(*args, **kwargs) ** 2

def deg2sec(deg, *args, **kwargs):
    """Return the secans of an angle/deg (see numpy.cos for docs)."""
    return sec(np.deg2rad(deg), *args, **kwargs)

def deg2sin2(deg, *args, **kwargs):
    """Return the sin^2 of an angle/deg (see numpy.sin for docs)."""
    return sin2(np.deg2rad(deg), *args, **kwargs)

def deg2cos2(deg, *args, **kwargs):
    """Return the cos^2 of an angle/deg (see numpy.cos for docs)."""
    return cos2(np.deg2rad(deg), *args, **kwargs)

def secspace(start, stop, **kwargs):
    """Return evenly in secans spaced numbers (see numpy.linspace for docs)."""
    return np.linspace(sec(start), sec(stop), **kwargs)

def sin2space(start, stop, **kwargs):
    """Return evenly in sin^2 spaced numbers (see numpy.linspace for docs)."""
    return np.linspace(sin2(start), sin2(stop), **kwargs)

def cos2space(start, stop, **kwargs):
    """Return evenly in cos^2 spaced numbers (see numpy.linspace for docs)."""
    return np.linspace(cos2(start), cos2(stop), **kwargs)

def deg2secspace(start_deg, stop_deg, **kwargs):
    """Return evenly in secans spaced numbers (see numpy.linspace for docs)."""
    return np.linspace(deg2sec(start_deg), deg2sec(stop_deg), **kwargs)

def deg2sin2space(start_deg, stop_deg, **kwargs):
    """Return evenly in sin^2 spaced numbers (see numpy.linspace for docs)."""
    return np.linspace(deg2sin2(start_deg), deg2sin2(stop_deg), **kwargs)

def deg2cos2space(start_deg, stop_deg, **kwargs):
    """Return evenly in cos^2 spaced numbers (see numpy.linspace for docs)."""
    return np.linspace(deg2cos2(start_deg), deg2cos2(stop_deg), **kwargs)
