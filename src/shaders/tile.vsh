#version 330

in vec3 inpos;
in vec2 inUV;

out vec2 UV;
flat out int textureLayer;

void main() {
    gl_Position = vec4(inpos.xy, 0.0, 1.0);

    UV = inUV;
    textureLayer = int(inpos.z);
}