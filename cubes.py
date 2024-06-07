from cube import Cube
from camera import Camera

class Cubes:
    def __init__(self, main):
        self.WIND_SIZE = main.WIND_SIZE
        self.camera = Camera(main)
        self.cubes = {}
        for i in range(10):
            self.cubes[i] = Cube('JAMES_DILLON', main, (2*i, 0, 0))
            self.cubes[i].shader_program['view_matrix'].write(self.camera.view_matrix)
            self.cubes[i].shader_program['proj_matrix'].write(self.camera.proj_matrix) # pass in the parameter proj_matrix with the value of the camera proj_matrix
    
    
    def update(self):
        self.camera.update()
        for i in self.cubes:
            self.cubes[i].shader_program['view_matrix'].write(self.camera.view_matrix)
    
    def render(self):
        self.update()
        for i in self.cubes:
            self.cubes[i].render()
    def clear(self):
        for i in self.cubes:
            self.cubes[i].clear()
