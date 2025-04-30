from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Dino position
dino_x, dino_y, dino_z = 0, 0, 0

# Dino movement step size
move_step = 3

# Jumping variables
is_jumping = False
jump_velocity = 0
gravity = -0.25
jump_start_velocity = 6.5
max_fall_speed = -0.1

def draw_dino(x, y, z):
    glPushMatrix()
    glTranslatef(x, y+5, z)
    glColor3f(0.0, 0.8, 0.2)  # Green Dino

    block = 3  # Small cube block size for pixel-art style

    # Head
    head = [(0,4),(1,4),(2,4),(0,3),(1,3),(2,3)]
    for px, py in head:
        glPushMatrix()
        glTranslatef(px*block, py*block, 0)
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
    glColor3f(0.6, 0.29, 0.0)  # Green ground
    glBegin(GL_QUADS)
    glVertex3f(-1000, 0, -1000)
    glVertex3f(1000, 0, -1000)
    glVertex3f(1000, 0, 1000)
    glVertex3f(-1000, 0, 1000)
    glEnd()

def idle():
    global dino_y, jump_velocity, is_jumping, max_fall_speed

    if is_jumping:
        dino_y += jump_velocity
        jump_velocity += gravity
            # Limit fall speed
        if jump_velocity < max_fall_speed:
            jump_velocity = max_fall_speed

        if dino_y <= 0:
            dino_y = 0
            jump_velocity = 0
            is_jumping = False
            glutIdleFunc(None)  # Stop idle animation when landed

        glutPostRedisplay()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Fixed camera
    gluLookAt(0, 100, 300,   # eye
              0, 0, 0,       # look at
              0, 1, 0)       # up

    draw_dino(dino_x, dino_y, dino_z)
    
    draw_ground()
    glutSwapBuffers()

def keyboardListener(key, x, y):
    global dino_x, dino_z, is_jumping, jump_velocity

    min_x, max_x = -165, 170
    min_z, max_z = -165, 170

    if key == b'a':
        dino_x -= move_step
    elif key == b'd':
        dino_x += move_step
    elif key == b'w':
        dino_z -= move_step
    elif key == b's':
        dino_z += move_step
    elif key == b' ' and not is_jumping:
        is_jumping = True
        jump_velocity = jump_start_velocity
        glutIdleFunc(idle)  # Start idle-based animation
 
    

    dino_x = max(min_x, min(max_x, dino_x))
    dino_z = max(min_z, min(max_z, dino_z))

    glutPostRedisplay()

def init():
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Sky blue
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1, 1, 1000)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0,0)

    glutCreateWindow(b"Dino Movement")

    init()
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutIdleFunc(idle)
    glutMainLoop()

main()
