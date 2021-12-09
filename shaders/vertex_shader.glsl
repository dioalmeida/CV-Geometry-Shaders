//Dev Team: Diogo Almeida

#version 330
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 color;
layout (location = 2) in float  sides;
layout (location = 3) in float  scale;
out vec3 vColor;
out float vSides;
out float vScale;

void main() {
    gl_Position =  vec4(position, 1.0);// Vertex position
    vColor = vec3(color);// Vertex color
    vSides = sides;//Number of vertex
    vScale = scale;//Drawing scale
    gl_PointSize = 5;// In case the shape is a point sets point size in px
}