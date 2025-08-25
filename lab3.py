from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

Grid_length = 60
fpps = False
player_x, player_y, player_z = 0, 0, 0 
camera_pos = (0, 400, 600)
fovY = 120
if fpps == True:
    player_y += 60
    fovY = 150
    camera_pos = (player_x, player_y, player_z+ 65) 

enemie = [(random.randint(-550, 550),random.randint(-550, 550), 40), (random.randint(-550, 550), random.randint(-550, 550), 40),
          (random.randint(-550, 550), random.randint(-550, 550), 40), (random.randint(-550, 550), random.randint(-550, 550), 40),
          (random.randint(-550, 550), random.randint(-550, 550), 40)]

def enemies(enemy_x, enemy_y, enemy_z):
    glPushMatrix()
    glColor(1, 0, 0)
    glTranslatef(enemy_x, enemy_y, enemy_z)
    glutSolidSphere(40, 10, 10)
    glColor(0, 1, 0)
    glTranslatef(0, 0, 50)
    glutSolidSphere(20, 10, 10)
    glPopMatrix()

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

    #making body and gun
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
    glRotatef(-90, 0, 1, 0) 
    glRotatef(90, 1, 0, 0)
    glTranslatef(player_x-40, player_y, player_z + 35)
    gluCylinder(gluNewQuadric(), 15, 5, 80, 10, 10)

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
    global enemie

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
    for i in enemie:
        x, y, z = i
        enemies(x, y, z)
        
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