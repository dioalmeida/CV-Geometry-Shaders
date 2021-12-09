//Dev Team: Diogo Almeida

#version 150 core

in float vSides[]; //Number of vertex for each geometry
in vec3 vColor[];// Output from vertex shader for each vertex
out vec3 fColor;// Output to fragment shader
const float PI = 3.1415926;
in float vScale[];
float a =0;

layout(points) in;// Describes what kind of primitives our shader will process.
//options for layout in:
//    points - GL_POINTS (1 vertex)
//    lines - GL_LINES, GL_LINE_STRIP, GL_LINE_LIST (2 vertices)
//    lines_adjacency - GL_LINES_ADJACENCY, GL_LINE_STRIP_ADJACENCY (4 vertices)
//    triangles - GL_TRIANGLES, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN (3 vertices)
//    triangles_adjacency - GL_TRIANGLES_ADJACENCY, GL_TRIANGLE_STRIP_ADJACENCY (6 vertices)
layout(line_strip, max_vertices = 146) out;// Determines what kind of geometry our shader will output.
//options for layout out:
//    points
//    line_strip
//    triangle_strip



void main()
{
    fColor = vColor[0];// Point has only one vertex
    for (int i = 0; i <=12; i++) {
        a+=0.01;
        for (int i = 0; i <=vSides[0]; i++) {
            // Angle between each side in radians
            float ang = PI * 2.0 / vSides[0]* i;

            // Offset from center of point (0.45 to accomodate for aspect ratio)
            //cos - horz | sin - vert
            vec4 offset = vec4((cos(ang) * 0.45)*vScale[0]+a, (-sin(ang) * 0.8)*vScale[0]+a, 1.5, 1.5);
            gl_Position = gl_in[0].gl_Position + offset;

            EmitVertex();
        }
    }

    EndPrimitive();//Generates the primitive
}