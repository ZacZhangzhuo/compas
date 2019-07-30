

from compas.geometry.transformations import quaternion_multiply
from compas.geometry.transformations import quaternion_conjugate
from compas.geometry.transformations import quaternion_unitize
from compas.geometry.transformations import quaternion_canonize
from compas.geometry.transformations import quaternion_norm
from compas.geometry.transformations import quaternion_is_unit

from compas.geometry.basic import allclose

__all__ = ['Quaternion']


class Quaternion(object):

    """Creates a ``Quaternion`` object.

    Parameters
    ----------
    w : float
        The scalar (real) part of a quaternion.
    x, y, z : float
        Components of the vector (complex, imaginary) part of a quaternion.


    Examples
    --------
    >>> Q = Quaternion(1.0, 1.0, 1.0, 1.0).unitized
    >>> R = Quaternion(0.0,-0.1, 0.2,-0.3).unitized
    >>> P = R*Q
    >>> P.is_unit
    True

    Notes
    -----
    The default convention to represent a quaternion :math:`q` in this module is by four real values **w**, **x**, **y**, **z**.
    The first value **w** is the scalar (real) part, and **x**, **y**, **z** form the vector (complex, imaginary) part [1]_, so that:

    :math:`q = w + xi + yj + zk`

    where :math:`i, j, k` are basis components with following multiplication rules [2]_:

    :math:`ii = jj = kk = ijk = -1`

    :math:`ij = k,\\qquad ji = -k`

    :math:`jk = i,\\qquad kj = -i`

    :math:`ki = j,\\qquad ik = -j`

    Quaternions are associative but not commutative.


    **Quaternion as rotation.**
    A rotation through an angle :math:`\\theta` around an axis defined by a euclidean unit vector :math:`u = u_{x}i + u_{y}j + u_{z}k`
    can be represented as a quaternion:

    :math:`q = cos(\\frac{\\theta}{2}) + sin(\\frac{\\theta}{2})  [u_{x}i + u_{y}j + u_{z}k]`

    i.e.:

    :math:`w = cos(\\frac{\\theta}{2})`

    :math:`x = sin(\\frac{\\theta}{2})  u_{x}`

    :math:`y = sin(\\frac{\\theta}{2})  u_{y}`

    :math:`z = sin(\\frac{\\theta}{2})  u_{z}`

    For a quaternion to represent a rotation or orientation, it must be unit-length.
    A quaternion representing a rotation :math:`p` resulting from applying a rotation :math:`r` to a rotation :math:`q`, i.e.:
    :math:`p = rq`,
    is also unit-length.


    References
    ----------
    .. [1] http://mathworld.wolfram.com/Quaternion.html
    .. [2] http://mathworld.wolfram.com/HamiltonsRules.html
    .. [3] https://github.com/matthew-brett/transforms3d/blob/master/transforms3d/quaternions.py

    """

    def __init__(self, w, x, y, z):

        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __iter__(self):
        return iter([self.w, self.x, self.y, self.z])

    def __str__(self):
        return "Quaternion = %s" % list(self)

    def __repr__(self):
        return 'Quaternion({:.{prec}f}, {:.{prec}f}, {:.{prec}f}, {:.{prec}f})'.format(*self, prec=6)

    def __mul__(self, other):
        """Multiply operator for two quaternions.

        Parameters
        ----------
        other
            A Quaternion object.

        Returns
        -------
        Quaternion
            The product P = R * Q of this quaternion (R) multiplied by other quaternion (Q).

        Examples
        --------
        >>> Q = Quaternion(1.0, 1.0, 1.0, 1.0).unitized
        >>> R = Quaternion(0.0,-0.1, 0.2,-0.3).unitized
        >>> P = R*Q
        >>> P.is_unit
        True

        Notes
        -----
        Multiplication of two quaternions R*Q can be interpreted as applying rotation R to an orientation Q,
        provided that both R and Q are unit-length.
        The result is also unit-length.
        Multiplication of quaternions is not commutative!

        """
        p = quaternion_multiply(list(self), list(other))
        return Quaternion(*p)

    @classmethod
    def from_frame(cls, frame):
        """Creates a ``Quaternion`` object from a ``Frame`` object.

        Parameters
        ----------
        frame : :obj:`Frame`

        Returns
        -------
        :obj:`Quaternion`
            The new constructed ``Quaternion`` object.

        Example
        -------
        >>> from compas.geometry import Frame
        >>> q = [1., -2., 3., -4.]
        >>> F = Frame.from_quaternion(q)
        >>> Q = Quaternion.from_frame(F)
        >>> allclose(list(Q.canonized), quaternion_canonize(quaternion_unitize(q)))
        True
        """

        w, x, y, z = frame.quaternion
        return cls(w, x, y, z)

    @property
    def wxyz(self):
        """
        Returns the quaternion as a list of float in the "wxyz" convention.
        """
        return [self.w, self.x, self.y, self.z]

    @property
    def xyzw(self):
        """
        Returns the quaternion as a list of float in the "xyzw" convention.
        """
        return [self.x, self.y, self.z, self.w]

    @property
    def conjugate(self):
        """
        Returns a conjugate :obj:`Quaternion`.
        """
        qc = quaternion_conjugate(list(self))
        return Quaternion(*qc)

    def unitize(self):
        """
        Scales the quaternion to make it unit-length.
        """
        qu = quaternion_unitize(list(self))
        self.w, self.x, self.y, self.z = qu

    @property
    def is_unit(self):
        """
        Returns ``True`` if the quaternion is unit-length or ``False`` if otherwise.
        """
        return quaternion_is_unit(list(self))

    @property
    def unitized(self):
        """
        Returns a :obj:`Quaternion` with a unit-length.
        """
        qu = quaternion_unitize(list(self))
        return Quaternion(*qu)

    def canonize(self):
        """
        Makes the quaternion canonic.
        """
        qc = quaternion_canonize(list(self))
        self.w, self.x, self.y, self.z = qc

    @property
    def canonized(self):
        """
        Returns a :obj:`Quaternion` in a canonic form.
        """
        qc = quaternion_canonize(list(self))
        return Quaternion(*qc)

    @property
    def norm(self):
        """
        Returns the length (euclidean norm) of the quaternion.
        """
        return quaternion_norm(list(self))


if __name__ == "__main__":
    import doctest
    doctest.testmod(globs=globals())


