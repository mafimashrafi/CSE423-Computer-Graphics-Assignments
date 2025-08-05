from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

game_over = False
paused = False
score = 0

# Delta timing
last_time = time.time()

# Midpoint line draw_lineing algorithm class
class mid_point_line_algo:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

    def find_zone(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) >= abs(dy):
            if dx >= 0 and dy >= 0:
                return 0
            elif dx < 0 and dy >= 0:
                return 3
            elif dx < 0 and dy < 0:
                return 4
            else:
                return 7
        else:
            if dx >= 0 and dy >= 0:
                return 1
            elif dx < 0 and dy >= 0:
                return 2
            elif dx < 0 and dy < 0:
                return 5
            else:
                return 6

    def zone_shiftin(self, x, y, zone):
        if zone == 0: 
            return x, y
        elif zone == 1: 
            return y, x
        elif zone == 2: 
            return y, -x
        elif zone == 3: 
            return -x, y
        elif zone == 4: 
            return -x, -y
        elif zone == 5: 
            return -y, -x
        elif zone == 6: 
            return -y, x
        elif zone == 7: 
            return x, -y

    def reverse_zone_shift(self, x, y, zone):
        if zone == 0: 
            return x, y
        elif zone == 1: 
            return y, x
        elif zone == 2: 
            return -y, x
        elif zone == 3: 
            return -x, y
        elif zone == 4: 
            return -x, -y
        elif zone == 5: 
            return -y, -x
        elif zone == 6: 
            return y, -x
        elif zone == 7: 
            return x, -y

    def draw_line(self):
        zone = self.find_zone(self.x1, self.y1, self.x2, self.y2)
        x1, y1 = self.zone_shiftin(self.x1, self.y1, zone)
        x2, y2 = self.zone_shiftin(self.x2, self.y2, zone)

        dx = x2 - x1
        dy = y2 - y1

        d = 2 * dy - dx
        dE = 2 * dy
        dNE = 2 * (dy - dx)

        x, y = x1, y1
        while x <= x2:
            px, py = self.reverse_zone_shift(x, y, zone)
            glBegin(GL_POINTS)
            glVertex2f(px, py)
            glEnd()
            x += 1
            if d > 0:
                y += 1
                d += dNE
            else:
                d += dE

class Diamond:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(-WINDOW_WIDTH//2 + 50, WINDOW_WIDTH//2 - 50)
        self.y = WINDOW_HEIGHT//2 - 30
        self.size = 20
        self.color = [random.random(), random.random(), random.random()]
        self.speed = 100

    def draw_line(self):
        glColor3f(*self.color)
        mid = [self.x, self.y]
        right = [self.x + self.size, self.y - self.size]
        bottom = [self.x, self.y - 2 * self.size]
        left = [self.x - self.size, self.y - self.size]

        for (a, b) in [(mid, right), (right, bottom), (bottom, left), (left, mid)]:
            mid_point_line_algo(a[0], a[1], b[0], b[1]).draw_line()

    def animation(self, dt):
        self.y -= self.speed * dt

        if check_collision(self.get_aabb(), catcher.get_aabb()):
            global score
            score += 1
            print("Score:", score)
            self.speed = min(self.speed + 20, 800)  # Speed up
            self.reset()
        elif self.y < -WINDOW_HEIGHT//2:
            global game_over
            print("Game Over. Final Score:", score)
            game_over = True
            catcher.color = [1, 0, 0]

    def get_aabb(self):
        return (self.x - self.size, self.y - 2 * self.size, self.size * 2, self.size * 2)

class Catcher:
    def __init__(self):
        self.width = 80
        self.height = 20
        self.x = 0
        self.y = -WINDOW_HEIGHT//2 + 40
        self.color = [1, 1, 1]
        self.speed = 300

    def draw_line(self):
        glColor3f(*self.color)
        top_left = [self.x - self.width//2, self.y + self.height//2]
        top_right = [self.x + self.width//2, self.y + self.height//2]
        bottom_right = [self.x + self.width//2, self.y - self.height//2]
        bottom_left = [self.x - self.width//2, self.y - self.height//2]

        for (a, b) in [(top_left, top_right), (top_right, bottom_right),
                      (bottom_right, bottom_left), (bottom_left, top_left)]:
            mid_point_line_algo(a[0], a[1], b[0], b[1]).draw_line()

    def get_aabb(self):
        return (self.x - self.width//2, self.y - self.height//2, self.width, self.height)

    def move(self, direction, dt):
        if direction == "left":
            self.x -= self.speed * dt
        elif direction == "right":
            self.x += self.speed * dt
        self.x = max(-WINDOW_WIDTH//2 + self.width//2, min(WINDOW_WIDTH//2 - self.width//2, self.x))

# Game elements
diamond = Diamond()
catcher = Catcher()

# Button stubs — for simplicity we omit full button rendering for now

def check_collision(aabb1, aabb2):
    return (
        aabb1[0] < aabb2[0] + aabb2[2] and
        aabb1[0] + aabb1[2] > aabb2[0] and
        aabb1[1] < aabb2[1] + aabb2[3] and
        aabb1[1] + aabb1[3] > aabb2[1]
    )

def update():
    global last_time
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    if game_over or paused:
        glutPostRedisplay()
        return

    diamond.animation(dt)  # Now animation handles fall + collision + scoring

    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    diamond.draw_line()
    catcher.draw_line()
    glutSwapBuffers()

def keyboard(key, x, y):
    global paused, game_over, score, diamond, catcher
    if game_over or paused:
        return
    key = key.decode("utf-8")
    if key == 'a':
        catcher.move("left", 0.03)
    elif key == 'd':
        catcher.move("right", 0.03)

def special_input(key, x, y):
    if key == GLUT_KEY_LEFT:
        catcher.move("left", 0.03)
    elif key == GLUT_KEY_RIGHT:
        catcher.move("right", 0.03)

def mouse(button, state, x, y):
    global game_over, paused, score
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if x < 100:  # Restart
            print("Starting Over")
            score = 0
            diamond.reset()
            catcher.color = [1, 1, 1]
            global game_over
            game_over = False
        elif 350 < x < 450:  # Toggle pause
            paused = not paused
        elif x > 700:  # Quit
            print("Goodbye. Final Score:", score)
            glutLeaveMainLoop()

def init():
    glClearColor(44/256, 45/256, 60/256, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-WINDOW_WIDTH//2, WINDOW_WIDTH//2, -WINDOW_HEIGHT//2, WINDOW_HEIGHT//2)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Catch the Diamonds")

init()
glutDisplayFunc(display)
glutIdleFunc(update)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_input)
glutMouseFunc(mouse)
glutMainLoop()