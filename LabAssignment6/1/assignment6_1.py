import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *


def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)

    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)

    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)

    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glEnd()


def drawCubeArray():
    for i in range(5):
        for j in range(5):
            for k in range(5):
                glPushMatrix()
                glTranslatef(i, j, -k - 1)
                glScalef(.5, .5, .5)
                drawUnitCube()
                glPopMatrix()


def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([1., 0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 1., 0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., 0]))
    glVertex3fv(np.array([0., 0., 1.]))
    glEnd()


def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glLoadIdentity()

    myFrustum(-1, 1, -1, 1, 1, 10)
    myLookAt(np.array([5, 3, 5]), np.array([1, 1, -1]), np.array([0, 1, 0]))

    drawFrame()
    glColor3ub(255, 255, 255)

    drawCubeArray()


def myFrustum(left, right, bottom, top, near, far):
    i00 = 2 * near / (right - left)
    i02 = (right + left) / (right - left)
    i11 = 2 * near / (top - bottom)
    i12 = (top + bottom) / (top / bottom)
    i22 = -1 * (far + near) / (far - near)
    i23 = -2 * far * near / (far - near)

    Mpers = np.array([[i00, 0, i02, 0],
                      [0, i11, i12, 0],
                      [0, 0, i22, i23],
                      [0, 0, -1, 0]])

    glMultMatrixf(Mpers.T)


def myLookAt(eye, at, up):
    tmpW = eye - at
    w = tmpW / np.sqrt(np.dot(tmpW, tmpW))
    tmpU = np.cross(up, w)
    u = tmpU / np.sqrt(np.dot(tmpU, tmpU))
    v = np.cross(w, u)

    Mv = np.identity(4)
    Mv[0, :3] = u
    Mv[1, :3] = v
    Mv[2, :3] = w
    Mv[:3, 3] = np.array([np.dot(-1*u, eye), np.dot(-1*v, eye), np.dot(-1*w, eye)])

    glMultMatrixf(Mv.T)


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, 'Lecture10', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()