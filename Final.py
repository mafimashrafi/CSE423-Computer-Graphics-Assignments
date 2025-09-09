from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random
import sys
import time

# Global variables
score = 0
bullets = []
targets = []
mouse_x = 400
mouse_y = 300
window_width = 800
window_height = 600
game_time = 0

# Colors for Olympic-style targets
WHITE = (1.0, 1.0, 1.0)
BLACK = (0.0, 0.0, 0.0)
RED = (1.0, 0.0, 0.0)
BLUE = (0.0, 0.0, 1.0)
YELLOW = (1.0, 1.0, 0.0)
GREEN = (0.0, 1.0, 0.0)
BROWN = (0.6, 0.3, 0.1)
GRAY = (0.5, 0.5, 0.5)

game_running = False
game_paused = False

class Bullet:
    def __init__(self, x, y, z, direction_x, direction_y, direction_z):
        self.x = x
        self.y = y
        self.z = z
        self.dx = direction_x * 1.2  # bullet speed
        self.dy = direction_y * 1.2
        self.dz = direction_z * 1.2
        self.active = True
        self.trail = []  # For bullet trail effect
    
    def update(self):
        if self.active:
            # Add current position to trail
            self.trail.append((self.x, self.y, self.z))
            if len(self.trail) > 10:  # Keep trail short
                self.trail.pop(0)
                
            self.x += self.dx
            self.y += self.dy
            self.z += self.dz
            
            # Remove bullet if it goes too far or hits back wall
            if self.z < -41 or abs(self.x) > 25 or abs(self.y) > 15:
                self.active = False
    
    def draw(self):
        if self.active:
            # Draw bullet trail
            glColor3f(1.0, 0.8, 0.0)
            glBegin(GL_LINE_STRIP)
            for i, pos in enumerate(self.trail):
                alpha = float(i) / len(self.trail)
                glColor3f(1.0 * alpha, 0.8 * alpha, 0.0)
                glVertex3f(pos[0], pos[1], pos[2])
            glEnd()
            
            # Draw bullet
            glPushMatrix()
            glTranslatef(self.x, self.y, self.z)
            glColor3f(1.0, 1.0, 0.0)
            glutSolidSphere(0.05, 6, 6)
            glPopMatrix()

class TargetType:
    def __init__(self, color, size, score):
        self.color = color
        self.size = size
        self.score = score

# Define some target types
TARGET_TYPES = [
    TargetType((1.0, 0.0, 0.0), 2.0, 10),   # Red, small, high score
    TargetType((0.0, 1.0, 0.0), 2.8, 7),    # Green, medium, medium score
    TargetType((0.0, 0.0, 1.0), 3.5, 4),    # Blue, large, low score
    TargetType((1.0, 1.0, 0.0), 1.2, 15),   # Yellow, very small, highest score
    ]
class OlympicTarget:
    def __init__(self, x, y, z, target_type):
        self.x = x
        self.y = y
        self.z = z
        self.active = True
        self.spawn_time = time.time()
        self.lifetime = 8.0
        self.size = target_type.size
        self.color = target_type.color
        self.score_value = target_type.score
        self.hit = False

    def update(self):
        if time.time() - self.spawn_time > self.lifetime:
            self.active = False
            if not self.hit:
                print("Target disappeared! No points.")

    def draw(self):
        if self.active:
            glPushMatrix()
            glTranslatef(self.x, self.y, self.z)
            glColor3f(*self.color)
            self.draw_filled_circle(self.size)
            glPopMatrix()

    def draw_filled_circle(self, radius):
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, 0)
        for i in range(33):
            angle = 2.0 * math.pi * i / 32
            glVertex3f(radius * math.cos(angle), radius * math.sin(angle), 0)
        glEnd()

    def is_hit_by(self, bullet):
        if not self.active or not bullet.active or self.hit:
            return False

        # Check if bullet crosses the target's z-plane between frames
        prev_z = bullet.z - bullet.dz
        # If bullet moved past the target's z position this frame
        if (prev_z > self.z and bullet.z <= self.z) or abs(bullet.z - self.z) < bullet.dz:
            # Check (x, y) distance at the z-plane of the target
            # Interpolate bullet position at target z
            t = (self.z - prev_z) / (bullet.z - prev_z) if bullet.z != prev_z else 0
            bx = bullet.x - bullet.dx + bullet.dx * t
            by = bullet.y - bullet.dy + bullet.dy * t
            dx = self.x - bx
            dy = self.y - by
            distance = math.sqrt(dx*dx + dy*dy)
            return distance <= self.size
        return False

