from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import math

from compas.geometry import close
from compas.geometry import Frame
from compas.geometry import Circle
from .curve import Curve

PI2 = 2.0 * math.pi


class Arc(Curve):
    """An arc is a segment of a circle, and is defined by a coordinate system, radius, and start and end angles.

    The centre of the underlying circle is at the origin of the coordinate system.
    The start and end angles are measured from the positive X axis towards the positive Y axis.
    The parameter domain of the arc is defined by the start and end angles.
    It is a subset of the domain of the circle.

    Transformations of the arc are performed by transforming the local coordinate system.
    They are limited to (combinations of) translations and rotations.
    All other components of transformations are ignored.

    Parameters
    ----------
    frame : :class:`~compas.geometry.Frame`
        Coordinate frame at the center of the arc's circle.
    radius : float
        Radius of the arc's circle.
    start_angle : float, optional
        The angle in radians of the start of this Arc.
        Defaults to 0.0.
    end_angle : float, optional
        The angle in radians of the end of this Arc.
        Defaults to `pi` (180 degrees).

    Attributes
    ----------
    frame : :class:`~compas.geometry.Frame`
        The coordinate frame of the arc.
    radius : float
        The radius of the circle.
    start_angle : float
        The start angle of the arc.
    end_angle : float
        The end angle of the arc.
    circle : :class:`~compas.geometry.Circle`
        The underlying circle.
    center : :class:`~compas.geometry.Point`
        The center of the underlying circle.
    plane : :class:`~compas.geometry.Plane`, read-only
        The plane of the arc.
    normal : :class:`~compas.geometry.Vector`, read-only
        The normal of the arc plane.
    diameter : float, read-only
        The diameter of the underlying circle.
    length : float
        The length of the arc.
    angle : float, read-only
        The sweep angle in radians between start angle and end angle.
    circumference : float, read-only
        The circumference of the underlying circle.
    domain : tuple(float, float), read-only
        The parameter domain of the arc.
    start : :class:`~compas.geometry.Point`, read-only
        The start point of the arc.
    end : :class:`~compas.geometry.Point`, read-only
        The end point of the arc.
    is_closed : bool, read-only
        ``True`` if the arc is closed.
    transformation : :class:`Transformation`, read-only
        The transformation from the local coordinate system of the arc (:attr:`frame`) to the world coordinate system.

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "frame": Frame.JSONSCHEMA,
            "radius": {"type": "number", "minimum": 0},
            "start_angle": {"type": "number", "minimum": 0, "optional": True},
            "end_angle": {"type": "number", "minimum": 0},
        },
        "required": ["frame", "radius", "start_angle", "end_angle"],
    }

    # overwriting the __new__ method is necessary
    # to avoid triggering the plugin mechanism of the base curve class
    def __new__(cls, *args, **kwargs):
        curve = object.__new__(cls)
        curve.__init__(*args, **kwargs)
        return curve

    def __init__(self, frame=None, radius=None, start_angle=0.0, end_angle=math.pi, **kwargs):
        super(Arc, self).__init__(frame=frame, **kwargs)

        self._radius = None
        self._start_angle = None
        self._end_angle = None

        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle

    def __repr__(self):
        return "Arc({0!r}, {1!r}, {2!r}, {3!r})".format(
            self.frame,
            self.radius,
            self.start_angle,
            self.end_angle,
        )

    def __len__(self):
        return 4

    def __getitem__(self, key):
        if key == 0:
            return self.frame
        elif key == 1:
            return self.radius
        elif key == 2:
            return self.start_angle
        elif key == 3:
            return self.end_angle
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.frame = value
        elif key == 1:
            self.radius = value
        elif key == 2:
            self.start_angle = value
        elif key == 3:
            self.end_angle = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.frame, self.radius, self.start_angle, self.end_angle])

    def __eq__(self, other):
        try:
            other_frame = other[0]
            other_radius = other[1]
            other_start = other[2]
            other_end = other[3]
        except Exception:
            return False
        return (
            self.frame == other_frame
            and self.radius == other_radius
            and self.start_angle == other_start
            and self.end_angle == other_end
        )

    # =============================================================================
    # Data
    # =============================================================================

    @property
    def data(self):
        return {
            "frame": self._frame,
            "radius": self._radius,
            "start_angle": self._start_angle,
            "end_angle": self._end_angle,
        }

    @data.setter
    def data(self, value):
        self.frame = value["frame"]
        self.radius = value["radius"]
        self.start_angle = value["start_angle"]
        self.end_angle = value["end_angle"]

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def radius(self):
        if self._radius is None:
            raise ValueError("Radius not set.")
        return self._radius

    @radius.setter
    def radius(self, value):
        if value <= 0.0:
            raise ValueError("Radius must be greater than or equal to zero.")
        self._radius = value

    @property
    def start_angle(self):
        if self._start_angle is None:
            self._start_angle = 0.0
        return self._start_angle

    @start_angle.setter
    def start_angle(self, value):
        if value < 0.0 or value > PI2:
            raise ValueError("Start angle must satisfy 0 <= angle <= 2 * pi.")
        self._start_angle = value

    @property
    def end_angle(self):
        if self._end_angle is None:
            raise ValueError("End angle not set.")
        return self._end_angle

    @end_angle.setter
    def end_angle(self, value):
        if value < 0.0 or value > PI2:
            raise ValueError("End angle must satisfy 0 <= angle <= 2 * pi.")
        self._end_angle = value

    @property
    def circle(self):
        return Circle(self.frame, self.radius)

    @property
    def length(self):
        return self.radius * self.angle

    @property
    def angle(self):
        return self.end_angle - self.start_angle

    # @property
    # def domain(self):
    #     return self.start_angle, self.end_angle

    @property
    def center(self):
        return self.frame.point

    @property
    def diameter(self):
        return 2.0 * self.radius

    @property
    def circumference(self):
        return self.diameter * math.pi

    @property
    def is_circle(self):
        return close(abs(abs(self.angle) - PI2), 0.0)

    @property
    def is_closed(self):
        return False

    @property
    def is_periodic(self):
        return False

    def _verify(self):
        if self.angle < 0.0 or self.angle > PI2:
            raise ValueError("Sweep angle must satisfy 0 < angle < 2 * Pi. Currently:{}".format(self.angle))

    # =============================================================================
    # Constructors
    # =============================================================================

    @classmethod
    def from_circle(cls, circle, start_angle, end_angle):
        """Creates an Arc from a circle and start and end angles.

        Parameters
        ----------
        circle : :class:`~compas.geometry.Circle`
            The frame and radius of this circle will be used to create an Arc.
        start_angle : float
            The start angle in radians.
        end_angle : float
            The end angle in radians.

        Returns
        -------
        :class:`~compas.geometry.Arc`

        """
        return cls(
            frame=circle.frame,
            radius=circle.radius,
            start_angle=start_angle,
            end_angle=end_angle,
        )

    # =============================================================================
    # Methods
    # =============================================================================