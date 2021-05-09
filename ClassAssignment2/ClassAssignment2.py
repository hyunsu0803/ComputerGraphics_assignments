import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *
import ctypes

# for Flat Shading of single mesh mode
singleVarrSeparate = []
singleFn = []
# for Smooth Shading of single mesh mode
singleVarrIndexed = []
singleIarr = []
singleVn = []

# for Flat Shading of single mesh mode
treeVarrSeparate = []
treeFn = []
# for Smooth Shading of single mesh mode
treeVarrIndexed = []
treeIarr = []
treeVn = []

# for Flat Shading
starVarrSeparate = []
starFn = []
# for Smooth Shading
starVarrIndexed = []
starIarr = []
starVn = []

# for Flat Shading
stickVarrSeparate = []
stickFn = []
# for Smooth Shading
stickVarrIndexed = []
stickIarr = []
stickVn = []

at = np.array([0., 0., 0.])
w = np.array([3., 4., 5.])
perspective = True
click = False
left = True

oldx = 0
oldy = 0
A = np.radians(30)
E = np.radians(36)

# modes
animation = False
wireframe = False
smooth = False


def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    if wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if perspective:
        gluPerspective(45, 1, .1, 40)
    else:
        glOrtho(-10, 10, -10, 10, -10, 20)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    cam = at + w
    if np.cos(E) > 0:
        gluLookAt(cam[0], cam[1], cam[2], at[0], at[1], at[2], 0, 1, 0)
    else:
        gluLookAt(cam[0], cam[1], cam[2], at[0], at[1], at[2], 0, -1, 0)

    drawGrid()
    drawFrame()

    glEnable(GL_LIGHTING)  # try to uncomment: no lighting
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)

    glEnable(GL_NORMALIZE)  # try to uncomment: lighting will be incorrect if you scale the object

    # light0 position
    glPushMatrix()
    t = glfw.get_time()
    glRotatef(t * (180 / np.pi), 0, 1, 0)  # try to uncomment: rotate light
    lightPos = (3., 4., 5., 1.)  # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()

    # light0 intensity for each color channel
    lightColor = (0., .5, 1., 1.)
    ambientLightColor = (.0, .05, .01, 1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    # light1 position
    glPushMatrix()
    t = glfw.get_time()
    glRotatef(2 * t * (180 / np.pi), 0, 1, 0)  # try to uncomment: rotate light
    lightPos = (-5., 4., -0., 1.)  # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    glPopMatrix()

    # light1 intensity for each color channel
    lightColor = (0., 1., 0., 1.)
    ambientLightColor = (.0, .1, .0, 1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)

    # light2 position
    glPushMatrix()
    t = glfw.get_time()
    glRotatef(t * (180 / np.pi), 0, 1, 0)  # try to uncomment: rotate light
    lightPos = (-3., 4., -5., 1.)  # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos)
    glPopMatrix()

    # light2 intensity for each color channel
    lightColor = (1., .3, .5, 1.)
    ambientLightColor = (.1, .03, .05, 1.)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT2, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor)

    # material reflectance for each color channel
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    # let's draw
    if not animation:
        glPushMatrix()
        # material reflectance for each color channel
        objectColor = (1., 1., 1., 1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        if smooth:
            drawSmooth(singleVarrIndexed, singleIarr)
        else:
            drawFlat(singleVarrSeparate)
        glPopMatrix()

    elif animation:
        glPushMatrix()
        if smooth:
            animatingModelDrawSmooth()
        else:
            animatingModelDrawFlat()
        glPopMatrix()

    glDisable(GL_LIGHTING)


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
    global perspective, animation, wireframe, smooth
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_V:
            perspective = not perspective
        elif key == glfw.KEY_H:
            animation = True
        elif key == glfw.KEY_Z:
            wireframe = not wireframe
        elif key == glfw.KEY_S:
            smooth = not smooth


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


def openAnimatingModel():
    global starVarrSeparate, starFn
    global starVarrIndexed, starIarr, starVn
    global treeVarrSeparate, treeFn
    global treeVarrIndexed, treeIarr, treeVn
    global stickVarrSeparate, stickFn
    global stickVarrIndexed, stickIarr, stickVn

    starObj = open("./animatingObjects/star.obj", 'r')
    stickObj = open("./animatingObjects/stick.obj", 'r')
    treeObj = open("./animatingObjects/tree.obj", 'r')

    treevarr, treeiarr, treefnarr, OBJinfo = parsing(treeObj)
    treeVarrSeparate, treeFn = buildFlatArray(treevarr, treeiarr, treefnarr)
    treeVarrIndexed, treeIarr, treeVn = buildSmoothArray(treevarr, treeiarr, treefnarr)

    starvarr, stariarr, starfnarr, OBJinfo = parsing(starObj)
    starVarrSeparate, starFn = buildFlatArray(starvarr, stariarr, starfnarr)
    starVarrIndexed, starIarr, starVn = buildSmoothArray(starvarr, stariarr, starfnarr)

    stickvarr, stickiarr, stickfnarr, OBJinfo = parsing(stickObj)
    stickVarrSeparate, stickFn = buildFlatArray(stickvarr, stickiarr, stickfnarr)
    stickVarrIndexed, stickIarr, stickVn = buildSmoothArray(stickvarr, stickiarr, stickfnarr)

    starObj.close()
    stickObj.close()
    treeObj.close()


def animatingModelDrawSmooth():
    t = glfw.get_time()

    # tree animation
    glPushMatrix()
    glRotatef(np.sin(t * 1.5) * 10, 0, 0, 1)

    # tree transformation
    glPushMatrix()
    # material reflectance for each color channel
    objectColor = (.4, 1., .4, 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glScalef(.5, .5, .5)
    glRotatef(-30, 0, 1, 0)
    drawSmooth(treeVarrIndexed, treeIarr)
    glPopMatrix()

    # stick1 animation
    glPushMatrix()
    glTranslatef(0, 4, -1)
    glRotatef(np.sin(t * 1.5) * 30, 1, 0, 0)
    glTranslatef(7, -1, 0)

    # stick1 transformation
    glPushMatrix()
    # material reflectance for each color channel
    objectColor = (.2, .2, 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glScalef(.5, .5, .5)
    drawSmooth(stickVarrIndexed, stickIarr)
    glPopMatrix()

    # star1 animation & transformation
    glPushMatrix()
    # material reflectance for each color channel
    objectColor = (1., 1., .0, 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glTranslatef(0, -2, 0)
    glRotatef(t * (360 / np.pi), 0, 1, 0)
    glRotatef(90, 1, 0, 0)
    glScalef(.1, .1, .1)
    drawSmooth(starVarrIndexed, starIarr)
    glPopMatrix()

    glPopMatrix()

    # stick2 animation
    glPushMatrix()
    glTranslatef(0, 4.5, 0)
    glRotatef(np.sin(t * 1.5) * -30, 1, 0, 0)
    glTranslatef(-5, -1, 0)

    # stick2 transformation
    glPushMatrix()
    # material reflectance for each color channel
    objectColor = (1., .2, .2, 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glScalef(.5, .8, .5)
    drawSmooth(stickVarrIndexed, stickIarr)
    glPopMatrix()

    # star2 animation & transformation
    glPushMatrix()
    # material reflectance for each color channel
    objectColor = (1., 1., .0, 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glTranslatef(0, -2.5, 0)
    glRotatef(t * (-360 / np.pi), 0, 1, 0)
    glRotatef(90, 1, 0, 0)
    glScalef(.1, .1, .1)
    drawSmooth(starVarrIndexed, starIarr)
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()


def animatingModelDrawFlat():
    t = glfw.get_time()

    # tree animation
    glPushMatrix()
    glRotatef(np.sin(t * 1.5) * 10, 0, 0, 1)

    # tree transformation
    glPushMatrix()
    # material reflectance for each color channel
    objectColor = (.4, 1., .4, 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glScalef(.5, .5, .5)
    glRotatef(-30, 0, 1, 0)
    drawFlat(treeVarrSeparate)
    glPopMatrix()

    # stick1 animation
    glPushMatrix()
    glTranslatef(0, 4, -1)
    glRotatef(np.sin(t * 1.5) * 30, 1, 0, 0)
    glTranslatef(7, -1, 0)

    # stick1 transformation
    glPushMatrix()
    # material reflectance for each color channel
    objectColor = (.2, .2, 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glScalef(.5, .5, .5)
    drawFlat(stickVarrSeparate)
    glPopMatrix()

    # star1 animation & transformation
    glPushMatrix()
    # material reflectance for each color channel
    objectColor = (1., 1., .0, 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glTranslatef(0, -2, 0)
    glRotatef(t * (360 / np.pi), 0, 1, 0)
    glRotatef(90, 1, 0, 0)
    glScalef(.1, .1, .1)
    drawFlat(starVarrSeparate)
    glPopMatrix()

    glPopMatrix()

    # stick2 animation
    glPushMatrix()
    glTranslatef(0, 4.5, 0)
    glRotatef(np.sin(t * 1.5) * -30, 1, 0, 0)
    glTranslatef(-5, -1, 0)

    # stick2 transformation
    glPushMatrix()
    # material reflectance for each color channel
    objectColor = (1., .2, .2, 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glScalef(.5, .8, .5)
    drawFlat(stickVarrSeparate)
    glPopMatrix()

    # star2 animation & transformation
    glPushMatrix()
    # material reflectance for each color channel
    objectColor = (1., 1., .0, 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glTranslatef(0, -2.5, 0)
    glRotatef(t * (-360 / np.pi), 0, 1, 0)
    glRotatef(90, 1, 0, 0)
    glScalef(.1, .1, .1)
    drawFlat(starVarrSeparate)
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()


# single mesh file reading
def drop_callback(window, paths):
    global animation
    global singleVarrSeparate, singleFn
    global singleVarrIndexed, singleIarr, singleVn

    singleObj = open(paths[0], 'r')
    animation = False

    varr, iarr, fnarr, OBJinfo = parsing(singleObj)
    singleVarrSeparate, singleFn = buildFlatArray(varr, iarr, fnarr)
    singleVarrIndexed, singleIarr, singleVn = buildSmoothArray(varr, iarr, fnarr)

    print("1. File name : " + (paths[0].split('\\'))[-1].strip(".obj"))
    print("2. Total number of faces : " + str(OBJinfo[0]))
    print("3. Number of faces with 3 vertices : " + str(OBJinfo[1]))
    print("4. Number of faces with 4 vertices : " + str(OBJinfo[2]))
    print("5. Number of faces with more than 4 vertices : " + str(OBJinfo[3]))
    print()
    singleObj.close()


def parsing(obj):
    varr = []
    iarr = []
    fnarr = []
    fns = []
    OBJinfo = [0, 0, 0, 0]

    for l in obj:
        if l == '\n':
            continue
        line = l.split()

        if line[0] == 'v':
            line[1:] = list(map(float, line[1:]))
            varr.append(np.array(line[1:]))

        elif line[0] == 'vn':
            line[1:] = list(map(float, line[1:]))
            fns.append(np.array(line[1:]))

        elif line[0] == 'f':
            OBJinfo[0] += 1
            if len(line) == 4:
                OBJinfo[1] += 1
            elif len(line) == 5:
                OBJinfo[2] += 1
            elif len(line) > 5:
                OBJinfo[3] += 1

            indexedPolygon = []
            fn = []

            # split index and face normal
            for v in line[1:]:
                vertex = v.split('/')
                indexedPolygon.append(vertex[0])
                fn = fns[int(vertex[-1]) - 1]  # real

            # make integer iarr element
            indexedPolygon = list(map(int, indexedPolygon))
            for i in range(len(indexedPolygon)):
                indexedPolygon[i] = indexedPolygon[i] - 1

            # store indexed triangle set and their face normal index
            for i in range(1, len(indexedPolygon) - 1):
                triangle = [indexedPolygon[0], indexedPolygon[i], indexedPolygon[i + 1]]
                iarr.append(np.array(triangle))
                fnarr.append(np.array(fn))

    return varr, iarr, fnarr, OBJinfo


def buildFlatArray(varr, iarr, fnarr):
    varrSeperate = []
    faceNormal = fnarr

    for i in range(len(fnarr)):
        varrSeperate.append(fnarr[i])
        varrSeperate.append(varr[iarr[i][0]])
        varrSeperate.append(fnarr[i])
        varrSeperate.append(varr[iarr[i][1]])
        varrSeperate.append(fnarr[i])
        varrSeperate.append(varr[iarr[i][2]])

    return varrSeperate, faceNormal


def buildSmoothArray(varr, iarr, fnarr):
    varrIndexed = []
    Iarr = iarr
    vertexNormal = []

    # calculate average face normal of each vertex
    for v in range(len(varr)):
        avgVertexNormal = np.array([0., 0., 0.])

        # get sum of face normals which share the vertex
        for i in range(len(iarr)):
            if v in iarr[i]:
                avgVertexNormal += fnarr[i]

        # normalize and push
        avgVertexNormal = avgVertexNormal / np.sqrt(np.dot(avgVertexNormal, avgVertexNormal))
        vertexNormal.append(avgVertexNormal)

        # make vertex array indexed
        varrIndexed.append(avgVertexNormal)
        varrIndexed.append(varr[v])

    return varrIndexed, Iarr, vertexNormal


def drawSmooth(varrIndexed, Iarr):
    varr = np.array(varrIndexed, dtype='float32')
    iarr = np.array(Iarr, dtype='int64')
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glVertexPointer(3, GL_FLOAT, 6 * varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3 * varr.itemsize))
    glNormalPointer(GL_FLOAT, 6 * varr.itemsize, varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)


def drawFlat(varrSeparate):
    varr = np.array(varrSeparate, dtype='float32')
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6 * varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6 * varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3 * varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size / 6))


def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([-30., 0., 0.]))
    glVertex3fv(np.array([30., 0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 3., 0.]))
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
    if not glfw.init():
        return
    window = glfw.create_window(900, 900, 'myBlender', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    openAnimatingModel()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
