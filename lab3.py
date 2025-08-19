from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

Grid_length = 60
camera_pos = (0, 400, 6) 
fovY = 120
player_x, player_y, player_z = 0, 0, 0 

def borders_of_grid():
    global player_x, player_y, player_z

    glBegin(GL_QUADS)
    glColor3f(0, 0, 1)
    glVertex3f(-600, -600, 100)
    glVertex3f(-600, -600, 0)
    glVertex3f(-600, 600, 0)
    glVertex3f(-600, 600, 100)

    glColor3f(1, 0, 0)
    glVertex3f(-600, 600, 100)
    glVertex3f(-600, 600, 0)
    glVertex3f(600, 600, 0)    
    glVertex3f(600, 600, 100)

    glColor3f(0, 1, 0)
    glVertex3f(600, 600, 100)    
    glVertex3f(600, 600, 0)
    glVertex3f(600, -600, 0)
    glVertex3f(600, -600, 100)

    glColor3f(1, 0.5, 1)
    glVertex3f(600, -600, 100)
    glVertex3f(600, -600, 0)    
    glVertex3f(-600, -600, 0)
    glVertex3f(-600, -600, 100)
    glEnd()

    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(player_x, player_y, player_z)  
    gluCylinder(gluNewQuadric(), 10, 15, 20, 10, 10)
    glTranslatef(player_x+40, player_y, player_z)  
    gluCylinder(gluNewQuadric(), 10, 15, 20, 10, 10)
    glColor3f(0, 1, 0)
    glTranslatef(player_x - 20, player_y, player_z+60)
    glScalef(1.2, 0.5, 1.3)
    glutSolidCube(60)
    glColor3f(0, 0, 1)
    glTranslatef(player_x , player_y, player_z+50) 
    glutSolidSphere(20, 10, 10)
    glColor3f(0.5, 0.5, 0.5)
    # glRotatef(90, 0, 1, 0) 
    glTranslatef(player_x, player_y, player_z)
    gluCylinder(gluNewQuadric(), 15, 5, 40, 10, 10)
    glPopMatrix()

def draw_tile(is_white=True):
    """Draw a single square tile on XY plane"""
    if is_white:
        glColor3f(1, 1, 1)
    else:
        glColor3f(0.7, 0.5, 0.95)

    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(Grid_length, 0, 0)
    glVertex3f(Grid_length, Grid_length, 0)
    glVertex3f(0, Grid_length, 0)
    glEnd()


def camera_setup():
    global camera_pos, fovY
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1000/800, 1, 5000) 
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    x, y, z = camera_pos
    gluLookAt(x, y, z,
               0, 0, 0,
               0, 0, 1)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, 1000, 800)
    camera_setup()

    for i in range(-10, 10):
        for j in range(-10, 10):
            glPushMatrix()
            glTranslatef(i * Grid_length, j * Grid_length, 0)

            # alternate color
            is_white = (i + j) % 2 == 0
            draw_tile(is_white)

            glPopMatrix()
    borders_of_grid()   

    glutSwapBuffers()


def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0, 0, 0, 1)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(1000, 800)   
glutInitWindowPosition(100, 100)
window = glutCreateWindow(b"3D OpenGL Checkerboard Grid")
init()
glutDisplayFunc(display)

glutMainLoop()