from typing import Any
from typing import Optional

import bpy  # type: ignore

from compas.geometry import Cylinder
from compas.artists import GeometryArtist
from compas.colors import Color
from compas_blender import conversions
from .artist import BlenderArtist


class CylinderArtist(BlenderArtist, GeometryArtist):
    """Artist for drawing cylinder shapes in Blender.

    Parameters
    ----------
    cylinder : :class:`~compas.geometry.Cylinder`
        A COMPAS cylinder.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.GeometryArtist`.

    """

    def __init__(self, cylinder: Cylinder, **kwargs: Any):
        super().__init__(geometry=cylinder, **kwargs)

    def draw(
        self,
        color: Optional[Color] = None,
        collection: Optional[str] = None,
        u: int = 16,
    ) -> bpy.types.Object:
        """Draw the cylinder associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the cylinder.
        collection : str, optional
            The Blender scene collection containing the created objects.
        u : int, optional
            Number of faces in the "u" direction.

        Returns
        -------
        :blender:`bpy.types.Object`
            The objects created in Blender.

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        vertices, faces = self.geometry.to_vertices_and_faces(u=u)
        mesh = conversions.vertices_and_faces_to_blender_mesh(vertices, faces, name=self.geometry.name)

        obj = self.create_object(mesh, name=name)
        self.update_object(obj, color=color, collection=collection, show_wire=True)

        return obj
