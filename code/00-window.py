import pygame as pg
from OpenGL import GL


def main():
    create_window(800, 600)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                continue


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