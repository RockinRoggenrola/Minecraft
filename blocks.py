import numpy as np
import pygame as pg
import glm
from camera import Camera

class Block:
    def __init__(self, main):
        self.main = main
        self.context = main.context
        # openGL rendering pipline: pipline recieves info about the vertices, 
        # vertice shader processes each vertice. Vertices passed to primitive assembly, 
        # where assembly is carried out based on vertex connectivity info (what vertex 
        # connects to what vertex). Rasterization stage: primitive figure is divided into
        # fragments, and for each fragment the fragment shader is used to determine each
        # fragments' color. Then fragments undergo tests that make it a pixel and that pixel
        # is outputted to the FrameBuffer (rendering display)
        self.vbo = self.vertex_buffer_object()  
        self.shader_program = self.shaders('default')
        self.vao = self.vertex_array_object()
        self.texture = self.texture()
        self.camera = Camera(main.WIND_SIZE[0] / main.WIND_SIZE[1])
        self.model_matrix = glm.mat4(1.0)
        self.shader_program['model_matrix'].write(self.model_matrix)
        self.shader_program['view_matrix'].write(self.camera.view_matrix)
        self.shader_program['proj_matrix'].write(self.camera.proj_matrix) # pass in the parameter proj_matrix with the value of the camera proj_matrix
        self.shader_program['block_texture'] = 0
        self.texture.use()
        

    def vertice_data(self):
        # change the vertice_data to what we get after all the projections, as this code just uses GPU to display code with shaders
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]   
        # we divide the cube into triangles and render each triangle
        # 0-7 = indices for each cube, create triangles, numbering the vertices counterclockwise
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
      

        texture_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
        # describe each triangle in cube using texture coords
        texture_indices = [(0, 2, 3), (0, 1, 2),
                           (0, 2, 3), (0, 1, 2), 
                           (0, 1, 2), (2, 3, 0),
                           (2, 3, 0), (2, 0, 1),
                           (0, 2, 3), (0, 1, 2),
                           (3, 1, 2), (3, 0, 1)]
        texture_coords_data = []
        for triangle in texture_indices:
            for index in triangle:
                texture_coords_data.append(texture_coords[index])
        texture_coords_data = np.array(texture_coords_data, dtype = 'f4')
        # combine text data and vertice data
        vertice_data = np.hstack([vertice_data, texture_coords_data])
        return vertice_data
    
    def vertex_buffer_object(self):
        vertice_data = self.vertice_data()
        # send vertex data from CPU to GPU using a vertex buffer object (holds all attributes (raw data) of each vertex)
        vbo = self.context.buffer(vertice_data)
        return vbo
    
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
    
    def vertex_array_object(self): # describes how the buffer is read by a shader program (stores the format of the vertex data for the graphics card, how he data is laid out in memory)
        vao = self.context.vertex_array(self.shader_program, [(self.vbo, '3f 2f', 'cube_position' ,'text_coords')]) # in the buffer each vertex is assigned 3 float numbers(x,y,z), these 3 numbers correspond to the input attribute in_position
        return vao
    
    def texture(self):
        texture = pg.image.load('deepslate_bricks.webp').convert()
        texture = pg.transform.flip(texture, False, True)
        texture = self.context.texture(texture.get_size(), 3, pg.image.tobytes(texture, 'RGB'))
        return texture

    def update(self):
        model_matrix = glm.rotate(self.model_matrix, self.main.time, glm.vec3(0, 1, 0))
        self.shader_program['model_matrix'].write(model_matrix)
        
    def render(self):
        self.update()
        self.vao.render()   
    
    def clear(self): # remove all created resources
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()




        
            
        


    



        









