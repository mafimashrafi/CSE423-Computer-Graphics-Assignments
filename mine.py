from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random
import sys
import time

w_width, w_height = 800, 600
BROWN = (0.6, 0.3, 0.1)

def draw_target():
    x = random.uniform(-20, 20)
    y = random.uniform(-8, 10)
    z = -39 

    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1, 0, 0)
    glutSolidSphere(4, 6, 6)
    glPopMatrix()

def draw_range():
    glColor3f(0.4, 0.6, 0.4)  # Green floor
    glBegin(GL_QUADS)
    glVertex3f(-30, -12, -40)
    glVertex3f(30, -12, -40)
    glVertex3f(30, -12, 5)
    glVertex3f(-30, -12, 5)
    glEnd()
    
    # Draw back wall
    glColor3f(0.8, 0.8, 0.9)  # Light gray wall
    glBegin(GL_QUADS)
    glVertex3f(-30, -12, -40)
    glVertex3f(30, -12, -40)
    glVertex3f(30, 15, -40)
    glVertex3f(-30, 15, -40)
    glEnd()
    
    # Draw side walls
    glColor3f(0.7, 0.7, 0.8)
    glBegin(GL_QUADS)
    # Left wall
    glVertex3f(-30, -12, -40)
    glVertex3f(-30, 15, -40)
    glVertex3f(-30, 15, 5)
    glVertex3f(-30, -12, 5)
    # Right wall  
    glVertex3f(30, -12, -40)
    glVertex3f(30, -12, 5)
    glVertex3f(30, 15, 5)
    glVertex3f(30, 15, -40)
    glEnd()
    
    # Draw ceiling
    glColor3f(0.9, 0.9, 0.9)
    glBegin(GL_QUADS)
    glVertex3f(-30, 15, -40)
    glVertex3f(30, 15, -40)
    glVertex3f(30, 15, 5)
    glVertex3f(-30, 15, 5)
    glEnd()
    
    # Draw shooting booth
    glColor3f(*BROWN)
    glBegin(GL_QUADS)
    # Booth table
    glVertex3f(-3, -2, 3)
    glVertex3f(3, -2, 3)
    glVertex3f(3, -2, 5)
    glVertex3f(-3, -2, 5)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(0, 0, 5,      # Camera at shooting booth
              0, 0, -10,    # Looking down range
              0, 1, 0)

    draw_range()
    # draw_target()

    glutSwapBuffers()

def reshape(width, height):
    global window_width, window_height
    window_width = width
    window_height = height
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glClearColor(0.6, 0.8, 1.0, 1.0)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(w_width, w_height)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Olympic Shooting")

init()
glutDisplayFunc(display)
glutReshapeFunc(reshape)

glutMainLoop()