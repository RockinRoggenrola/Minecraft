from cube import Cube
from camera import Camera
from skybox import Skybox
import glm

class Cubes:
    def __init__(self, main):
        self.WIND_SIZE = main.WIND_SIZE
        self.world_length =  20
        self.world_width = 20
        self.camera = Camera(main)
        
        self.cubes = [] 
        for x in range(-(self.world_length//2), (self.world_length+1)//2):
            for z in range(-(self.world_width//2), (self.world_width+1)//2):
                self.cubes.append(Cube('dillon16', main, (2*x, 0, -2*z)))
        self.cubes.append(Cube('dillon16', main, (0, 2, 0)))

        self.skybox = Skybox(main)
        
    def render(self):
        self.camera.update()
        for cube in self.cubes:
            cube.shader_program['view_matrix'].write(self.camera.view_matrix)
            cube.shader_program['proj_matrix'].write(self.camera.proj_matrix) # pass in the parameter proj_matrix with the value of the camera proj_matrix
            cube.render()
            cube.shader_program['view_matrix'].write(self.camera.view_matrix)
    
        self.skybox.sky_shader_program['view_matrix'].write(glm.mat4(glm.mat3(self.camera.view_matrix)))
        self.skybox.sky_shader_program['proj_matrix'].write(self.camera.proj_matrix)
        self.skybox.render()
        self.skybox.sky_shader_program['view_matrix'].write(glm.mat4(glm.mat3(self.camera.view_matrix)))


    def clear(self):
        for cube in self.cubes:
            cube.clear()
        self.skybox.clear()
