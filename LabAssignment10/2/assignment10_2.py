import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo

gCamAng = 0.
gCamHeight = 1.


def createVertexAndIndexArrayIndexed():
    varr = np.array([
        (-0.5773502691896258, 0.5773502691896258, 0.5773502691896258),
        (-1, 1, 1),  # v0
        (0.8164965809277261, 0.4082482904638631, 0.4082482904638631),
        (1, 1, 1),  # v1
        (0.4082482904638631, -0.4082482904638631, 0.8164965809277261),
        (1, -1, 1),  # v2
        (-0.4082482904638631, -0.8164965809277261, 0.4082482904638631),
        (-1, -1, 1),  # v3
        (-0.4082482904638631, 0.4082482904638631, -0.8164965809277261),
        (-1, 1, -1),  # v4
        (0.4082482904638631, 0.8164965809277261, -0.4082482904638631),
        (1, 1, -1),  # v5
        (0.5773502691896258, -0.5773502691896258, -0.5773502691896258),
        (1, -1, -1),  # v6
        (-0.8164965809277261, -0.4082482904638631, -0.4082482904638631),
        (-1, -1, -1),  # v7
    ], 'float32')
    iarr = np.array([
        (0, 2, 1),
        (0, 3, 2),
        (4, 5, 6),
        (4, 6, 7),
        (0, 1, 5),
        (0, 5, 4),
        (3, 6, 2),
        (3, 7, 6),
        (1, 2, 6),
        (1, 6, 5),
        (0, 7, 3),
        (0, 4, 7),
    ])
    return varr, iarr


def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6 * varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6 * varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3 * varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)


def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([3., 0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 3., 0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., 0]))
    glVertex3fv(np.array([0., 0., 3.]))
    glEnd()


def exp(rv):
    th = l2norm(rv)
    costh = np.cos(th)
    sinth = np.sin(th)

    rv = normalized(rv)
    ux = rv[0]
    uy = rv[1]
    uz = rv[2]

    R = np.array(
        [[costh + ux * ux * (1 - costh), ux * uy * (1 - costh) - uz * sinth, ux * uz * (1 - costh) + uy * sinth],
         [uy * ux * (1 - costh) + uz * sinth, costh + uy * uy * (1 - costh), uy * uz * (1 - costh) - ux * sinth],
         [uz * ux * (1 - costh) - uy * sinth, uz * uy * (1 - costh) + ux * sinth, costh + uz * uz * (1 - costh)]])
    return R


def log(R):
    w = np.array([0, 0, 0])
    th = 0

    if R[0, 0] + R[1, 1] + R[2, 2] == 3:
        w = np.array([0, 0, 0])
        th = 0
    elif R[0, 0] + R[1, 1] + R[2, 2] == -1:
        th = np.pi
        w = np.array([R[0, 2], R[1, 2], 1 + R[2, 2]]) / np.sqrt(2 * (1 + R[2, 2]))
    else:
        th = np.arccos((R[0, 0] + R[1, 1] + R[2, 2] - 1) / 2)
        w = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]]) / (2 * np.sin(th))

    w = normalized(w)
    return th * w


def slerp(R1, R2, t):
    return R1 @ exp(t * log(R1.T @ R2))


def l2norm(v):
    return np.sqrt(np.dot(v, v))


def normalized(v):
    l = l2norm(v)
    return 1 / l * np.array(v)


def XYZEulerToRotMat(euler):
    xang, yang, zang = euler
    xang = np.radians(xang)
    yang = np.radians(yang)
    zang = np.radians(zang)

    Rx = np.array([[1, 0, 0],
                   [0, np.cos(xang), -np.sin(xang)],
                   [0, np.sin(xang), np.cos(xang)]])
    Ry = np.array([[np.cos(yang), 0, np.sin(yang)],
                   [0, 1, 0],
                   [-np.sin(yang), 0, np.cos(yang)]])
    Rz = np.array([[np.cos(zang), -np.sin(zang), 0],
                   [np.sin(zang), np.cos(zang), 0],
                   [0, 0, 1]])
    return Rx @ Ry @ Rz


