# Author - Piyush Yadav
# Insight Centre for Data Analytics
# Package- VidWIN Project

class VertexObject:
    # define the different attributes for vertex objects
    def __init__(self,vertex_id, vertex_label,confidence):
        self.vertex_id = vertex_id
        self.vertex_label = vertex_label
        self.confidence = confidence

    #definiting the getter and setter using properties
    @property
    def vertex_id(self,vertex_id):
        """I'm the 'x' property."""
        return self.vertex_id

    @vertex_id.setter
    def vertex_id(self, vertex_id):
        self.vertex_id = vertex_id

    @vertex_id.deleter
    def vertex_id(self):
        del self.vertex_id




