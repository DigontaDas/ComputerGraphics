from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

r, g, b = 0.0, 0.0, 0.0
perdrops = 110
raindrops = [{"x": random.uniform(0, 1000), "y": random.uniform(0, 650)} for i in range(perdrops)]
rain_speed = 1
wind = 0 
rain_r, rain_g, rain_b = 0.2, 0.2, 0.8
transition_active = False
transition_start_time = 0
transition_duration = 5.0  # seconds for full transition
transition_target = "day"  # "day" or "night"
start_color = [0, 0, 0]  # Starting r,g,b values
target_color = [1, 1, 1]

def drawing_linear_objects():
    #floor
    glPointSize(5) 
    glLineWidth(15)
    glBegin(GL_TRIANGLES)
    glColor3f(0.6,0.3,0)
    glVertex2f(0,0)
    glVertex2f(1000,500)
    glVertex2f(0,500)
    glEnd()
    glPointSize(5) 
    glLineWidth(15)
    glBegin(GL_TRIANGLES)
    glColor3f(0.6,0.3,0)
    glVertex2f(0,0)
    glVertex2f(1000,0)
    glVertex2f(1000,500)
    glEnd()

    #bush
    glPointSize(5) 
    glLineWidth(15)
    glBegin(GL_LINES)
    glColor3f(0, 0.6, 0)
    glVertex2f(0,350)
    glVertex2f(1000,350)
    glEnd()
    i = 0
    glBegin(GL_TRIANGLES)

    while i < 1000:
       
        glColor3f(0, 1, 0)
        glVertex2f(i, 350)
        glVertex2f(i + 25, 480)
        glVertex2f(i + 50, 350)
        i += 50
    glEnd()
   
    #house
    glPointSize(5) 
    glLineWidth(30)
    glBegin(GL_LINES)
    glColor3f(0.36, 0.25, 0.20)
    glVertex2f(290,295)
    glVertex2f(710,295)
    glEnd()
    glPointSize(5) 
    glLineWidth(15)
    glBegin(GL_TRIANGLES)
    glColor3f(0.90, 0.80, 0.50)
    glVertex2f(300,300)
    glVertex2f(300,450)
    glVertex2f(700,300)
    glEnd()
    glPointSize(5) 
    glLineWidth(15)
    glBegin(GL_TRIANGLES)
    glColor3f(0.90, 0.80, 0.50)
    glVertex2f(700,450)
    glVertex2f(700,300)
    glVertex2f(300,450)
    glEnd()
    #roof
    glPointSize(5) 
    glLineWidth(15)
    glBegin(GL_TRIANGLES)
    glColor3f(0.50, 0.25, 0.15)
    glVertex2f(500,550)
    glVertex2f(280,450)
    glVertex2f(720,450)
    glEnd()

    #door
    glPointSize(5) 
    glLineWidth(15)
    glBegin(GL_TRIANGLES)
    glColor3f(0.65, 0.42, 0.30)
    glVertex2f(470,300)
    glVertex2f(470,400)
    glVertex2f(530,300)
    glEnd()
    glPointSize(5) 
    glLineWidth(15)
    glBegin(GL_TRIANGLES)
    glColor3f(0.65, 0.42, 0.30)
    glVertex2f(530,400)
    glVertex2f(530,300)
    glVertex2f(470,400)
    glEnd()
    #doorknob
    glPointSize(5) 
    glLineWidth(15)
    glBegin(GL_TRIANGLES)
    glColor3f(0,0,0)
    glVertex2f(515,348)
    glVertex2f(515,353)
    glVertex2f(520,348)
    glEnd()
    glPointSize(5) 
    glLineWidth(15)
    glBegin(GL_TRIANGLES)
    glColor3f(0,0,0)
    glVertex2f(520,353)
    glVertex2f(520,348)
    glVertex2f(515,353)
    glEnd()
    #window 1
    glPointSize(5) 
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(0.65, 0.42, 0.30)
    glVertex2f(365,348)
    glVertex2f(423,348)
    glEnd()
    glPointSize(5) 
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(0.65, 0.42, 0.30)
    glVertex2f(368,348)
    glVertex2f(368,403)
    glEnd()
    glPointSize(5) 
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(0.65, 0.42, 0.30)
    glVertex2f(365,403)
    glVertex2f(423,403)
    glEnd()
    glPointSize(5) 
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(0.65, 0.42, 0.30)
    glVertex2f(423,348)
    glVertex2f(423,403)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.3, 0.4, 0.5)
    glVertex2f(370, 350)
    glVertex2f(370, 400)
    glVertex2f(420, 350)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(0.3, 0.4, 0.5)
    glVertex2f(420, 400)
    glVertex2f(420, 350)
    glVertex2f(370, 400)
    glEnd()

    #window 2
    glPointSize(5)
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(0.65, 0.42, 0.30)
    glVertex2f(577, 348)
    glVertex2f(633, 348)
    glEnd()
    glBegin(GL_LINES)
    glColor3f(0.65, 0.42, 0.30)
    glVertex2f(580, 348)
    glVertex2f(580, 403)
    glEnd()
    glBegin(GL_LINES)
    glColor3f(0.65, 0.42, 0.30)
    glVertex2f(577, 403)
    glVertex2f(633, 403)
    glEnd()
    glBegin(GL_LINES)
    glColor3f(0.65, 0.42, 0.30)
    glVertex2f(633, 348)
    glVertex2f(633, 403)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(0.3, 0.4, 0.5)
    glVertex2f(580, 350)
    glVertex2f(580, 400)
    glVertex2f(630, 350)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(0.3, 0.4, 0.5)
    glVertex2f(630, 400)
    glVertex2f(630, 350)
    glVertex2f(580, 400)
    glEnd()
    
