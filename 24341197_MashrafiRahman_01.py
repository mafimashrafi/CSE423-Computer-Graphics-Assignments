#task1 
from OpenGL.GL import *
from OpenGL.GLUT import *  
from OpenGL.GLU import * 
import random 

window_width, window_height = 500, 500
R, G, B = 0.0, 0.0, 0.0
target_R, target_G, target_B = 0.0, 0.0, 0.0 
color_step = 0.01 
raindrops = []
diagonal_value_shift = 0

class Rain:
    def __init__ (self, x, y, x1=0):
        self.x = x
        self.y = y
        self.x1 = x
        self.speed = 0.5

    def convert_coordinate(self, left_x ):
        self.x1 = self.x + 10
        return self.x1


    def draw_raindrop(self, R, G, B, diagonal):
        rain_drop_length = [30, 25, 20]
        length = random.choice(rain_drop_length)

        if self.x1 > 0 and self.x1 < window_width:

            glPointSize(5)
            glBegin(GL_LINES)
            glColor3f(R, G, B)
            glVertex2f(self.x, self.y)
            glVertex2f(self.x1+diagonal, self.y -length)
            glEnd()

    def animate(self):
        self.x += self.speed
        self.y -= self.speed
        if self.y < 0 and self.x > window_width:
            self.y = window_height
            self.x = random.randint(0, window_width)
        self.x1 = self.x
        glutPostRedisplay()


class House_Roof:
    def draw(self):
        glBegin(GL_TRIANGLES)
        glColor3f(0,0,1)
        glVertex2f(170, 320)
        glVertex2f(330, 320)
        glColor3f(0, 0.5, 1)
        glVertex2f(250, 400)
        glEnd()

class House_Door:
    def draw(self):
        glBegin(GL_TRIANGLES)
        glColor3f(0, 0.5, 1)
        glVertex2f(235, 220)
        glVertex2f(260, 220)
        glVertex2f(235, 290)

        glColor3f(0, 0.5, 1)
        glVertex2f(235, 290)    
        glVertex2f(260, 220)
        glVertex2f(260, 290)
        glEnd()

    def draw_knob(self):
        glPointSize(10)
        glColor3f(0, 0, 0)
        glBegin(GL_POINTS)
        glVertex2f(255, 265)
        glEnd()

class House_Window:
    def __init__(self, x, y, x1, y1):
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1

    def draw(self):
        glBegin(GL_TRIANGLES)
        glColor3f(0, 0.5, 1)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x1, self.y)
        glVertex2f(self.x, self.y1)

        
        glColor3f(0, 0.5, 1)
        glVertex2f(self.x, self.y1)   
        glVertex2f(self.x1, self.y)
        glVertex2f(self.x1, self.y1) 
        glEnd() 

    def draw_lines(self):
        glPointSize(5)
        glBegin(GL_LINES)
        glColor3f(0, 0, 0)
        glVertex2f(((self.x1-self.x)/2)+self.x, self.y)
        glVertex2f(((self.x1-self.x)/2)+self.x, self.y1)
        glVertex2f(self.x, (self.y1-self.y)/2+self.y)
        glVertex2f(self.x1, (self.y1-self.y)/2+self.y)
        glEnd()

class House_Walls:
    def draw(self):
        glColor3f(1,1,1)
        glBegin(GL_TRIANGLES)
        glVertex2f(190, 220)
        glVertex2f(310, 220)
        glVertex2f(190, 320)

        glColor3f(1,1,1)
        glVertex2f(190, 320)
        glVertex2f(310, 220)
        glVertex2f(310, 320)
        glEnd()


class Triangle_grass: 
    def __init__(self, x, y, top):
        self.x = x
        self.y = y
        self.top = top

    def draw(self):
        glBegin(GL_TRIANGLES)
        glColor3f(0.0, 1.0, 0.0)  
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + 20, self.y)
        # glColor3f(0.6667, 0.3333, 0.0)
        glVertex2f(self.x + 10, self.top)
        glEnd()


class FrontBackground: 
    def __init__ (self):
        self.color = (0.6667, 0.3333, 0.0)
        self.x = 0
        self.y = 0
        self.width = window_width
        self.height = window_height*(3/4)

    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(*self.color)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

def display():
    global raindrops

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)

    FrontBackground().draw()
    for i in range(0, window_width, 20):
            Triangle_grass(i, 300, 350).draw()
    House_Walls().draw()
    x = 190+10
    x1 = 190+25+10
    y = 270+5
    y1 =270+10+20
    House_Window(x, y, x1, y1).draw()
    House_Window(x, y, x1, y1).draw_lines()
    House_Window(x+70, y, x1+70, y1).draw()
    House_Window(x+70, y, x1+70, y1).draw_lines()

    House_Door().draw()
    House_Door().draw_knob()
    House_Roof().draw()

    for i in range(200):
        rain_x = random.randint(0, window_width)
        rain_y = random.randint(0, window_height)
        rain = Rain(rain_x, rain_y)

        rain_R = random.random()
        rain_G = random.random()
        rain_B = random.random()
        rain.draw_raindrop(rain_R, rain_G, rain_B, diagonal_value_shift)
        raindrops.append(rain)
    
    glutSwapBuffers()

def mouse_Listener(button, state, x, y):
    global R, G, B , target_R, target_G, target_B
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            target_R = 1.0
            target_G = 1.0
            target_B = 1.0
    elif button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            target_R = 0.114
            target_G = 0.67
            target_B = 0.988
    else:
        target_R = 0.0
        target_G = 0.0
        target_B = 0.0

def specialkey_listener(key, x, y):
    global raindrops, diagonal_value_shift
    if key == GLUT_KEY_LEFT:
        diagonal_value_shift = 20
    elif key == GLUT_KEY_RIGHT:
        diagonal_value_shift = -20
    else: 
        diagonal_value_shift = 0
    glutPostRedisplay()

def init(R, G, B):
    glClearColor(R, G, B, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    gluPerspective(104, 1, 1, 1000.0)

def animate():
    global R, G, B, target_R, target_G, target_B, color_step, raindrops

    if R < target_R:
        R = min(R + color_step, target_R)
    elif R > target_R:
        R = max(R - color_step, target_R)
    if G < target_G:
        G = min(G + color_step, target_G)
    elif G > target_G:
        G = max(G - color_step, target_G)
    if B < target_B:
        B = min(B + color_step, target_B)
    elif B > target_B:
        B = max(B - color_step, target_B)
    init(R, G, B)
    for rain in raindrops:
        rain.animate()
    glutPostRedisplay()

glutInit()
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(100, 100)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

window = glutCreateWindow(b"Task1 Rain Animation")
init(R, G, B)

glutDisplayFunc(display)

glutMouseFunc(mouse_Listener)
glutSpecialFunc(specialkey_listener)
glutIdleFunc(animate)

glutMainLoop()

#task2
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