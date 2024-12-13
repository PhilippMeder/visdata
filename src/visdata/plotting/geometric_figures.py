from abc import ABC

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import RegularPolygon


class BaseRegularPolygon(ABC, RegularPolygon):

    _name = "Regular Polygon base class"
    _n_corners = None

    def __init__(self, xy, radius=1, radius_is_edge_length=False, **kwargs):
        self._set_geometric_properties(radius, radius_is_edge_length)
        super().__init__(
            xy, self.n_corners, radius=self.circumradius, **kwargs
        )

    def get_trigonometrics_of_pi_div_n(self):
        """Return sin(pi/n), sin(2pi/n), cos(pi/n)."""
        pi_div_n = np.pi / self.n_corners

        return np.sin(pi_div_n), np.sin(2 * pi_div_n), np.cos(pi_div_n)

    def _set_geometric_properties(self, radius, is_edge_length):
        """Calculate and set geometric properties."""
        sin_a, sin_2a, cos_a = self.get_trigonometrics_of_pi_div_n()

        if is_edge_length:
            r = radius / (2 * sin_a)
            self._corner_distance = radius
        else:
            r = radius
            self._corner_distance = 2 * r * sin_a

        self._circumradius = r
        self._inradius = r * cos_a
        self._area = self.n_corners * r ** 2 * sin_2a / 2

    @property
    def name(self):
        """Return name."""
        return self._name

    @property
    def circumradius(self):
        """Return radius (distance center-corner)."""
        return self._circumradius

    @property
    def n_corners(self):
        """Return number of corners."""
        return self._n_corners

    @property
    def corner_distance(self):
        """Return distance between corners."""
        return self._corner_distance

    @property
    def inradius(self):
        """Return the height/inradius."""
        return self._inradius

    @property
    def height(self):
        """Return the height/inradius."""
        return self._inradius

    @property
    def area(self):
        """Return the area."""
        return self._area

    def __str__(self):
        """Return string representation."""
        tab = f"{'':2}"
        return (
            f"{self.name}\n"
            f"{tab}{'circumradius':16}{tab}{'R':2}{tab}{self.circumradius}\n"
            f"{tab}{'inradius':16}{tab}{'r':2}{tab}{self.inradius}\n"
            f"{tab}{'corner distance':16}{tab}{'a':2}{tab}"
            f"{self.corner_distance}\n"
            f"{tab}{'area':16}{tab}{'A':2}{tab}{self.area}\n"
        )


class RegularTriangle(BaseRegularPolygon):

    _name = "Regular Triangle"
    _n_corners = 3

    def get_trigonometrics_of_pi_div_n(self):
        """
        Return sin(pi/n), sin(2pi/n), cos(pi/n).

        Implementation of exact values reduces rounding errors.
        """
        sqrt3_div_2 = np.sqrt(3) / 2

        return sqrt3_div_2, sqrt3_div_2, 0.5


class RegularSquare(BaseRegularPolygon):

    _name = "Regular Square"
    _n_corners = 4

    def get_trigonometrics_of_pi_div_n(self):
        """
        Return sin(pi/n), sin(2pi/n), cos(pi/n).

        Implementation of exact values reduces rounding errors.
        """
        div_sqrt2 = 1 / np.sqrt(2)

        return div_sqrt2, 1, div_sqrt2


class RegularHexagon(BaseRegularPolygon):

    _name = "Regular Hexagon"
    _n_corners = 6

    def get_trigonometrics_of_pi_div_n(self):
        """
        Return sin(pi/n), sin(2pi/n), cos(pi/n).

        Implementation of exact values reduces rounding errors.
        """
        sqrt3_div_2 = np.sqrt(3) / 2

        return 0.5, sqrt3_div_2, sqrt3_div_2
