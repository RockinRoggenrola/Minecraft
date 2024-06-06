#version 330 core
// use openGL's own glsl langauge for shaders
// specifiy that we're using version 3.3

layout (location = 0) in vec3 cube_position; // attribute location number = 0, describes the vertex position (x, y, z)
layout (location = 1) in vec2 text_coords;

out vec2 uv_coords;

uniform mat4 model_matrix; // uniform allows for using proj_matrix as a parameter when calling shader program
uniform mat4 view_matrix;
uniform mat4 proj_matrix; // this is where i put ur making matrices functions

void main() {
    uv_coords = text_coords;
    gl_Position = proj_matrix * view_matrix * model_matrix * vec4(cube_position, 1.0); // initialize the gl_Position (just some vertex shader output variable)
    // as a 4 component vector (x, y, z, w) since vertices are expressed as (x,y,z).
    

}