def draw_shooting_range():
    """Draw the shooting range environment"""
    # Draw floor
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

def spawn_target():
    global targets
    # Random position on the back wall
    x = random.uniform(-20, 20)
    y = random.uniform(-8, 10)
    z = -39
    target_type = random.choice(TARGET_TYPES)
    target = OlympicTarget(x, y, z, target_type)
    targets.append(target)
    print(f"New target ({target_type.score} pts) at ({x:.1f}, {y:.1f})!")

def shoot():
    global bullets, mouse_x, mouse_y, window_width, window_height

    # Camera position
    cam_x, cam_y, cam_z = 0, 0, 5

    # Calculate mouse look direction (same as display)
    mouse_look_x = (mouse_x - window_width/2) * 0.005
    mouse_look_y = (mouse_y - window_height/2) * 0.005

    # Direction vector from camera to crosshair
    look_x = math.sin(mouse_look_x)
    look_y = mouse_look_y
    look_z = -math.cos(mouse_look_x)

    # Normalize direction
    length = math.sqrt(look_x**2 + look_y**2 + look_z**2)
    direction_x = look_x / length
    direction_y = look_y / length
    direction_z = look_z / length

    # Create bullet from camera position
    bullet = Bullet(cam_x, cam_y, cam_z, direction_x, direction_y, direction_z)
    bullets.append(bullet)
    print("Shot fired!")

def draw_text(text, x, y):
    """Draw text on screen"""
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def draw_crosshair():
    """Draw simple crosshair for aiming"""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST)
    glColor3f(0.0, 0.0, 0.0)  # Green crosshair
    glLineWidth(1.0)
    
    # Simple small crosshair
    size = 8
    glBegin(GL_LINES)
    glVertex2f(window_width/2 - size, window_height/2)
    glVertex2f(window_width/2 + size, window_height/2)
    glVertex2f(window_width/2, window_height/2 - size)
    glVertex2f(window_width/2, window_height/2 + size)
    glEnd()
    
    glEnable(GL_DEPTH_TEST)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_hud():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glColor3f(*WHITE)
    draw_text(f"Score: {score}", 10, window_height - 30)
    active_targets = len([t for t in targets if t.active])
    draw_text(f"Active Targets: {active_targets}", 10, window_height - 60)
    draw_text("Left Click: Shoot", 10, window_height - 100)
    # Show target types and scores
    y_offset = window_height - 130
    for tt in TARGET_TYPES:
        glColor3f(*tt.color)
        draw_text(f"{tt.score} pts", 10, y_offset)
        y_offset -= 20
    glColor3f(*WHITE)
    draw_text("Targets disappear after 8 seconds!", 10, 10)
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def update_game():
    global bullets, targets, score, game_time

    game_time += 0.016  # Roughly 60 FPS

    # Update bullets
    for bullet in bullets[:]:
        bullet.update()
        if not bullet.active:
            bullets.remove(bullet)

    # Update targets
    for target in targets[:]:
        target.update()
        if not target.active:
            targets.remove(target)

    # Check collisions and update score
    for bullet in bullets[:]:
        for target in targets[:]:
            if target.is_hit_by(bullet):
                score += target.score_value
                print(f"SCORE UPDATE! +{target.score_value} points! Total score: {score}")
                target.hit = True
                target.active = False
                bullet.active = False
                if bullet in bullets:
                    bullets.remove(bullet)
                glutPostRedisplay()
                break  # Only one target per bullet

    # Spawn new targets occasionally
    active_targets = len([t for t in targets if t.active])
    if active_targets == 0 or (game_time > 3.0 and random.random() < 0.01):
        if active_targets < 3:
            spawn_target()

