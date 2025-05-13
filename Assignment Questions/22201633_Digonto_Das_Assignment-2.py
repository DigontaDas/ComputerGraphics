from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

#8 way
def midpoint_line(x1, y1, x2, y2):
    zone = Zone(x1, y1, x2, y2)
    
    # Convert to zone 0
    x1_0, y1_0 = convert_to_zone_0(x1, y1, zone)
    x2_0, y2_0 = convert_to_zone_0(x2, y2, zone)
    
    # Get all points in zone 0
    points_zone0 = midpoint_line_drawing(x1_0, y1_0, x2_0, y2_0)
    
    # Convert back to original zone and return
    original_points = []
    for x, y in points_zone0:
        original_points.append(convert_from_zone_0(x, y, zone))
    
    return original_points
def Zone(x1,y1,x2,y2):
    dx=x2-x1
    dy=y2-y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0: 
            return 0
        if dx < 0 and dy >= 0: 
            return 3
        if dx < 0 and dy < 0: 
            return 4
        if dx >= 0 and dy < 0: 
            return 7
    else:
        if dx >= 0 and dy >= 0: 
            return 1
        if dx < 0 and dy >= 0: 
            return 2
        if dx < 0 and dy < 0: 
            return 5
        if dx >= 0 and dy < 0: 
            return 6
def convert_to_zone_0(x,y,zone):
    if zone==0:
        return x,y
    else:
        if zone==1:
            return y,x
        elif zone==2:
            return y,-x
        elif zone==3:
            return -x,y
        elif zone==4:
            return -x,-y
        elif zone==5:
            return -y,-x
        elif zone==6:
            return -y,x
        elif zone==7:
            return x,-y
def convert_from_zone_0(x,y,zone):
    if zone==0:
        return x,y
    else:
        if zone==1:
            return y,x
        elif zone==2:
            return -y,x
        elif zone==3:
            return -x,y
        elif zone==4:
            return -x,-y
        elif zone==5:
            return -y,-x
        elif zone==6:
            return y,-x
        elif zone==7:
            return x,-y       
def midpoint_line_drawing(x1,y1,x2,y2):
    dx=x2-x1
    dy=y2-y1
    d_int=(2*dy)-dx
    NE=(2*dy)-(2*dx)
    E=(2*dy)
    x=x1
    y=y1
    points=[]
    points.append((x,y))
    while x<x2:
        if d_int>0:
            d_int+=NE
            y+=1
            x+=1
        else:
            d_int+=E
            x+=1
        points.append((x,y))

    return points

#calculations
def draw_pixel(x, y, color):
    glBegin(GL_POINTS)
    glColor3f(color[0], color[1], color[2])
    glVertex2i(int(x), int(y))
    glEnd()

def draw_line(x1, y1, x2, y2, color):
    points = midpoint_line(x1, y1, x2, y2)
    for x, y in points:
        draw_pixel(x, y, color)
        
def check_collision():
    global diamond_x,diamond_y,diamond_size,catcher_x,catcher_width,catcher_height
    return (diamond_x - diamond_size < catcher_x + catcher_width//2 and
            diamond_x + diamond_size > catcher_x - catcher_width//2 and
            diamond_y - diamond_size < 30 + catcher_height and
            diamond_y + diamond_size > 30)

#Items
def restart_button():
    x, y, size, color=40,window_height-40,30, (0,1,1)
    draw_line(x-size, y, x, y-size, color)
    draw_line(x-size, y, x, y+size, color)
    draw_line(x-size, y, x+size, y, color)
def play_button():
    x, y, size, color=window_width//2,window_height-40,30, (1,.5,0)
    draw_line(x-size/2, y-size, x-size/2, y+size, color)
    draw_line(x-size/2, y-size, x+size/2, y, color)
    draw_line(x-size/2, y+size, x+size/2, y, color)
def pause_button():
    x, y, size, color=window_width//2,window_height-40,30, (1,.5,0)
    draw_line(x-size/3, y-size, x-size/3, y+size, color)
    draw_line(x+size/3, y-size, x+size/3, y+size, color)
def exit_button():
    x, y, size, color=window_width-40,window_height-40,30, (1,0,0)
    draw_line(x-size, y-size, x+size, y+size, color)
    draw_line(x-size, y+size, x+size, y-size, color)

def diamond():
    x, y, size, color = diamond_x, diamond_y, diamond_size, diamond_color
    draw_line(x, y+size, x+size, y, color)
    draw_line(x+size, y, x, y-size, color)
    draw_line(x, y-size, x-size, y, color)
    draw_line(x-size, y, x, y+size, color)
