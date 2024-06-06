#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_coords;

uniform sampler2D block_texture;
void main() {
    vec3 color = texture(block_texture, uv_coords).rgb;
    fragColor = vec4(color, 1.0);
    

}