#version 330

in vec2 UV;

uniform sampler2D Texture;

void main() {
    vec4 texc = texture(Texture, UV).rgba;

    gl_FragColor = texc;
}