def catcher():
    x, y, width, height = catcher_x, 30, catcher_width, catcher_height
    if game_over:
        color = (1,0,0)
    else:
        color=catcher_color  
    draw_line(x-width//2, y, x-width//4, y-height, color)
    draw_line(x-width//4, y-height, x+width//4, y-height, color)
    draw_line(x+width//4, y-height, x+width//2, y, color)
    draw_line(x-width//2, y, x+width//2, y, color)

#main game
def initialize(): #proti game start hoile eita hoi shurute
    global diamond_x, diamond_y, diamond_speed, score, game_over, paused, catcher_x
    diamond_x = random.randint(30, window_width-30)
    diamond_y = window_height - 100
    if (window_width//2-30) <= diamond_x <= (window_width//2+30): #middle button 
        if random.choice([True,False]):
            diamond_x=(window_width//2)-40
        else:
            diamond_x=(window_width//2)+40
    diamond_speed = 3

def click(point_x, point_y, icon_x, icon_y):
    # ekta box er moto kaj kore oi box er bhitore click korle kaj kore

    if icon_x == 40 and icon_y == window_height-40: #restart button
        if (10 <= point_x <= 70) and ((window_height-70) <= point_y <= (window_height-10)):
            return True
   
    elif icon_x == window_width//2 and icon_y == window_height-40: #middle button 
         if ((window_width//2-30) <= point_x <= (window_width//2+30)) and ((window_height-70) <= point_y <= (window_height-10)):
             return True
   
    elif icon_x == window_width-40 and icon_y == window_height-40: #exit button 
        if ((window_width-70) <= point_x <= (window_width-10)) and ((window_height-70) <= point_y <= (window_height-10)):
            return True
    else:
        return False

def reset_diamond():
    global diamond_x, diamond_y,diamond_color
    diamond_x = random.randint(30, window_width-30) #left ar right button 80 deyar jonno handle hoye jacche
    diamond_y = window_height - 100
    diamond_color = (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))

def progress(delta_time):
    global diamond_y, score, game_over, diamond_speed,paused

    if game_over or paused:
        return None
    
    diamond_y -= diamond_speed * delta_time * 60  #frame er upore hocche

    if check_collision():
        score += 1
        print(f"Score: {score}")
        reset_diamond()
        diamond_speed += .3

    if diamond_y < 0:
        game_over = True
        print(f"Game Over! Final Score: {score}")
        
def mouselistener(button, state, x, y):
    global paused
    # convert kortesi y coordinate opengl theke glut (GLUT er 0,0 origin top-left e, OpenGL e 0,0 origin bottom-left e)
    y = window_height - y
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if click(x, y, 40, window_height-40):
            initialize()
            print("Starting Over")
        elif click(x, y, window_width//2, window_height-40):
            paused = not paused 
            print("Pause/Play toggled")
        elif click(x, y, window_width-40, window_height-40):
            print(f"Goodbye! Final Score: {score}")
            glutLeaveMainLoop()  #it stops the whole game and everything

def special_keys(key,x,y):
    global catcher_x
    
    if game_over or paused:
        return
    if key == GLUT_KEY_LEFT:
        catcher_x = max(catcher_x - 20, catcher_width//2)
    elif key == GLUT_KEY_RIGHT:
        catcher_x = min(catcher_x + 20, window_width - catcher_width//2)  

def animation() :
    global last_time
    #from internet, delta time
    current_time = time.time()
    if last_time == 0:
        delta_time = 0
    else:
        delta_time = current_time - last_time
    last_time = current_time
    
    progress(delta_time)
    glutPostRedisplay()

def iterate():
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, window_width, 0.0, window_height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0, 0, 0, 1)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    diamond()
    restart_button()
    if paused==True:
        play_button()
    else:
        pause_button()
    catcher()
    exit_button()
    iterate()
    glutSwapBuffers()


window_width = 500
window_height = 800
diamond_x = 0
diamond_y = 0
x, y = window_width // 2, window_height // 2
catcher_x = window_width // 2
catcher_width = 150
catcher_height = 20  
catcher_color=(1,1,1)
diamond_size = 15
diamond_color = (1,1,0)
score = 0
game_over = False
paused = False
last_time = time.time() #time function use korsi aste aste speed bare diamond er


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(window_width, window_height)
glutCreateWindow(b"Catch the Diamonds!")
glPointSize(2.0) #pixel-line size barai
glutSpecialFunc(special_keys)
glutMouseFunc(mouselistener)
glutIdleFunc(animation)
glLoadIdentity()
glutDisplayFunc(display)
initialize()
glutMainLoop()
