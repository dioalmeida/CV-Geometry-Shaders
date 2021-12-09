//Dev Team: Diogo Almeida

#version 330
//out vec4 out_color;
//in vec3 vColor;
in vec3 fColor;
out vec4 outColor;
void main() {
    outColor = vec4(fColor, 1.0);
}