def iterate():
    glViewport(0, 0, 1000, 650)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1000, 0.0, 650, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(r, g, b, 1.0)

def showscreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    drawing_linear_objects()
    draw_rain()
    updateTransition()
    glutSwapBuffers()

def updateTransition():
    global r, g, b, rain_r, rain_g, rain_b, transition_active, transition_start_time
    if transition_active:
        current_time = time.time()
        elapsed = current_time - transition_start_time
        progress = min(elapsed / transition_duration, 1.0)
        r = start_color[0] + (target_color[0] - start_color[0]) * progress
        g = start_color[1] + (target_color[1] - start_color[1]) * progress
        b = start_color[2] + (target_color[2] - start_color[2]) * progress
        if transition_target == "day":
            rain_r = 0.2 + (0.4 - 0.2) * progress
            rain_g = 0.2 + (0.4 - 0.2) * progress
            rain_b = 0.8
        else:
            rain_r = 0.4 - (0.4 - 0.2) * progress
            rain_g = 0.4 - (0.4 - 0.2) * progress
            rain_b = 0.8 - (0.8 - 0.7) * progress
        if progress >= 1.0:
            transition_active = False
def keyboardlistener(key, x, y):
    global r, g, b, rain_r, rain_g, rain_b, transition_active, transition_start_time, start_color, target_color, transition_target
    
    if key == b'n':
        if r > 0.0 and not transition_active:
            transition_active = True
            transition_start_time = time.time()
            transition_target = "night"
            start_color = [r, g, b]
            target_color = [0.0, 0.0, 0.0]
            print("Transitioning to Night")
        else:
            print("Already Night")
    if key == b'm':
        if r < 1.0 and not transition_active:
            transition_active = True
            transition_start_time = time.time()
            transition_target = "day"
            start_color = [r, g, b] 
            target_color = [1.0, 1.0, 1.0]  
            print("Transitioning to Morning")
        else:
            print("Already Morning ")
            
    glutPostRedisplay()
    
def specialkeylistener(key, x, y):
    global wind, rain_speed
    if key == GLUT_KEY_LEFT:
        if wind > 0:
            wind = 0
            rain_speed = 1
        else:
            wind -= 0.1  
            rain_speed = 1

    elif key == GLUT_KEY_RIGHT:
        if wind < 0:  
            wind = 0
            rain_speed = 1
        else:
            wind += 0.1  
            rain_speed =  1

    glutPostRedisplay()
    
def draw_rain():
    global raindrops, wind, rain_speed, rain_r, rain_g, rain_b
    glColor3f(rain_r, rain_g, rain_b)
    glLineWidth(2.6)
    glBegin(GL_LINES)
    for i in raindrops:
        i["y"] -= rain_speed  
        i["x"] += wind
        if i["y"] < 0:
            i["y"] = random.uniform(650,-650)
            i["x"] = random.uniform(-1000, 1000)  
        glVertex2f(i["x"], i["y"])
        glVertex2f(i["x"] + wind, i["y"] - 30)
    glEnd()
    glutPostRedisplay()

def animation() :
    draw_rain()
    glutPostRedisplay()
    
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000,650) 
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"22201633_Digonto_Das_Assignment1") 
glutDisplayFunc(showscreen)
glutKeyboardFunc(keyboardlistener)
glutSpecialFunc(specialkeylistener)
glutIdleFunc(animation)
glutMainLoop()