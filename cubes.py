from cube import Cube
from camera import Camera
from skybox import Skybox
import glm

class Cubes:
    def __init__(self, main):
        self.main = main
        self.WIND_SIZE = main.WIND_SIZE
        self.world_length =  main.world_length
        self.world_width = main.world_width
        self.world_height = main.world_height
        self.camera = Camera(main)
        self.voxels = self.create_voxels()
        self.visible_voxel_faces = self.visible_faces()
                
        self.cubes = {}
        for x in range(-(self.world_length//2), (self.world_length+1)//2):
            for y in range(-(self.world_height//2), (self.world_height+1)//2):
                for z in range(-(self.world_width//2), (self.world_width+1)//2):
                    cube_pos = (x, y, -z)
                    cube = Cube('dillon32', main, cube_pos, self.visible_voxel_faces)
                    self.cubes[cube_pos] = cube
                    if not cube.visible:
                        self.voxels[cube_pos] = 0

        self.skybox = Skybox(main)
        
    def create_voxels(self):
        x = self.main.world_length
        y = self.main.world_height
        z = self.main.world_width
        voxels = {}

        for x in range(-(self.world_length//2), (self.world_length+1)//2):
            for y in range(-(self.world_height//2), (self.world_height+1)//2):
                for z in range(-(self.world_width//2), (self.world_width+1)//2):
                    voxel_pos = (x, y, -z)
                    voxels[voxel_pos] = 1 # filled
        return voxels
    
    def is_empty(self, voxel_pos):
        x, y, z = voxel_pos
        if -(self.world_length//2) <= x < self.world_length//2 and -(self.world_height//2) <= y < self.main.world_height//2 and -(self.world_length//2)+1 <= z < (self.main.world_width//2)+1:
            if self.voxels[voxel_pos] == 1:
                return False
        return True
    
    def visible_faces(self):
        visible_voxel_faces = {}
        for x in range(-(self.world_length//2), (self.world_length+1)//2):
            for y in range(-(self.world_height//2), (self.world_height+1)//2):
                for z in range(-(self.world_width//2), (self.world_width+1)//2):
                    x_coord, y_coord, z_coord = x, y, -z
                    if self.is_empty((x_coord, y_coord, z_coord+1)): # front is visible
                        visible_voxel_faces[(x_coord, y_coord, z_coord, 0)] = 1

                    if self.is_empty((x_coord+1, y_coord, z_coord)): # right is visible
                        visible_voxel_faces[(x_coord, y_coord, z_coord, 1)] = 1
        
                    if self.is_empty((x_coord, y_coord, z_coord-1)): # back is visible
                        visible_voxel_faces[(x_coord, y_coord, z_coord, 2)] = 1
            
                    if self.is_empty((x_coord-1, y_coord, z_coord)): # left is visible
                        visible_voxel_faces[(x_coord, y_coord, z_coord, 3)] = 1
              
                    if self.is_empty((x_coord, y_coord+1, z_coord)): # top is visible
                        visible_voxel_faces[(x_coord, y_coord, z_coord, 4)] = 1

                    if self.is_empty((x_coord, y_coord-1, z_coord)): # bottom is visible
                        visible_voxel_faces[(x_coord, y_coord, z_coord, 5)] = 1
        return visible_voxel_faces

    def render(self):
        self.camera.update()
        for cube in self.cubes.values():
            if (self.voxels[cube.pos] == 1):
                cube.shader_program['view_matrix'].write(self.camera.view_matrix)
                cube.shader_program['proj_matrix'].write(self.camera.proj_matrix) # pass in the parameter proj_matrix with the value of the camera proj_matrix
                cube.render()
                cube.shader_program['view_matrix'].write(self.camera.view_matrix)
    
        self.skybox.sky_shader_program['view_matrix'].write(glm.mat4(glm.mat3(self.camera.view_matrix)))
        self.skybox.sky_shader_program['proj_matrix'].write(self.camera.proj_matrix)
        self.skybox.render()
        self.skybox.sky_shader_program['view_matrix'].write(glm.mat4(glm.mat3(self.camera.view_matrix)))


    def clear(self):
        for cube in self.cubes.values():
            if (self.voxels[cube.pos] == 1):
                cube.clear()
        self.skybox.clear()
