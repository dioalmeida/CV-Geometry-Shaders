# Dev Team: Diogo Almeida

import ctypes

import pygame as pg
from OpenGL.GL import glClearColor, glClear, glEnable, glGenBuffers, shaders
from OpenGL.GL.shaders import GL_COMPILE_STATUS, glGetShaderiv, glGetShaderInfoLog, glGetProgramiv, GL_LINK_STATUS, glGetProgramInfoLog, GL_FALSE
from OpenGL.raw.GL.ARB.vertex_shader import GL_FLOAT
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_COLOR_BUFFER_BIT, GL_POINTS
from OpenGL.raw.GL.VERSION.GL_1_1 import glDrawArrays
from OpenGL.raw.GL.VERSION.GL_1_5 import GL_ARRAY_BUFFER, glBindBuffer, glBufferData, GL_STATIC_DRAW
from OpenGL.raw.GL.VERSION.GL_2_0 import GL_VERTEX_PROGRAM_POINT_SIZE, glUseProgram, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glVertexAttribPointer, glEnableVertexAttribArray
from OpenGL.raw.GL.VERSION.GL_3_2 import GL_GEOMETRY_SHADER
from numpy import array
from pygame.locals import DOUBLEBUF, OPENGL, RESIZABLE


class Tutorial:
    def __init__(self, w: int, h: int, geometry: list, min_x: int = -1, min_y: int = -1, max_x: int = 1, max_y: int = 1) -> None:
        self.__window_size = (w, h)
        self.__geometry = geometry

        self.__min_x = min_x
        self.__min_y = min_y
        self.__max_x = max_x
        self.__max_y = max_y

        self.__vao_geometry = None  # Vertex Array Object
        self.__vbo_geometry = None  # Vertex Buffer Object
        self.__shader = None

        self.__init_window()
        self.__init_vbo()
        self.__init_shaders()

    # Class specific and static methods
    def __init_window(self):
        """
        This function initializes a pygame window to serve as OpenGL context.
        """
        pg.init()
        pg.display.set_mode(self.__window_size, DOUBLEBUF | OPENGL | RESIZABLE)
        pg.display.set_caption("Geometry Shaders Tutorial- Visual Computing")
        glClearColor(1.0, 1.0, 1.0, 1.0)  # White background

    @staticmethod
    def __read_and_compile_shader(file: str, shader_type: int) -> int:
        """
        Reads a shader from a file and checks if its compilation is OK.

        :param file: OpenGL file to read.
        :param shader_type: Type of shader to compile.
        """
        # Read the shader from file and compile it
        with open(file) as code_file:
            code = code_file.read()
            shader = shaders.compileShader(code, shader_type)
            result = glGetShaderiv(shader, GL_COMPILE_STATUS)
            if not result:
                raise RuntimeError(glGetShaderInfoLog(shader))
            return shader

    def __init_shaders(self) -> None:  # edit with geometry shader
        """
        This function defines the vertex and fragment shaders and compiles them
        """

        vertex_shader = self.__read_and_compile_shader("shaders/vertex_shader.glsl", GL_VERTEX_SHADER)
        geometry_shader = self.__read_and_compile_shader("shaders/geometry_shader.glsl", GL_GEOMETRY_SHADER)
        fragment_shader = self.__read_and_compile_shader("shaders/fragment_shader.glsl", GL_FRAGMENT_SHADER)

        # Compile program with shaders
        self.__shader = shaders.compileProgram(vertex_shader, geometry_shader, fragment_shader)

        # Check if the shader program is linked OK
        result = glGetProgramiv(self.__shader, GL_LINK_STATUS)
        if not result:
            raise RuntimeError(glGetProgramInfoLog(self.__shader))

    def __init_vbo(self) -> None:
        """
        Defines the geometry and copies it to a vertex buffer object
        """
        geometry_vertices = array([self.__geometry], "f")
        self.__vbo_geometry = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_geometry)
        glBufferData(GL_ARRAY_BUFFER, 4 * geometry_vertices.size, geometry_vertices, GL_STATIC_DRAW)

    def __render(self) -> None:
        """
        This function will deal with rendering objects to the scene.
        """
        glClear(GL_COLOR_BUFFER_BIT)  # Clear buffer
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)  # Enables point size if the primitive is a point

        # Vertex positions
        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_geometry)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, None)
        glEnableVertexAttribArray(0)
        # glDrawArrays(GL_LINE_LOOP, 0, 4)
        glDrawArrays(GL_POINTS, 0, len(self.__geometry))

        # Vertex Colors
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)

        # Number of Vertex
        glVertexAttribPointer(2, 1, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(6 * 4))
        glEnableVertexAttribArray(2)

        # Scale of Vertex
        glVertexAttribPointer(3, 1, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(7 * 4))
        glEnableVertexAttribArray(3)

        # Define shaders to use
        glUseProgram(self.__shader)

        # Update contents of entire display with the updated buffer
        pg.display.flip()

    # Public methods
    def run(self) -> None:
        # enter the loop for rendering and processing events
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            self.__render()
