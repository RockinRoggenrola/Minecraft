import numpy as np
import pygame as pg
import glm
from camera import Camera

class Cube:
    def __init__(self, texture_name, main, pos, visible_faces):
        self.camera = Camera(main)
        self.texture_name = texture_name
        self.main = main
        self.context = main.context
        self.pos = pos
        # openGL rendering pipline: pipline recieves info about the vertices, 
        # vertice shader processes each vertice. Vertices passed to primitive assembly, 
        # where assembly is carried out based on vertex connectivity info (what vertex 
        # connects to what vertex). Rasterization stage: primitive figure is divided into
        # fragments, and for each fragment the fragment shader is used to determine each
        # fragments' color. Then fragments undergo tests that make it a pixel and that pixel
        # is outputted to the FrameBuffer (rendering display)

        self.visible_faces = visible_faces
        self.vertice_data = self.vertice_data()
        self.visible = False

        if len(self.vertice_data) != 0:
            self.visible = True
            self.vbo = self.vertex_buffer_object(self.vertice_data)
            self.shader_program = self.shaders('default')
            self.vao = self.vertex_array_object()
            self.cube_texture = self.texture()
        
            self.model_matrix = self.model_matrix()
            self.shader_program['model_matrix'].write(self.model_matrix)
        
            self.shader_program['block_texture'] = 0
            self.cube_texture.use()

    def vertice_data(self):
        # change the vertice_data to what we get after all the projections, as this code just uses GPU to display code with shaders
        vertices = [(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5),
                    (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5)]   
        # we divide the cube into triangles and render each triangle
        # 0-7 = indices for each cube, create triangles, numbering the vertices counterclockwise
        triangle_indices = [(0, 2, 3), (0, 1, 2), # front
                            (1, 7, 2), (1, 6, 7), # right
                            (6, 5, 4), (4, 7, 6), # back
                            (3, 4, 5), (3, 5, 0), # left
                            (3, 7, 4), (3, 2, 7), # top
                            (0, 6, 1), (0, 5, 6)] # bottom
        
        texture_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
        # describe each triangle in cube using texture coords
        texture_indices = [(0, 2, 3), (0, 1, 2),
                           (0, 2, 3), (0, 1, 2), 
                           (0, 1, 2), (2, 3, 0),
                           (2, 3, 0), (2, 0, 1),
                           (0, 2, 3), (0, 1, 2),
                           (3, 1, 2), (3, 0, 1)]
        
        visible_vertices_indices = []
        visible_texture_indices = []

        for i in range(6):
            key = self.pos + (i,)
            if self.visible_faces.get(key) != None:
                if self.visible_faces[key] == 1:
                    visible_vertices_indices.append(triangle_indices[2*i])
                    visible_vertices_indices.append(triangle_indices[2*i+1])
                    
                    visible_texture_indices.append(texture_indices[2*i])
                    visible_texture_indices.append(texture_indices[2*i+1])

        visible_vertices_data = []
        visible_texture_coords_data = []
        
        for triangle in visible_vertices_indices:
            for index in triangle:
                visible_vertices_data.append(vertices[index])
            
        visible_vertices_data = np.array(visible_vertices_data, dtype = 'f4')

        for triangle in visible_texture_indices:
            for index in triangle:
                visible_texture_coords_data.append(texture_coords[index])
        visible_texture_coords_data = np.array(visible_texture_coords_data, dtype = 'f4')

        # combine text data and vertice data
        visible_vertices_data = np.hstack([visible_vertices_data, visible_texture_coords_data])

        return visible_vertices_data
    
    def vertex_buffer_object(self, data):
        vertice_data = data
        # send vertex data from CPU to GPU using a vertex buffer object (holds all attributes (raw data) of each vertex)
        vbo = self.context.buffer(data)
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
        vao = self.context.vertex_array(self.shader_program, [(self.vbo, '3f 2f', 'vertex_position' ,'text_coords')]) # in the buffer each vertex is assigned 3 float numbers(x,y,z), these 3 numbers correspond to the input attribute in_position
        return vao

    def texture(self):
        texture_path = 'textures/{texture_name}.png'
        texture_path = texture_path.format(texture_name = self.texture_name)
        texture = pg.image.load(texture_path).convert()
        # texture.fill('red')
        texture = pg.transform.flip(texture, False, True)
        texture = self.context.texture(texture.get_size(), 3, pg.image.tobytes(texture, 'RGB'))
        texture.build_mipmaps()
        texture.anisotropy = 16.0
        return texture

    def model_matrix(self):
        model_matrix = glm.mat4(1.0)
        model_matrix = glm.translate(model_matrix, self.pos)
        return model_matrix

    def update(self):
        self.shader_program['model_matrix'].write(self.model_matrix)
        # model_matrix = glm.rotate(self.model_matrix, self.cubes.time, glm.vec3(0, 1, 0))
        
    def render(self):
        self.update()
        self.vao.render()
    
    def clear(self): # remove all created resources
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
        self.cube_texture.release()




        
            
        


    



        









