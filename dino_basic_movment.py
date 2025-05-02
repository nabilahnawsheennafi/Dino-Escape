from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random

# Dino position
dino_x, dino_y, dino_z = 0, 0, 0
move_step = 2
speed_multiplier = 1.0
dino_facing_left = False #


# Jumping variables
is_jumping = False
jump_velocity = 0
gravity = -0.25
jump_start_velocity = 6.5
max_fall_speed = -0.1

# Gem system
gems_collected = 0
gem_positions = [(random.randint(-100, 100), -80)] 
gem_spawn_z = -80  
speed_multiplier = 1.0

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)  

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1, 1, 1)  
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_dino(x, y, z):
    glPushMatrix()
    glTranslatef(x, y+5, z)

    if dino_facing_left:
        glRotatef(180, 0, 1, 0)  

    glColor3f(0.0, 0.8, 0.2)  

    block = 3  

    # Head
    head = [(0,4),(1,4),(2,4),(0,3),(1,3),(2,3)]
    for py in range(3, 5):  
        for px in range(0, 3):  
            glPushMatrix()
            glTranslatef(px * block, py * block, 0)
            glutSolidCube(block)
            glPopMatrix()


    # Neck + Body
    body = [(0,2),(0,1),(0,0),(-1,0),(-2,0),(-2,1),(-2,2)]
    for px, py in body:
        glPushMatrix()
        glTranslatef(px*block, py*block, 0)
        glutSolidCube(block)
        glPopMatrix()

    # Arms
    glPushMatrix()
    glTranslatef(-1*block, 1*block, 0)
    glutSolidCube(block)
    glPopMatrix()

    # Legs
    legs = [(-1,-1), (-2,-1)]
    for px, py in legs:
        glPushMatrix()
        glTranslatef(px*block, py*block, 0)
        glutSolidCube(block)
        glPopMatrix()

    # Tail
    tail = [(-3,1),(-4,2),(-5,3)]
    for px, py in tail:
        glPushMatrix()
        glTranslatef(px*block, py*block, 0)
        glutSolidCube(block)
        glPopMatrix()

    glPopMatrix()

def draw_ground():
    glColor3f(0.6, 0.29, 0.0)  
    glBegin(GL_QUADS)
    glVertex3f(-1000, 0, -1000)
    glVertex3f(1000, 0, -1000)
    glVertex3f(1000, 0, 1000)
    glVertex3f(-1000, 0, 1000)
    glEnd()

def draw_gems():
    glColor3f(0.2, 0.9, 1.0)  
    quadric = gluNewQuadric()

    for gx, gz in gem_positions:
        glPushMatrix()
        glTranslatef(gx, 3, gz)  

        # Top
        glPushMatrix()
        glTranslatef(0, 1.5, 0)             
        glRotatef(-90, 1, 0, 0)             
        gluCylinder(quadric, 3.0, 0.0, 3.0, 16, 1)  
        glPopMatrix()

        # Bottom
        glPushMatrix()
        glTranslatef(0, 1.5, 0)           
        glRotatef(90, 1, 0, 0)              
        gluCylinder(quadric, 3.0, 0.0, 3.0, 16, 1)
        glPopMatrix()

        glPopMatrix()


def check_gem_collision():
    global gem_positions, gems_collected, move_step, speed_multiplier

    new_positions = []
    for gx, gz in gem_positions:
        dist = math.sqrt((dino_x - gx)**2 + (dino_z - gz)**2)
        if dist < 10 and dist < 10:
            gems_collected += 1
            speed_multiplier += 0.25
            move_step = int(3 * speed_multiplier)

            # Spawn new gem at random x, same z
            new_x = random.randint(-100, 100)
            new_positions.append((new_x, gem_spawn_z))
        else:
            new_positions.append((gx, gz))

    gem_positions[:] = new_positions

def idle():
    global dino_y, jump_velocity, is_jumping

    if is_jumping:
        dino_y += jump_velocity
        jump_velocity += gravity

        if jump_velocity < max_fall_speed:
            jump_velocity = max_fall_speed

        if dino_y <= 0:
            dino_y = 0
            jump_velocity = 0
            is_jumping = False
            glutIdleFunc(None)  

        glutPostRedisplay()

def showScreen():
    global gems_collected
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(0, 100, 300,   
              0, 0, 0,       
              0, 1, 0)       

    draw_ground()
    draw_gems()
    draw_dino(dino_x, dino_y, dino_z)

    draw_text(10, 760, f"Game Score: {gems_collected}")

    glutSwapBuffers()

def keyboardListener(key, x, y):
    global dino_x, dino_z, is_jumping, jump_velocity, dino_facing_left

    min_x, max_x = -165, 170
    min_z, max_z = -165, 170

    if key == b'a':
        dino_x -= move_step
        dino_facing_left = True
    elif key == b'd':
        dino_x += move_step
        dino_facing_left = False
    elif key == b'w':
        dino_z -= move_step
    elif key == b's':
        dino_z += move_step
    elif key == b' ' and not is_jumping:
        is_jumping = True
        jump_velocity = jump_start_velocity
        glutIdleFunc(idle)

    dino_x = max(min_x, min(max_x, dino_x))
    dino_z = max(min_z, min(max_z, dino_z))

    check_gem_collision()
    glutPostRedisplay()


def init():
    glClearColor(0.5, 0.8, 1.0, 1.0) 
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1, 1, 1000)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Dino Movement with Gems")

    init()
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutIdleFunc(idle)
    glutMainLoop()

main()
