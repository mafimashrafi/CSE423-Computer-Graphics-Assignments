from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

w_width, w_height = 500, 500
speed = 0.1
vertex_x, vertex_y = random.randint(0, w_width), random.randint(0, 500)
directions = [[-1, 1], [1, 1], [-1, -1], [1, -1]]
direction = random.choice(directions)
coordinates = []
R, G, B = random.random(), random.random(), random.random()
coordinates.append([vertex_x, vertex_y, direction[0], direction[1], (R, G, B)])
pause = True
dot_visibility = True
blinking = False

class createDot:
    def draw(self, vertex_x, vertex_y, color):

        glPointSize(5)
        glBegin(GL_POINTS)
        glColor3f(*color)
        glVertex2f(vertex_x, vertex_y)
        glEnd()


def display():
    global coordinates, dot_visibility

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)

    if dot_visibility:
        for x, y, _, _, color in coordinates:
            createDot().draw(x, y, color)

    glutSwapBuffers()

def restore_visibility(arg):
    global dot_visibility
    dot_visibility = True

    glutPostRedisplay()

def blinker(value):
    global dot_visibility, blinking
    
    if blinking:
            dot_visibility = not dot_visibility
            glutTimerFunc(500, blinker, 0)    
    else:
        dot_visibility =True


    glutPostRedisplay()    


def mouse_listener(button, state, x, y):
    global w_width, w_height, coordinates, directions, dot_visibility, blinking
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            vertex_x = random.randint(0, w_width)
            vertex_y = random.randint(0, w_height)
            direction = random.choice(directions)
            R, G, B = random.random(), random.random(), random.random()
            coordinates.append([vertex_x, vertex_y, direction[0], direction[1], (R, G, B)]) 

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blinking = not blinking
        if blinking:
            glutTimerFunc(0, blinker, 0)
        else:
            dot_visibility = True


    glutPostRedisplay()

def specialkey_listener(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        speed+=0.1
    if key == GLUT_KEY_DOWN:
        speed-=0.1
        if speed < 0 :
            speed = 0.01

    glutPostRedisplay()

def normal_key_listener(key, x, y):
    global pause, BR, BG, BB
    if key == b' ':
        pause = not pause

    glutPostRedisplay()
    

def animate():
    global w_width, w_height, coordinates
    if pause:
        for dots in coordinates:
            vertex_x, vertex_y, direction_x, direction_y, color = dots
            if vertex_x >= w_width:
                direction_x *= (-1)
            elif vertex_x < 0:
                direction_x *= -1
                
            if vertex_y >= w_height:
                direction_y *= (-1)
            elif vertex_y <= 0:
                direction_y *= -1
            
            vertex_x += speed*direction_x
            vertex_y += speed*direction_y

            dots[0] = vertex_x
            dots[1] = vertex_y
            dots[2] = direction_x
            dots[3] = direction_y
            dots[4] = color

    glutPostRedisplay()


def init():
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w_width, 0, w_height)
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitWindowSize(w_width, w_height)
glutInitWindowPosition(100, 100)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )

window = glutCreateWindow(b'Magic Box')
init()

glutDisplayFunc(display)
glutIdleFunc(animate)
glutMouseFunc(mouse_listener)
glutSpecialFunc(specialkey_listener)
glutKeyboardFunc(normal_key_listener)

glutMainLoop()