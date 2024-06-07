import glm
import pygame as pg

class Camera:
    def __init__(self, main):
        self.main = main
        self.FOV = 45
        self.ASPECT_RATIO = main.WIND_SIZE[0] / main.WIND_SIZE[1]
        self.NEAR_PLANE = 0.1
        self.FAR_PLANE = 100
        self.SENSITIVITY = 0.5
        self.pos = glm.vec3(2, 2, 3)
        
        # vectors for camera movements
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0 ,-1) # positive z axis is towards you
        self.movement_speed = 20

        self.yaw = 0
        self.pitch = 0

        self.view_matrix = glm.lookAt(self.pos, glm.vec3(0, 0, 0), self.up)
        self.proj_matrix = glm.perspective(glm.radians(self.FOV), self.ASPECT_RATIO, self.NEAR_PLANE, self.FAR_PLANE)
    
    def move(self):
        camera_speed = self.movement_speed * self.main.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.pos += self.forward * camera_speed
        if keys[pg.K_a]:
            self.pos -= self.right * camera_speed
        if keys[pg.K_s]:
            self.pos -= self.forward * camera_speed
        if keys[pg.K_d]:
            self.pos += self.right * camera_speed
        if keys[pg.K_SPACE]:
            self.pos += self.up * camera_speed
        if keys[pg.K_LSHIFT]:
            self.pos -= self.up * camera_speed
        self.view_matrix = glm.lookAt(self.pos, self.pos + self.forward, self.up)
    
    def rotate(self):
        delta_x, delta_y = pg.mouse.get_rel()
        self.yaw += delta_x * self.SENSITIVITY
        self.pitch -= delta_y * self.SENSITIVITY
        if self.pitch > 89:
            self.pitch = 89
        if self.pitch < -89:
            self.pitch = -89

    def update(self):
        self.move()
        self.rotate()

        yaw = glm.radians(self.yaw)
        pitch = glm.radians(self.pitch)
        direction = glm.vec3(0,0,0)
        direction.x = glm.cos(yaw) * glm.cos(pitch)
        direction.y = glm.sin(pitch)
        direction.z = glm.sin(yaw) * glm.cos(pitch)
        self.forward = glm.normalize(direction) 
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))


        self.view_matrix = glm.lookAt(self.pos, self.pos + self.forward, self.up)







        
    # def move_up(self):
    #     self.pos[1] += 0.1
    
    # def move_down(self):
    #     self.pos[1] -= 0.1
    
    # def move_right(self):
    #     self.pos[0] += 0.1
    
    # def move_left(self):
    #     self.pos[0] -= 0.1

    # def project_to_near(self, point):
    #     lambda_ = self.near*sum(self.dir*self.dir) / (sum((point-self.pos)*self.dir))
    #     return lambda_ * numpy.array(point) + (1-lambda_) * self.pos
    
    # def return_tilt_x(self, angle):
    #     x, y, z = self.dir
    #     h = math.sqrt(x*x + y*y + z*z)
    #     j = math.sqrt(y*y + z*z)
    #     self_angle = math.acos(j/h)
    #     a = h * math.cos(angle+self_angle) / j
    #     b = h * math.sin(angle+self_angle) / x
    #     n = math.sqrt(2*a*a + b*b)
    #     return numpy.array(x*b/n, y*a/n, z*a/n)
    
    # def return_tilt_y(self, angle):
    #     x, y, z = self.dir
    #     h = math.sqrt(x*x + y*y + z*z)
    #     j = math.sqrt(x*x + z*z)
    #     self_angle = math.acos(j/h)
    #     a = h * math.cos(angle+self_angle) / j
    #     b = h * math.sin(angle+self_angle) / y
    #     n = math.sqrt(2*a*a + b*b)
    #     return numpy.array(x*a/n, y*b/n, z*a/n)

    # def return_tilt_z(self, angle):
    #     x, y, z = self.dir
    #     h = math.sqrt(x*x + y*y + z*z)
    #     j = math.sqrt(x*x + y*y)
    #     self_angle = math.acos(j/h)
    #     a = h * math.cos(angle+self_angle) / j
    #     b = h * math.sin(angle+self_angle) / z
    #     n = math.sqrt(2*a*a + b*b)
    #     return numpy.array((x*a/n, y*a/n, z*b/n))
    
    # def tilt_x(self, angle):
    #     self.dir = self.return_tilt_x(angle)

    # def tilt_y(self, angle):
    #     self.dir = self.return_tilt_y(angle)

    # def tilt_z(self, angle):
    #     self.dir = self.return_tilt_z(angle)

    # def near_plane(self): # order: T, R, B, L (clockwise)
    #     tilt_z1 = self.return_tilt_z(self.fov/2)
    #     tilt_z2 = self.return_tilt_z(-1*self.fov/2)
    #     center_to_right = (self.near/math.cos(self.fov/2))*tilt_z1
    #     center_to_left = -1*center_to_right
    #     center_to_top = numpy.cross(self.dir, center_to_right) * height / width
    #     center_to_bottom = -1*center_to_top

    #     # these are vectors from the center of the near plane to each of the edges
    #     new_dirs = [center_to_top, center_to_right, center_to_bottom, center_to_left]
    #     return new_dirs

    # def make_projection_matrix(self):
    #     near_plane = self.near_plane()
    #     return numpy.linalg.inv(numpy.array([near_plane[1].tolist(), near_plane[0].tolist(), self.dir.tolist()]))

    # def project_to_2d(self, point, projection_matrix):
    #     near_plane_projection = self.project_to_near(point) - self.pos - self.near * self.dir
    #     return projection_matrix @ near_plane_projection
    
    # def convert_to_pygame(self, coords):
    #     return (width/2 + coords[0]*width/2, height/2 + coords[1]*height/2)

    # def render_cube(self, cube):
    #     projected_coords = []
    #     for vertex in cube.vertices():
    #         projection_matrix = self.make_projection_matrix()
    #         twoD_coords = self.project_to_2d(vertex, projection_matrix)
    #         pygame_coords = self.convert_to_pygame(twoD_coords)
    #         projected_coords.append(pygame_coords)
    #         pygame.draw.circle(screen, cube.color, pygame_coords, 3)
    #     for edge in cube.edges():
    #         pygame.draw.line(screen, cube.color, projected_coords[edge[0]], projected_coords[edge[1]], 1)

        