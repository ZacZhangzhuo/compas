
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    import bpy
except ImportError:
    pass

from compas.datastructures import Mesh

from compas.geometry import add_vectors
from compas.geometry import distance_point_point
from compas.geometry import subtract_vectors

from compas_blender.geometry import BlenderGeometry


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'BlenderMesh',
]


class BlenderMesh(BlenderGeometry):

    def __init__(self, object):
        super(BlenderMesh, self).__init__(object)


    # ------------------------------------------------------------------------------------
    # Vertices
    # ------------------------------------------------------------------------------------

    def get_vertex_coordinates(self, vertex):
        
        return add_vectors(self.location, self.geometry.vertices[vertex].co)
        

    def get_vertices_coordinates(self):

        xyzs = [list(i.co) for i in self.geometry.vertices]

        return {vertex: add_vectors(self.location, xyz) for vertex, xyz in enumerate(xyzs)}


    def set_vertices_coordinates(self, xyzs):

        for vertex, xyz in xyzs.items():
            self.geometry.vertices[vertex].co = subtract_vectors(xyz, self.location)


    def get_vertices_colors(self, vertices=None):

        colors = {}
        col    = self.geometry.vertex_colors.active

        if col:

            if not vertices:
                vertices = range(len(self.geometry.vertices))

            for face in self.geometry.polygons:
                for i in face.loop_indices:
                    
                    j = self.geometry.loops[i].vertex_index

                    if (j in vertices) and (not colors.get(j, None)):
                        colors[j] = list(col.data[i].color)[:3]

            return colors

        return


    def set_vertices_colors(self, colors):

        if self.geometry.vertex_colors:
            col = self.geometry.vertex_colors.active
            
        else:
            col = self.geometry.vertex_colors.new()

        for face in self.geometry.polygons:
            for i in face.loop_indices:
                
                j = self.geometry.loops[i].vertex_index

                if j in colors:
                    col.data[i].color = list(colors[j]) + [1]


    def unset_vertices_colors(self):

        vertex_colors = self.geometry.vertex_colors

        while vertex_colors:
            vertex_colors.remove(vertex_colors[0])


    def get_vertex_index(self):

        raise NotImplementedError


    def get_vertices_indices(self):

        raise NotImplementedError


    def get_vertex_face_indices(self):

        raise NotImplementedError


    def get_vertices_face_indices(self):

        raise NotImplementedError


    # ------------------------------------------------------------------------------------
    # Edges
    # ------------------------------------------------------------------------------------

    def get_edge_vertex_indices(self, edge):
        
        return list(self.geometry.edges[edge].vertices)
    

    def get_edges_vertex_indices(self, edges=None):

        if not edges:
            edges = range(len(self.geometry.edges))

        return {edge: self.get_edge_vertex_indices(edge=edge) for edge in edges}


    def get_edge_index(self):

        raise NotImplementedError


    def get_edges_indices(self):

        raise NotImplementedError


    def edge_length(self, edge):

        u, v   = self.geometry.edges[edge].vertices
        sp, ep = [list(self.geometry.vertices[i].co) for i in [u, v]]

        return distance_point_point(sp, ep)


    def edges_lengths(self, edges=None):
        
        if not edges:
            edges = range(len(self.geometry.edges))

        return {edge: self.edge_length(edge=edge) for edge in edges}


    # ------------------------------------------------------------------------------------
    # Faces
    # ------------------------------------------------------------------------------------

    def get_face_vertex_indices(self, face):
        
        return list(self.geometry.polygons[face].vertices)
        

    def get_faces_vertex_indices(self, faces=None):

        if not faces:
            faces = range(len(self.geometry.polygons))

        return {face: self.get_face_vertex_indices(face=face) for face in faces}
    
    
    def get_face_vertex_coordinates(self, face):

        raise NotImplementedError


    def get_faces_vertex_coordinates(self, faces=None):

        raise NotImplementedError


    def get_face_index(self):

        raise NotImplementedError


    def get_faces_indices(self):

        raise NotImplementedError


    def face_normal(self, face):

        return list(self.geometry.polygons[face].normal)


    def faces_normals(self, faces=None):

        if not faces:
            faces = range(len(self.geometry.polygons))

        return {face: self.face_normal(face=face) for face in faces}


    def face_area(self, face):

        return self.geometry.polygons[face].area


    def faces_areas(self, faces=None):

        if not faces:
            faces = range(len(self.geometry.polygons))

        return {face: self.face_area(face=face) for face in faces}


    # ------------------------------------------------------------------------------------
    # Other
    # ------------------------------------------------------------------------------------

    def get_vertices_and_faces(self):

        vertices = self.get_vertices_coordinates()
        faces    = self.get_faces_vertex_indices()

        return vertices, faces


    def get_border(self):

        raise NotImplementedError


    def closest_point(self, point, maxdist=None):

        raise NotImplementedError


    def closest_points(self, points, maxdist=None):

        raise NotImplementedError
        
        
    def to_datastructure(self):
        
        vertices = self.get_vertices_coordinates().values()
        faces    = self.get_faces_vertex_indices().values()
        
        return Mesh.from_vertices_and_faces(vertices=vertices, faces=faces)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    
    from compas_blender.utilities import get_object_by_name
    
    
    object = get_object_by_name(name='Cube')

    mesh = BlenderMesh(object)

    print(mesh.geometry)
    print(mesh.object)
    print(mesh.otype)
    print(mesh.name)
    print(mesh.location)

    #mesh.set_vertices_coordinates({0: [0, 0, 0], 1: [-1, -1, 0]})
    #mesh.set_vertices_colors(colors={0: [1, 0, 0], 1: [0, 0, 1], 2: [0, 1, 0]})
    #mesh.unset_vertices_colors()
    #mesh.refresh()

    #print(mesh.get_vertices_coordinates())
    #print(mesh.get_vertices_colors())
    #print(mesh.get_vertex_coordinates(vertex=0))

    #print(mesh.get_edge_vertex_indices(edge=4))
    #print(mesh.get_edges_vertex_indices(edges=[3, 4]))
    #print(mesh.edge_length(edge=2))
    #print(mesh.edges_lengths())
    
    #print(mesh.get_face_vertex_indices(face=4))
    #print(mesh.get_faces_vertex_indices())
    #print(mesh.face_normal(face=2))
    #print(mesh.faces_normals())
    #print(mesh.face_area(face=2))
    #print(mesh.faces_areas())
    #print(mesh.get_vertices_and_faces())
    
    datastructure = mesh.to_datastructure()
    
    print(datastructure)
