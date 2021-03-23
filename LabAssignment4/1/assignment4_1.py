import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

mat = []


def render():
    global mat
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # draw coordinates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([1., 0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([0., 1.]))
    glEnd()
    glColor3ub(255, 255, 255)

    # draw triangle
    for i in mat:
        if i == 1:
            glLoadIdentity()
            mat = []
        elif i == 'Q':
            glTranslate(-0.1, 0, 0)
        elif i == 'E':
            glTranslate(0.1, 0, 0)
        elif i == 'A':
            glRotatef(10, 0, 0, 1)
        elif i == 'D':
            glRotatef(-10, 0, 0, 1)
    drawTriangle()


def key_callback(window, key, scancode, action, mods):
    global mat
    # rotate the camera when 1 or 3 key is pressed or repeated
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_1:
            mat.insert(0, 1)
        elif key == glfw.KEY_Q:
            mat.insert(0, 'Q')
        elif key == glfw.KEY_E:
            mat.insert(0, 'E')
        elif key == glfw.KEY_A:
            mat.insert(0, 'A')
        elif key == glfw.KEY_D:
            mat.insert(0, 'D')


def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0., .5]))
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([.5, 0.]))
    glEnd()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(480, 480, "2019023436", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
