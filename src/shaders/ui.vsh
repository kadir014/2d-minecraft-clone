#version 330

in vec2 inpos;
in vec2 inUV;

out vec2 UV;

void main() {
    gl_Position = vec4(inpos, 0.0, 1.0);

    UV = inUV;
}