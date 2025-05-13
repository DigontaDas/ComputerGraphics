from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
# Camera-related variables
camera_pos = (100, 100, 400)
fps_mode=False

fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines

#bullet
bullet_sequence = []  
bullet_speed = 8

#hero infos
hero_pos = [300, 300, 30]  # hero position x,y,z (center of grid)
hero_angle = 0  # Angle of rotation (in degrees)
hero_life = 5
hero_rotation_speed=5
hero_size= [40,40,60] #bounding box for AABB collision
fps_mode=False
#enemy 
enemies=[] #each [x, y, z, size_factor, size_direction]
enemy_base=15 #base size for multiple use korar jonno
enemy_speed=.2
#for text
game_score = 0
missing_bullet = 0
game_over = False
#cheatmode
cheat_mode=False
automated_gun=False
body_rotation_time=0

def grid():
    grid_size = GRID_LENGTH # Number of cells in each direction
    cell_size = grid_size / 13
    wall_height=100
    glBegin(GL_QUADS)
    for i in range(13):
        for j in range(13):
            # Calculate the corners of each cell
            x1 = i * cell_size
            y1 = j * cell_size
            x2 = (i + 1) * cell_size
            y2 = (j + 1) * cell_size
            
            # Set color based on checkerboard pattern
            if (i + j) % 2 == 0:
                glColor3f(1.0, 1.0, 1.0)  # White
            else:
                glColor3f(0.7, 0.5, 0.95)  # Purple
            
            # Draw the cell
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
    glEnd()
    
    glBegin(GL_QUADS)
    glColor3f(0, 1, 1)
    glVertex3f(0, grid_size, 0)
    glVertex3f(grid_size, grid_size, 0)
    glVertex3f(grid_size, grid_size, wall_height)
    glVertex3f(0, grid_size, wall_height)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(1, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(grid_size, 0, 0)
    glVertex3f(grid_size, 0, wall_height)
    glVertex3f(0, 0, wall_height)
    glEnd()


    glColor3f(0,0,1)  # Bluish color for contrast
    glBegin(GL_QUADS)
    glVertex3f(grid_size, 0, 0)
    glVertex3f(grid_size, grid_size, 0)
    glVertex3f(grid_size, grid_size, wall_height)
    glVertex3f(grid_size, 0, wall_height)
    glEnd()

    glColor3f(0,1,0)
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(0, grid_size, 0)
    glVertex3f(0, grid_size, wall_height)
    glVertex3f(0, 0, wall_height)
    glEnd() 
def hero():
    glPushMatrix()
    glTranslatef(hero_pos[0], hero_pos[1], hero_pos[2])
    if game_over:
        glRotatef(90, 1, 0, 0)
    else:
        glRotatef(hero_angle, 0, 0, 1)
    #body
    glTranslatef(0, 0, 10 )
    glScalef(.7,.7,1.4)
    glColor3f(0.2, 0.5, 0.2)  
    glutSolidCube(40)
    
    #head
    glPushMatrix()
    glTranslatef(0, 0, 30 )
    glColor3f(0, 0, 0)
    gluSphere(gluNewQuadric(), 12 , 15, 15)
    glPopMatrix()
    #hands
    glPushMatrix()
    glTranslatef(10, 15, 0)
    glRotatef(90, 0, 1, 0)
    glColor3f(.93, 0.68, 0.53)  
    gluCylinder(gluNewQuadric(), 10, 2, 30, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(10, -15, 0)
    glRotatef(90, 0, 1, 0)
    glColor3f(.93, 0.68, 0.53)  
    gluCylinder(gluNewQuadric(), 10, 2, 30, 10, 10)
    glPopMatrix()
    
    # Left leg
    glPushMatrix()
    glTranslatef(0, 10, -35)
    glColor3f(0, 0, 1)  
    gluCylinder(gluNewQuadric(), 10, 3, 30, 10, 10)
    glPopMatrix()
    
    # Right leg
    glPushMatrix()
    glTranslatef(0, -10, -35)
    glColor3f(0, 0, 1)  
    gluCylinder(gluNewQuadric(), 10, 3, 30, 10, 10)
    glPopMatrix()

    #gun 
    glPushMatrix()
    glTranslatef(10, 0, 0)
    glRotatef(90, 0, 1, 0)
    glColor3f(0.3, 0.3, 0.3) 
    gluCylinder(gluNewQuadric(), 10, 2, 60, 10, 10)
    glPopMatrix()
    
    glPopMatrix()
def restart():
    global hero_pos,hero_angle,hero_life,automated_gun,game_over,enemies,game_score,missing_bullet,bullet_sequence,cheat_mode
    print(f"Remaining hero Life: {hero_life}")
    hero_pos=[300,300,30]
    hero_angle=0
    hero_life=5
    game_score=0
    missing_bullet=0
    game_over=False
    cheat_mode=False
    bullet_sequence=[]
    automated_gun=False
    enemies=[]
    start_enemies()  
def text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
def bullets(): #create
    global bullet_sequence
    for bullet in bullet_sequence:
        glPushMatrix()
        glTranslatef(bullet[0], bullet[1], bullet[2])
        glColor3f(1, 0, 0)  
        glutSolidCube(4) 
        glPopMatrix()
def fire_bullet(): #fire
    global bullet_sequence,hero_pos,game_over,hero_angle

    if game_over==False:

        #bullet direction based on hero angle
        dx = math.cos(math.radians(hero_angle))
        dy = math.sin(math.radians(hero_angle))

        gun_length = 10 #tip of the gun
        x = hero_pos[0] + dx * gun_length
        y = hero_pos[1] + dy * gun_length
        z = hero_pos[2] + 5  # Bullet height
        bullet_sequence.append([x, y, z, dx, dy])# adding bullet with position and direction
        print("hero Bullet Fired!")
    else:
        return
def update_bullets(): #update
    global bullet_sequence, bullet_speed, GRID_LENGTH, missing_bullet, game_score, game_over, enemies
    i = 0
    while i < len(bullet_sequence):
        bullet = bullet_sequence[i]#current bullet
        bullet[0] += bullet[3] * bullet_speed  #position based on direction
        bullet[1] += bullet[4] * bullet_speed   #position based son direction
        hit = False
        j = 0
        while j < len(enemies) and not hit:
            enemy = enemies[j]
            enemy_pos = [enemy[0], enemy[1], enemy[2]]
            enemy_size = [30 * 2 * enemy[3]] * 3  #30*size for main body ,30 instead of enemy_base
            bullet_pos = [bullet[0], bullet[1], bullet[2]]
            bullet_size = [5, 5, 5]  #larger bullet hitbox

            if check_collision(bullet_pos, bullet_size, enemy_pos, enemy_size):
                game_score += 1
                x, y = 0, 0 
                while True:#respawn the hit enemy at a random position
                    x = random.uniform(60, GRID_LENGTH - 60)
                    y = random.uniform(60, GRID_LENGTH - 60)
                    dist = math.sqrt((x - hero_pos[0])**2 + (y - hero_pos[1])**2)
                    if dist > 150:  # keep enemy away from hero
                        break
                enemies[j] = [x, y, enemy_base, 1.0, 1] #reset
                hit = True
            j += 1
                                    #bullet hits wall or not
        hit_wall = (bullet[0] < 0 or bullet[0] > GRID_LENGTH or 
                         bullet[1] < 0 or bullet[1] > GRID_LENGTH)
        if hit_wall==True:
            missing_bullet += 1
            print(f"Bullet missed : {missing_bullet}")
            if missing_bullet >= 10: #10 tar beshi bullet wall e lagbena
                game_over = True
            bullet_sequence.pop(i)
        elif hit==True:
            bullet_sequence.pop(i)  # Remove bullet
        else:
            i += 1  # Move to next bullet
#took from assignment2 AABB collision technique       
def check_collision(obj1_pos, obj1_size, obj2_pos, obj2_size):
    """
    Check if two 3D objects (represented by their position and size) collide.
    
    Parameters:
    - obj1_pos: [x, y, z] position of object 1's center
    - obj1_size: [width, height, depth] size of object 1
    - obj2_pos: [x, y, z] position of object 2's center
    - obj2_size: [width, height, depth] size of object 2
    
    Returns:
    - True if collision detected, False otherwise
    """
    # Calculate half-sizes
    half_size1 = [s/2 for s in obj1_size]
    half_size2 = [s/2 for s in obj2_size]
    
    # Calculate min and max bounds for each object
    min1 = [obj1_pos[i] - half_size1[i] for i in range(3)]
    max1 = [obj1_pos[i] + half_size1[i] for i in range(3)]
    min2 = [obj2_pos[i] - half_size2[i] for i in range(3)]
    max2 = [obj2_pos[i] + half_size2[i] for i in range(3)]
    
    # Check overlap in all three dimensions
    x_overlap = min1[0] < max2[0] and max1[0] > min2[0]
    y_overlap = min1[1] < max2[1] and max1[1] > min2[1]
    z_overlap = min1[2] < max2[2] and max1[2] > min2[2]
    
    # Collision occurs only if all three dimensions overlap
    if x_overlap and y_overlap and z_overlap:
        return True
def inside_boundary(): #grid er baire hero jate chole na jai
    global hero_pos, GRID_LENGTH,hero_size
    hero_min_x = hero_pos[0] - hero_size[0]/2
    hero_max_x = hero_pos[0] + hero_size[0]/2
    hero_min_y = hero_pos[1] - hero_size[1]/2
    hero_max_y = hero_pos[1] + hero_size[1]/2

    #x
    if hero_min_x < 0:
        hero_pos[0] = hero_size[0]/2
    elif hero_max_x > GRID_LENGTH:
        hero_pos[0] = GRID_LENGTH - hero_size[0]/2
    #y
    if hero_min_y < 0:
        hero_pos[1] = hero_size[1]/2
    elif hero_max_y > GRID_LENGTH:
        hero_pos[1] = GRID_LENGTH - hero_size[1]/2
def enemy(): #draw
    global enemies, enemy_base
    for i in enemies:
        x,y,z,size,size_dir=i
        glPushMatrix()
        glTranslatef(x, y, z)
        #body
        glColor3f(1, 0, 0) 
        gluSphere(gluNewQuadric(), 30 * size, 20, 20)
        #head
        glTranslatef(0, 0, enemy_base * size * 1)
        glColor3f(0,0,0) 
        gluSphere(gluNewQuadric(), enemy_base* size * 1, 15, 15)
        glPopMatrix()
def enemy_army(): #position update and collision check kortese
    global enemies, hero_life,game_over,hero_size,enemy_speed,enemy_base
    hero_size = [40, 40, 60]  # [width, depth, height] for AABB collision
    i = 0
    while i < len(enemies):
        one_enemy = enemies[i]
        #pulsing effect
        one_enemy[3] += one_enemy[4] * .01 #(size change)  
        if one_enemy[3] > 1.3:
            one_enemy[3] = 1.3
            one_enemy[4] = -1  #shrinking
        elif one_enemy[3] < 0.7:
            one_enemy[3] = 0.7
            one_enemy[4] = 1   #growing
        #move toward hero
        dx = hero_pos[0] - one_enemy[0]
        dy = hero_pos[1] - one_enemy[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:  #avoid division by zero
            # Normalize direction vector and multiply by speed
            one_enemy[0] += (dx / distance) * enemy_speed
            one_enemy[1] += (dy / distance) * enemy_speed

        if game_over==False:#collision check
            enemy_pos = [one_enemy[0], one_enemy[1], one_enemy[2]]
            enemy_size = [enemy_base * 2 * one_enemy[3]] * 3 
            if check_collision(hero_pos, hero_size, enemy_pos, enemy_size)==True:
                hero_life -= 1
                print(f"Remaining hero Life: {hero_life}")
                while True:
                    x = random.uniform(30, GRID_LENGTH - 30)
                    y = random.uniform(30, GRID_LENGTH - 30)
                    dist = math.sqrt((x - hero_pos[0])**2 + (y - hero_pos[1])**2)
                    if dist > 150:  # keep enemy away from hero
                        break
                enemies[i] = [x, y, enemy_base, 1.0, 1]
                if hero_life == 0:
                    game_over = True
        i += 1  
def start_enemies(): #create
    global enemies, GRID_LENGTH, hero_pos, enemy_base
    enemies = []  #clear
    for i in range(5):
        while True:
            x = random.uniform(30, GRID_LENGTH - 30)
            y = random.uniform(30, GRID_LENGTH - 30)
            # enemey jate heror beshi kache spawn na hoi
            dist = math.sqrt((x - hero_pos[0])**2 + (y - hero_pos[1])**2)
            if dist > 150:  # >150 units away from hero
                break
        # [x, y, z, size_factor, size_direction]
        enemies.append([x, y, enemy_base, 1.0, 1])
def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    if fps_mode==True:
        # First-person camera follows the hero
        # Calculate position slightly behind and above hero
        angle = math.radians(hero_angle)
        camera_x = hero_pos[0] 
        camera_y = hero_pos[1] 
        camera_z = hero_pos[2] + 80
        
        # Calculate look-at point in front of hero
        look_x = hero_pos[0] +100 * math.cos(angle)
        look_y = hero_pos[1] + 100 * math.sin(angle)
        look_z = hero_pos[2] + 40
        
        gluLookAt(camera_x, camera_y, camera_z,  # Camera position
                  look_x, look_y, look_z,        # Look-at target
                  0, 0, 1)                       # Up vector (z-axis)
    else:
        # Default third-person camera
        x, y, z = camera_pos
        gluLookAt(x, y, z,          # Camera position
                  200, 200, 0,      # Look-at center of grid
                  0, 0, 1)          # Up vector (z-axis)
def start_cheat_mode():
    global hero_angle, game_score,hero_pos,hero_size
    if cheat_mode==True and game_over==False:
        hero_angle = (hero_angle + 8) % 360  
        for enemy in enemies:
            dx = enemy[0] - hero_pos[0]
            dy = enemy[1] - hero_pos[1]
            if dx == 0 and dy == 0:
                continue
            enemy_angle = math.degrees(math.atan2(dy, dx)) % 360 #angle to enemy in degrees
            angle_diff = min((hero_angle - enemy_angle) % 360, (enemy_angle - hero_angle) % 360)
            if angle_diff < 5:  # difference between each bullets 
                enemy_pos = [enemy[0], enemy[1], enemy[2]]
                enemy_size = [enemy_base * 2 * enemy[3]] * 3  #for firing dummy enemy
                fire_bullet()
                if check_collision(hero_pos, hero_size, enemy_pos, enemy_size)==True:
                    game_score+=1
                    break
def showScreen():
    global game_over,hero_life,game_score,missing_bullet,camera_pos,cheat_mode
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size
    setupCamera()  # Configure camera perspective
    grid()
    if camera_pos[2] >= 0:  # Only show characters when viewed from above
        hero()
        if game_over==False:
            enemy()
            bullets()
    if game_over:
        text(30, 730, f"GAME OVER. Your Score is {game_score}")
        text(30, 700, "Press "R" to Restart")
    else:
        text(30, 760, f"Player Life Remaining: {hero_life}")
        text(30, 730, f"Game Score: {game_score}")
        text(30, 700, f"Player Bullet Missed: {missing_bullet}")
        if cheat_mode==True:
            text(30, 670, "Toggle V for cheat mode")
    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()
def keyboardListener(key, x, y):
    global hero_angle,hero_pos,game_score,hero_rotation_speed,cheat_mode,automated_gun
    """
    Handles keyboard inputs for hero movement, gun rotation, camera updates, and cheat mode toggles.
    """
    hero_movement=10
    # # Move forward (W key)
    if key == b'w':  
        hero_pos[0]+=hero_movement*math.cos(math.radians(hero_angle)) # x dike angle er value
        hero_pos[1]+=hero_movement*math.sin(math.radians(hero_angle)) # y dike angle er value 
        inside_boundary()

    # # Move backward (S key)
    if key == b's':
        hero_pos[0]-=hero_movement*math.cos(math.radians(hero_angle)) # x dike angle er value
        hero_pos[1]-=hero_movement*math.sin(math.radians(hero_angle)) # y dike angle er value 
        inside_boundary()
    # # Rotate gun left (A key)
    if key == b'a'and cheat_mode==False:
        hero_angle+=hero_rotation_speed
    # # Rotate gun right (D key)
    if key == b'd'and cheat_mode==False:
        hero_angle-=hero_rotation_speed
    # # Toggle cheat mode (C key)
    if key == b'c' and game_over==False:
        cheat_mode=True
    # # Toggle cheat vision (V key)
    if key == b'v' and game_over==False and cheat_mode==True:
        cheat_mode=not cheat_mode
    # # Reset the game if R key is pressed
    if game_over==True and key==b"r":
        restart()
        return
def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos
    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        z += 10

    # # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        z -= 10

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        y -= 10
        x-=5  # Small angle decrement for smooth movement
    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        y += 10  # Small angle increment for smooth movement
        x+=5
    camera_pos = (x, y, z)
def mouseListener(button, state, x, y):
    global fps_mode
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and game_over==False:
        fire_bullet()

        # # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and game_over==False:
        fps_mode=not fps_mode    
def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    if game_over==False:
        if cheat_mode==True:
            start_cheat_mode()
        update_bullets()
        enemy_army()
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()
# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    glutCreateWindow(b"Bullet Frenzy")  # Create the window
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    restart()
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically
    glutMainLoop()  # Enter the GLUT main loop
if __name__ == "__main__":
    main()
