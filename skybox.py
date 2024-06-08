import pygame as pg
import numpy as np

class Skybox:
    def __init__(self, main):
        self.context = main.context
        self.sky_box_vbo = self.vertex_buffer_object(self.sky_box_vertice_data())

        self.sky_shader_program = self.shaders('sky_box')

        self.sky_box_vao = self.sky_vao()

        self.sky_texture = self.sky_texture_cube()
        
        self.sky_shader_program['skybox_texture'] = 0
        self.sky_texture.use()
        
    def shaders(self, shader_name): # vertex shader transforms the vertices from model space(original coord sys) to clip space (coord system of the camera)
        vfile_path = 'shaders/{shader_name}.vert'
        vfile_path = vfile_path.format(shader_name = shader_name)
        with open(vfile_path) as file:
            vertex_shader = file.read()
        ffile_path = 'shaders/{shader_name}.frag'
        ffile_path = ffile_path.format(shader_name = shader_name)   
        with open (ffile_path) as file:
            fragment_shader = file.read()
        shader_program = self.context.program(vertex_shader = vertex_shader, fragment_shader=fragment_shader) # compile shaders using CPU to be used by GPU
        return shader_program
    
    def vertex_buffer_object(self, data):
        vertice_data = data
        # send vertex data from CPU to GPU using a vertex buffer object (holds all attributes (raw data) of each vertex)
        vbo = self.context.buffer(data)
        return vbo
    
    def sky_vao(self):
        vao = self.context.vertex_array(self.sky_shader_program, [(self.sky_box_vbo, '3f', 'vertex_position')]) # in the buffer each vertex is assigned 3 float numbers(x,y,z), these 3 numbers correspond to the input attribute in_position
        return vao
    
    def sky_texture_cube(self):
        cube_faces = ["right", "left", "top", "bottom", "front", "back"]
        textures = []
        for face in cube_faces:
            texture_path = 'textures/skybox/{face}.png'
            texture_path = texture_path.format(face = face)
            textures.append(pg.image.load(texture_path).convert())
            
        sky_texture_cube = self.context.texture_cube(textures[0].get_size(), 3, None)
        
        for i in range(6):
            texture_data = pg.image.tobytes(textures[i], 'RGB')
            sky_texture_cube.write(i, texture_data)

        return sky_texture_cube
    
    def sky_box_vertice_data(self):
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]   
        
        triangle_indices = [(0, 2, 3), (0, 1, 2),
                            (1, 7, 2), (1, 6, 7),
                            (6, 5, 4), (4, 7, 6),
                            (3, 4, 5), (3, 5, 0),
                            (3, 7, 4), (3, 2, 7),   
                            (0, 6, 1), (0, 5, 6)]
        vertice_data = []

        for triangle in triangle_indices:
            for index in triangle:
                vertice_data.append(vertices[index])
        vertice_data = np.array(vertice_data, dtype = 'f4')
        vertice_data = np.fliplr(vertice_data).copy('C')
        return vertice_data

    def render(self):
        self.sky_box_vao.render()

    def clear(self): # remove all created resources
        self.sky_box_vbo.release()
        self.sky_shader_program.release()
        self.sky_box_vao.release()
        self.sky_texture.release()

