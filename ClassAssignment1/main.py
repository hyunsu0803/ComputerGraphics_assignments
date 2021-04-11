import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *

gVertexArrayIndexed = None
gIndexArray = None

at = np.array([0., 0., 0.])
w = np.array([3., 4., 5.])
perspective = True
click = False
left = True

oldx = 0
oldy = 0
A = np.radians(30)
E = np.radians(36)



def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glLoadIdentity()
    if perspective:
        gluPerspective(45, 1, .1, 40)
    else:
        glOrtho(-10, 10, -10, 10, -10, 20)

    cam = at + w

    if np.cos(E) > 0:
        gluLookAt(cam[0], cam[1], cam[2], at[0], at[1], at[2], 0, 1, 0)
    else:
        gluLookAt(cam[0], cam[1], cam[2], at[0], at[1], at[2], 0, -1, 0)

    drawGrid()
    drawFrame()
    glColor3ub(255, 255, 255)

    drawCube_glDrawElements()


def createVertexAndIndexArrayIndexed():
    varr = np.array([
        (0, 0, 0),  # v0
        (1.5, 0, 0),  # v1
        (0, 1.5, 0),  # v2
        (0, 0, 1.5),  # v3
        (1.5, 0, 1.5),  # v4
        (1.5, 1.5, 0),  # v5
        (1.5, 1.5, 1.5),  # v6
        (0, 1.5, 1.5),  # v7
    ], 'float32')
    iarr = np.array([
        (0, 1, 4, 3),
        (7, 3, 4, 6),
        (6, 4, 1, 5),
        (2, 5, 1, 0),
        (7, 2, 0, 3),
        (6, 5, 2, 7)
    ])
    return varr, iarr


def button_callback(window, button, action, mod):
    global click, left
    global oldx, oldy

    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            oldx, oldy = glfw.get_cursor_pos(window)
            click = True
            left = True

        elif action == glfw.RELEASE:
            click = False

    elif button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            oldx, oldy = glfw.get_cursor_pos(window)
            click = True
            left = False

        elif action == glfw.RELEASE:
            click = False


def cursor_callback(window, xpos, ypos):
    global oldx, oldy

    if click:
        newx = xpos
        newy = ypos

        dx = newx - oldx
        dy = newy - oldy

        if left:
            orbit(dx, dy)
        else:
            panning(dx, dy)

        oldx = newx
        oldy = newy


def key_callback(window, key, scancode, action, mods):
    global perspective
    if key == glfw.KEY_V and action == glfw.PRESS:
        if perspective:
            perspective = False
        else:
            perspective = True


# orbit
def orbit(dx, dy):
    global w, A, E

    A -= np.radians(dx) / 5
    E += np.radians(dy) / 5

    distance = np.sqrt(w[0] ** 2 + w[1] ** 2 + w[2] ** 2)
    w = distance * np.array([np.cos(E) * np.sin(A), np.sin(E), np.cos(E) * np.cos(A)])


def panning(dx, dy):
    global at

    up = np.array([0, 1, 0])
    w_ = w / np.sqrt(w[0] ** 2 + w[1] ** 2 + w[2] ** 2)
    u = np.cross(up, w_)
    u = u / np.sqrt(u[0] ** 2 + u[1] ** 2 + u[2] ** 2)
    v = np.cross(w_, u)

    at += (-1 * dx * u + dy * v) / 30


# zoom
def scroll_callback(window, xoffset, yoffset):
    zoom(yoffset)


def zoom(yoffset):
    global w
    w -= w * yoffset / 5


def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 3 * varr.itemsize, varr)
    glDrawElements(GL_QUADS, iarr.size, GL_UNSIGNED_INT, iarr)


def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([-30., 0., 0.]))
    glVertex3fv(np.array([30., 0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 1., 0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., -30]))
    glVertex3fv(np.array([0., 0., 30.]))
    glEnd()


def drawGrid():
    glBegin(GL_LINES)
    glColor3ub(60, 60, 60)
    for i in np.linspace(-20, 20, 50):
        glVertex3fv(np.array([-20, 0, i]))
        glVertex3fv(np.array([20, 0, i]))
        glVertex3fv(np.array([i, 0, -20]))
        glVertex3fv(np.array([i, 0, 20]))
    glEnd()


def main():
    global gVertexArrayIndexed, gIndexArray
    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    if not glfw.init():
        return
    window = glfw.create_window(1000, 1000, 'myBlender', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
