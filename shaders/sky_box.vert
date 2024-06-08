#version 330 core
layout (location = 0) in vec3 vertex_position;

out vec3 texture_cube_coords;
uniform mat4 proj_matrix;
uniform mat4 view_matrix;

void main()
{
    texture_cube_coords = vertex_position;
    vec4 pos = proj_matrix * view_matrix * vec4(vertex_position, 1.0);
    gl_Position = pos.xyww;
}  