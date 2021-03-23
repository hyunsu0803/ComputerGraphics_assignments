import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


def render(th):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # draw coordinate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()

    glColor3ub(255, 255, 255)
    # calculate matrix M1, M2 using th
    M1 = np.array([[np.cos(th), -np.sin(th), 0],
                   [np.sin(th), np.cos(th), 0],
                   [0, 0, 1]]) @ np.array([[1, 0, 0.5],
                                           [0, 1, 0],
                                           [0, 0, 1]])
    M2 = np.array([[np.cos(th), -np.sin(th), 0],
                   [np.sin(th), np.cos(th), 0],
                   [0, 0, 1]]) @ np.array([[1, 0, 0],
                                           [0, 1, 0.5],
                                           [0, 0, 1]])

    p1 = np.array([0.5, 0., 1.])
    p2 = np.array([0., 0.5, 1.])
    v1 = np.array([0.5, 0, 0])
    v2 = np.array([0., 0.5, 0])

    # draw point p
    glBegin(GL_POINTS)
    glVertex2fv((M1 @ p1)[:-1])
    glVertex2fv((M2 @ p2)[:-1])
    glEnd()

    # draw vector v
    glBegin(GL_LINES)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv((M1 @ v1)[:-1])
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv((M2 @ v2)[:-1])
    glEnd()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(480, 480, "2019023436", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        t = glfw.get_time()
        th = t
        render(th)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