def render(t):
    global gCamAng, gCamHeight
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1, 10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5 * np.sin(gCamAng), gCamHeight, 5 * np.cos(gCamAng), 0, 0, 0, 0, 1, 0)

    # draw global frame
    drawFrame()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_RESCALE_NORMAL)

    lightPos = (3., 4., 5., 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    lightColor = (1., 1., 1., 1.)
    ambientLightColor = (.1, .1, .1, 1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    # frame0
    # ZYX Euler angles: rot z by -90 deg then rot y by 90 then rot x by 0
    euler1 = np.array([20, 30, 30])  # in XYZ Euler angles
    euler2 = np.array([15, 30, 25])
    R1 = XYZEulerToRotMat(euler1)  # in rotation matrix
    R2 = XYZEulerToRotMat(euler2)
    color = (1., 0., 0., 1.)
    r1_0 = np.identity(4)
    r1_0 = R1
    r2_0 = np.identity(4)
    r2_0 = R2
    drawKeyframe(r1_0, r2_0, color)

    # frame20
    # ZYX Euler angles: rot z by -90 deg then rot y by 90 then rot x by 0
    euler1 = np.array([45, 60, 40])  # in XYZ Euler angles
    euler2 = np.array([25, 40, 40])
    R1 = XYZEulerToRotMat(euler1)  # in rotation matrix
    R2 = XYZEulerToRotMat(euler2)
    color = (1., 1., 0., 1.)
    r1_20 = np.identity(4)
    r1_20 = R1
    r2_20 = np.identity(4)
    r2_20 = R2
    drawKeyframe(r1_20, r2_20, color)

    # frame40
    # ZYX Euler angles: rot z by -90 deg then rot y by 90 then rot x by 0
    euler1 = np.array([60, 70, 50])  # in XYZ Euler angles
    euler2 = np.array([40, 60, 50])
    R1 = XYZEulerToRotMat(euler1)  # in rotation matrix
    R2 = XYZEulerToRotMat(euler2)
    color = (0., 1., 0., 1.)
    r1_40 = np.identity(4)
    r1_40 = R1
    r2_40 = np.identity(4)
    r2_40 = R2
    drawKeyframe(r1_40, r2_40, color)

    # frame60
    # ZYX Euler angles: rot z by -90 deg then rot y by 90 then rot x by 0
    euler1 = np.array([80, 85, 70])  # in XYZ Euler angles
    euler2 = np.array([55, 80, 65])
    R1 = XYZEulerToRotMat(euler1)  # in rotation matrix
    R2 = XYZEulerToRotMat(euler2)
    color = (0., 0., 1., 1.)
    r1_60 = np.identity(4)
    r1_60 = R1
    r2_60 = np.identity(4)
    r2_60 = R2
    drawKeyframe(r1_60, r2_60, color)

    # inner frame
    objectColor = (1., 1., 1., 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    if 0 <= t <= 20:
        R1 = slerp(r1_0, r1_20, t/20)
        R2 = slerp(r2_0, r2_20, t/20)
    elif 20 < t <= 40:
        R1 = slerp(r1_20, r1_40, (t - 20) / 20)
        R2 = slerp(r2_20, r2_40, (t - 20) / 20)
    elif 40 < t <= 60:
        R1 = slerp(r1_40, r1_60, (t - 40) / 20)
        R2 = slerp(r2_40, r2_60, (t - 40) / 20)

    J1 = np.identity(4)
    J1[:3, :3] = R1
    temp1 = np.identity(4)
    temp1[:3, :3] = R1
    R1 = temp1
    temp2 = np.identity(4)
    temp2[:3, :3] = R2
    R2 = temp2

    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    T1 = np.identity(4)
    T1[0][3] = 1.

    J2 = R1 @ T1 @ R2

    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    glDisable(GL_LIGHTING)


def drawKeyframe(r1, r2, objectColor):

    R1 = np.identity(4)
    R1[:3, :3] = r1
    R2 = np.identity(4)
    R2[:3, :3] = r2

    glPushMatrix()

    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, objectColor)

    J1 = R1

    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    T1 = np.identity(4)
    T1[0][3] = 1.

    J2 = R1 @ T1 @ R2

    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    glPopMatrix()


def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    # rotate the camera when 1 or 3 key is pressed or repeated
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key == glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key == glfw.KEY_2:
            gCamHeight += .1
        elif key == glfw.KEY_W:
            gCamHeight += -.1


gVertexArrayIndexed = None
gIndexArray = None


def main():
    global gVertexArrayIndexed, gIndexArray
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, '2019023436', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    t = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()

        t += 1
        t = t % 61
        render(t)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()

