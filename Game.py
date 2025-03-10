from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random



points = [((250, 250), (1, 1), (0.5, 0.5, 0.5))] #position,velocity,color
speed = 0.1 #movement speed
invisible_time = False  
blinking = True  
freeze = False  


def draw_point(x, y):
    glPointSize(5)  
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def iterate():
    glViewport(0, 0, 1000, 1000)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 1000, 0, 1000, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    for i in points:
        x, y = i[0]
        a,b,c = i[2]


        if invisible_time and blinking:
            glColor3f(0, 0, 0)  
        else:
            glColor3f(a, b, c) 
            draw_point(x, y)
    glutSwapBuffers()


def updated_points():
    if freeze:
        return
    global blinking, invisible_time
    for i in range(len(points)):
        (x, y), (dx, dy), color = points[i]
        x += dx * speed
        y += dy * speed
        if x <= 0 or x >= 1000:
            dx *= -1
        if y <= 0 or y >= 1000:
            dy *= -1
        points[i] = ((x, y), (dx, dy), color)
    glutPostRedisplay()  

def mouse(button, state, x, y):
    if freeze:
        return
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        new_x, new_y = convert_coordinates(x, y)
        new_dx = random.choice([-1, 1])
        new_dy = random.choice([-1, 1])
        new_color = (random.random(), random.random(), random.random())
        points.append(((new_x, new_y), (new_dx, new_dy), new_color))

def special_keyboard_keys(key, x, y):
    if freeze:
        return
    global speed, invisible_time, blinking
    if key == GLUT_KEY_UP:
        speed *= 1.5
    elif key == GLUT_KEY_DOWN:
        speed /= 1.5
    elif key == GLUT_KEY_LEFT:
        invisible_time = not invisible_time
        if invisible_time:
            blinking = True
            glutTimerFunc(1000, blink, 0)

def keyboard_keys(key,x,y):
    global freeze
    if key == b' ':
        freeze = not freeze


def blink(value):
    global blinking
    if not freeze:
        blinking = not blinking
    if invisible_time:
        glutTimerFunc(1000, blink, 0)


def convert_coordinates(x, y):
    return x, 1000 - y


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Game")
glutDisplayFunc(display)
glutIdleFunc(updated_points)
glutMouseFunc(mouse)
glutSpecialFunc(special_keyboard_keys)
glutKeyboardFunc(keyboard_keys)
glutMainLoop()