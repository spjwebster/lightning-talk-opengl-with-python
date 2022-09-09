import pygame as pg
from OpenGL import GL
import ctypes


def main():
    create_window(800, 600)

    shader_program_id = setup_shaders()

    vao_id, vertex_count = create_model([
        # Left bottom triangle
        -0.5, 0.5, 0.0,
        -0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,

        # Top right triangle
        0.5, -0.5, 0.0,
        0.5, 0.5, 0.0,
        -0.5, 0.5, 0.0,
    ])

    # Game loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                continue

        # Clear the display buffer
        GL.glClearColor(0.1, 0.1, 0.1, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # Select desired shader program
        GL.glUseProgram(shader_program_id)

        # Rebind the VAO (we might have drawn something else on the last call)
        GL.glBindVertexArray(vao_id)

        # Draw the vertices
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, vertex_count)

        # Unbind the VAO
        GL.glBindVertexArray(0)

        pg.display.flip()


def create_model(data:list[float]):
    # Create the vertex array
    vao_id = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao_id)
    
    # Create VBO that we will store the vertex data in
    vbo_id = GL.glGenBuffers(1)

    # Store vertex data in VBO 
    array_type = (GL.GLfloat * len(data))
    offset = ctypes.c_void_p(0)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_id)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, array_type(*data), GL.GL_STATIC_DRAW)

    # Associate VBO with VAO and Define layout as 3 consecutive float values (x, y, z)
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, offset)
    GL.glEnableVertexAttribArray(0)

    # Unbind VBO (will be rebound any time we bind VAO)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    # Unbind VAO - we may have more models
    GL.glBindVertexArray(0)

    return vao_id, len(data) // 3


def setup_shaders():
    vertex_shader = """
#version 330 core

in vec3 vertex_position;

void main() {
    gl_Position = vec4(vertex_position, 1.0);
}
"""

    fragment_shader = """
#version 330 core

out vec4 colour;

void main() {
    colour = vec4(1.0, 0.5, 0.2, 1.0);
}
"""

    # Compile shaders
    vert_shader_id = GL.glCreateShader(GL.GL_VERTEX_SHADER)
    GL.glShaderSource(vert_shader_id, vertex_shader)
    GL.glCompileShader(vert_shader_id)
    log = GL.glGetShaderInfoLog(vert_shader_id)
    if isinstance(log, bytes):
        print("Error compiling vertex shader: ")
        log = log.decode()
        for line in log.split("\n"):
            print(line)

    frag_shader_id = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
    GL.glShaderSource(frag_shader_id, fragment_shader)
    GL.glCompileShader(frag_shader_id)
    log = GL.glGetShaderInfoLog(frag_shader_id)
    if isinstance(log, bytes):
        print("Error compiling fragment shader: ")
        log = log.decode()
        for line in log.split("\n"):
            print(line)

    # Create shader program, attach vertex and fragment shaders and link
    shader_program_id = GL.glCreateProgram()
    GL.glAttachShader(shader_program_id, vert_shader_id)
    GL.glAttachShader(shader_program_id, frag_shader_id)
    GL.glValidateProgram(shader_program_id)
    GL.glLinkProgram(shader_program_id)
    log = GL.glGetProgramInfoLog(shader_program_id)
    if isinstance(log, bytes):
        print("Error linking shaders in program: ")
        log = log.decode()
        for line in log.split("\n"):
            print(line)

    # Clean up shaders - they're part of the program now
    GL.glDeleteShader(vert_shader_id)
    GL.glDeleteShader(frag_shader_id)

    return shader_program_id


def create_window(width:int, height:int, gl_version=(3, 2)):
    pg.init()

    # By setting these attributes we can choose which Open GL Profile
    # to use, profiles greater than 3.2 use a different rendering path
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, gl_version[0])
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, gl_version[1])
    pg.display.gl_set_attribute(
        pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
    )

    pg.display.gl_set_attribute(pg.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)

    pg.display.set_mode((width, height), pg.DOUBLEBUF | pg.OPENGL)

    GL.glViewport(0, 0, width, height)    

if __name__ == "__main__":
    main()