def draw_icons():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

    icon_size = 40
    margin = 20
    base_x = window_width - icon_size - margin

    # Start icon (triangle)
    if not game_running:
        glColor3f(0.2, 0.8, 0.2)
        glBegin(GL_TRIANGLES)
        glVertex2f(base_x, window_height - margin - icon_size)
        glVertex2f(base_x, window_height - margin)
        glVertex2f(base_x + icon_size, window_height - margin - icon_size/2)
        glEnd()
    # Pause icon (two vertical bars)
    elif not game_paused:
        glColor3f(0.8, 0.8, 0.2)
        glBegin(GL_QUADS)
        glVertex2f(base_x, window_height - margin - icon_size)
        glVertex2f(base_x + icon_size/3, window_height - margin - icon_size)
        glVertex2f(base_x + icon_size/3, window_height - margin)
        glVertex2f(base_x, window_height - margin)
        glVertex2f(base_x + icon_size*2/3, window_height - margin - icon_size)
        glVertex2f(base_x + icon_size, window_height - margin - icon_size)
        glVertex2f(base_x + icon_size, window_height - margin)
        glVertex2f(base_x + icon_size*2/3, window_height - margin)
        glEnd()
    # Restart icon (circle with arrow)
    else:
        glColor3f(0.2, 0.6, 1.0)
        cx = base_x + icon_size/2
        cy = window_height - margin - icon_size/2
        r = icon_size/2 - 4
        glBegin(GL_LINE_LOOP)
        for i in range(24):
            angle = 2 * math.pi * i / 24
            glVertex2f(cx + r * math.cos(angle), cy + r * math.sin(angle))
        glEnd()
        # Arrow head
        glBegin(GL_TRIANGLES)
        glVertex2f(cx + r, cy)
        glVertex2f(cx + r - 10, cy + 7)
        glVertex2f(cx + r - 10, cy - 7)
        glEnd()

    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def restart_game():
    global score, bullets, targets, game_time
    score = 0
    bullets.clear()
    targets.clear()
    game_time = 0
    spawn_target()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Calculate mouse look direction
    mouse_look_x = (mouse_x - window_width/2) * 0.005
    mouse_look_y = (mouse_y - window_height/2) * 0.005

    # Camera position
    cam_x, cam_y, cam_z = 0, 0, 5

    # Camera look direction (forward, adjusted by mouse)
    look_x = cam_x + math.sin(mouse_look_x) * 10
    look_y = cam_y + mouse_look_y * 10
    look_z = cam_z - math.cos(mouse_look_x) * 10

    gluLookAt(cam_x, cam_y, cam_z,
            look_x, look_y, look_z,
            0, 1, 0)

    # Draw shooting range and targets
    draw_shooting_range()
    for target in targets:
        target.draw()

    # Draw bullets
    for bullet in bullets:
        bullet.draw()
    
    # Draw HUD
    draw_crosshair()
    draw_hud()
    draw_icons() 
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

def mouse_motion(x, y):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y
    glutPostRedisplay()

def mouse_click(button, state, x, y):
    global game_running, game_paused
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y
    
    # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
    #     shoot()

    icon_size = 40
    margin = 20
    base_x = window_width - icon_size - margin
    icon_top = window_height - margin
    icon_bottom = window_height - margin - icon_size

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Check if click is inside icon area
        if base_x <= x <= base_x + icon_size and icon_bottom <= y <= icon_top:
            if not game_running:
                game_running = True
                game_paused = False
            elif not game_paused:
                game_paused = True
            else:
                # Restart
                restart_game()
                game_running = True
                game_paused = False
            glutPostRedisplay()
            return
        # Only shoot if game is running and not paused
        if game_running and not game_paused:
            shoot()

def keyboard(key, x, y):
    if key == b'\033':  # ESC key
        print(f"Game Over! Final Score: {score}")
        sys.exit()

def timer(value):
    if game_running and not game_paused:
        update_game()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glClearColor(0.6, 0.8, 1.0, 1.0)  # Sky blue background
    
    # Spawn first target
    spawn_target()
    
    print("=== Olympic Shooting Range ===")
    print("Welcome to the Olympic shooting range!")
    print("Targets will appear randomly and disappear after 8 seconds.")
    print("Scoring: Bullseye=10, Inner=9, Red=7, Blue=5, Outer=1")
    print("Use mouse to aim, left click to shoot. Good luck!")

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Olympic Shooting Range")
    
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse_click)
    glutPassiveMotionFunc(mouse_motion)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, timer, 0)
    
    init()
    glutMainLoop()

if __name__ == "__main__":
    try:
        from OpenGL.GL import *
        from OpenGL.GLU import *
        from OpenGL.GLUT import *
    except ImportError as e:
        print("OpenGL libraries not found!")
        print("Please install: pip install PyOpenGL PyOpenGL_accelerate")
        sys.exit(1)
    
    main()