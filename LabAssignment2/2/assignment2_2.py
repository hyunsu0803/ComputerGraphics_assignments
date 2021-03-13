import numpy as np
import glfw
from OpenGL.GL import *

pressedKey = 3


def render():
    global pressedKey
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    angle = np.linspace(0, 360, 13)
    angle = angle * np.pi / 180
    y = np.sin(angle[:13])
    x = np.cos(angle[:13])

    glBegin(GL_LINE_LOOP)
    for i in range(13):
        glVertex2f(x[i], y[i])
    glEnd()

    glBegin(GL_LINES)
    glVertex2f(0, 0)
    glVertex2f(x[pressedKey], y[pressedKey])
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global pressedKey

    if key == glfw.KEY_1:
        if action == glfw.PRESS:
            pressedKey = 2

    elif key == glfw.KEY_2:
        if action == glfw.PRESS:
            pressedKey = 1

    elif key == glfw.KEY_3:
        if action == glfw.PRESS:
            pressedKey = 0

    elif key == glfw.KEY_4:
        if action == glfw.PRESS:
            pressedKey = 11

    elif key == glfw.KEY_5:
        if action == glfw.PRESS:
            pressedKey = 10

    elif key == glfw.KEY_6:
        if action == glfw.PRESS:
            pressedKey = 9

    elif key == glfw.KEY_7:
        if action == glfw.PRESS:
            pressedKey = 8

    elif key == glfw.KEY_8:
        if action == glfw.PRESS:
            pressedKey = 7

    elif key == glfw.KEY_9:
        if action == glfw.PRESS:
            pressedKey = 6

    elif key == glfw.KEY_0:
        if action == glfw.PRESS:
            pressedKey = 5

    elif key == glfw.KEY_Q:
        if action == glfw.PRESS:
            pressedKey = 4

    elif key == glfw.KEY_W:
        if action == glfw.PRESS:
            pressedKey = 3

    else:
        pressedKey = 3


def main():
    global pressedKey
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480, 480, "2019023436", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)

    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        render()

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()


# global pressedKey
if __name__ == "__main__":
    pressedKey = 3
    main()
