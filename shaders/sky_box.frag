#version 330 core
out vec4 fragColor;

in vec3 texture_cube_coords;

uniform samplerCube skybox_texture;

void main()
{    
    fragColor = texture(skybox_texture, texture_cube_coords);
}