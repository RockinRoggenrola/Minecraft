import numpy
import math
from setup import *

class Camera:
    def __init__(self, pos, dir, near, far, fov):
        self.pos = numpy.array(pos)
        n = math.sqrt(sum(dir*dir))
        self.direction = numpy.array(dir/n)
        self.near = near
        self.far = far
        self.dir = dir / math.sqrt(sum(dir**2))
        self.fov = fov * math.pi / 180

    def move_up(self):
        self.pos[1] += 0.1
    
    def move_down(self):
        self.pos[1] -= 0.1
    
    def move_right(self):
        self.pos[0] += 0.1
    
    def move_left(self):
        self.pos[0] -= 0.1

    def project_to_near(self, point):
        lambda_ = self.near*sum(self.dir*self.dir) / (sum((point-self.pos)*self.dir))
        return lambda_ * numpy.array(point) + (1-lambda_) * self.pos
    
    def return_tilt_x(self, angle):
        x, y, z = self.dir
        h = math.sqrt(x*x + y*y + z*z)
        j = math.sqrt(y*y + z*z)
        self_angle = math.acos(j/h)
        a = h * math.cos(angle+self_angle) / j
        b = h * math.sin(angle+self_angle) / x
        n = math.sqrt(2*a*a + b*b)
        return numpy.array(x*b/n, y*a/n, z*a/n)
    
    def return_tilt_y(self, angle):
        x, y, z = self.dir
        h = math.sqrt(x*x + y*y + z*z)
        j = math.sqrt(x*x + z*z)
        self_angle = math.acos(j/h)
        a = h * math.cos(angle+self_angle) / j
        b = h * math.sin(angle+self_angle) / y
        n = math.sqrt(2*a*a + b*b)
        return numpy.array(x*a/n, y*b/n, z*a/n)

    def return_tilt_z(self, angle):
        x, y, z = self.dir
        h = math.sqrt(x*x + y*y + z*z)
        j = math.sqrt(x*x + y*y)
        self_angle = math.acos(j/h)
        a = h * math.cos(angle+self_angle) / j
        b = h * math.sin(angle+self_angle) / z
        n = math.sqrt(2*a*a + b*b)
        return numpy.array((x*a/n, y*a/n, z*b/n))
    
    def tilt_x(self, angle):
        self.dir = self.return_tilt_x(angle)

    def tilt_y(self, angle):
        self.dir = self.return_tilt_y(angle)

    def tilt_z(self, angle):
        self.dir = self.return_tilt_z(angle)

    def near_plane(self): # order: T, R, B, L (clockwise)
        tilt_z1 = self.return_tilt_z(self.fov/2)
        tilt_z2 = self.return_tilt_z(-1*self.fov/2)
        center_to_right = (self.near/math.cos(self.fov/2))*tilt_z1
        center_to_left = -1*center_to_right
        center_to_top = numpy.cross(self.dir, center_to_right) * height / width
        center_to_bottom = -1*center_to_top

        # these are vectors from the center of the near plane to each of the edges
        new_dirs = [center_to_top, center_to_right, center_to_bottom, center_to_left]
        return new_dirs

    def make_projection_matrix(self):
        near_plane = self.near_plane()
        return numpy.linalg.inv(numpy.array([near_plane[1].tolist(), near_plane[0].tolist(), self.dir.tolist()]))

    def project_to_2d(self, point, projection_matrix):
        near_plane_projection = self.project_to_near(point) - self.pos - self.near * self.dir
        return projection_matrix @ near_plane_projection
    
    def convert_to_pygame(self, coords):
        return (width/2 + coords[0]*width/2, height/2 + coords[1]*height/2)

    def render_cube(self, cube):
        projected_coords = []
        for vertex in cube.vertices():
            projection_matrix = self.make_projection_matrix()
            twoD_coords = self.project_to_2d(vertex, projection_matrix)
            pygame_coords = self.convert_to_pygame(twoD_coords)
            projected_coords.append(pygame_coords)
            pygame.draw.circle(screen, cube.color, pygame_coords, 3)
        for edge in cube.edges():
            pygame.draw.line(screen, cube.color, projected_coords[edge[0]], projected_coords[edge[1]], 1)

        