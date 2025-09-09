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
            if self.z < -35 or abs(self.x) > 25 or abs(self.y) > 15:
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

class OlympicTarget:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.active = True
        self.spawn_time = time.time()
        self.lifetime = 8.0  # Target stays for 8 seconds
        self.size = 2.0
        self.hit = False
        
    def update(self):
        # Check if target should disappear
        if time.time() - self.spawn_time > self.lifetime:
            self.active = False
            if not self.hit:
                print("Target disappeared! No points.")
    
    def draw(self):
        if self.active:
            glPushMatrix()
            glTranslatef(self.x, self.y, self.z)
            
            # Draw target backing (white circle)
            glColor3f(*WHITE)
            self.draw_filled_circle(self.size)
            
            # Draw scoring rings from outside to inside
            # Outer ring (1 point) - Black
            glColor3f(*BLACK)
            self.draw_ring(self.size * 0.9, self.size)
            
            # Second ring (5 points) - Blue  
            glColor3f(*BLUE)
            self.draw_ring(self.size * 0.7, self.size * 0.9)
            
            # Third ring (7 points) - Red
            glColor3f(*RED)
            self.draw_ring(self.size * 0.5, self.size * 0.7)
            
            # Inner ring (9 points) - Gold/Yellow
            glColor3f(1.0, 0.8, 0.0)
            self.draw_ring(self.size * 0.3, self.size * 0.5)
            
            # Bullseye (10 points) - Black center
            glColor3f(*BLACK)
            self.draw_filled_circle(self.size * 0.3)
            
            # Draw target frame
            glColor3f(*BLACK)
            glLineWidth(3.0)
            self.draw_circle_outline(self.size)
            glLineWidth(1.0)
            
            glPopMatrix()
    
    def draw_filled_circle(self, radius):
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, 0)
        for i in range(33):  # 32 segments + 1 to close
            angle = 2.0 * math.pi * i / 32
            glVertex3f(radius * math.cos(angle), radius * math.sin(angle), 0)
        glEnd()
    
    def draw_ring(self, inner_radius, outer_radius):
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(33):  # 32 segments + 1 to close
            angle = 2.0 * math.pi * i / 32
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            # Outer vertex
            glVertex3f(outer_radius * cos_a, outer_radius * sin_a, 0)
            # Inner vertex
            glVertex3f(inner_radius * cos_a, inner_radius * sin_a, 0)
        glEnd()
    
    def draw_circle_outline(self, radius):
        glBegin(GL_LINE_LOOP)
        for i in range(32):
            angle = 2.0 * math.pi * i / 32
            glVertex3f(radius * math.cos(angle), radius * math.sin(angle), 0)
        glEnd()
    
    def check_collision(self, bullet):
        if not self.active or not bullet.active or self.hit:
            return 0
        
        # Calculate distance from bullet to target center
        distance = math.sqrt((self.x - bullet.x)**2 + (self.y - bullet.y)**2)
        
        # Check if bullet is close enough in Z direction
        if abs(self.z - bullet.z) > 0.3:
            return 0
        
        # Check which ring was hit and return score
        if distance <= self.size * 0.3:  # Bullseye
            self.hit = True
            bullet.active = False
            return 10
        elif distance <= self.size * 0.5:  # Inner ring
            self.hit = True
            bullet.active = False
            return 9
        elif distance <= self.size * 0.7:  # Third ring
            self.hit = True
            bullet.active = False
            return 7
        elif distance <= self.size * 0.9:  # Second ring
            self.hit = True
            bullet.active = False
            return 5
        elif distance <= self.size:  # Outer ring
            self.hit = True
            bullet.active = False
            return 1
        
        return 0

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
    """Spawn a new target at random position"""
    global targets
    
    # Random position on the back wall
    x = random.uniform(-20, 20)
    y = random.uniform(-8, 10)
    z = -39  # Just in front of back wall
    
    target = OlympicTarget(x, y, z)
    targets.append(target)
    print(f"New target appeared at ({x:.1f}, {y:.1f})! Shoot it before it disappears!")

def shoot():
    global bullets, mouse_x, mouse_y, window_width, window_height
    
    # Convert mouse position to world coordinates
    norm_x = (2.0 * mouse_x / window_width) - 1.0
    norm_y = 1.0 - (2.0 * mouse_y / window_height)
    
    # Calculate shooting direction from shooting position
    direction_x = norm_x * 0.8
    direction_y = norm_y * 0.8
    direction_z = -1.0
    
    # Normalize direction
    length = math.sqrt(direction_x**2 + direction_y**2 + direction_z**2)
    direction_x /= length
    direction_y /= length
    direction_z /= length
    
    # Create bullet from shooting position
    bullet = Bullet(0, -1, 3, direction_x, direction_y, direction_z)
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
    glColor3f(0.0, 1.0, 0.0)  # Green crosshair
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
    """Draw game HUD"""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST)
    glColor3f(*WHITE)
    
    # Score
    draw_text(f"Score: {score}", 10, window_height - 30)
    
    # Active targets
    active_targets = len([t for t in targets if t.active])
    draw_text(f"Active Targets: {active_targets}", 10, window_height - 60)
    
    # Instructions
    draw_text("Left Click: Shoot", 10, window_height - 100)
    draw_text("Bullseye=10pts, Inner=9pts, Red=7pts, Blue=5pts, Outer=1pt", 10, 30)
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
    
    # Check collisions with detailed logging
    for bullet in bullets:
        for target in targets:
            points = target.check_collision(bullet)
            if points > 0:
                score += points
                print(f"SCORE UPDATE! +{points} points! Total score: {score}")
                break
    
    # Spawn new targets occasionally
    active_targets = len([t for t in targets if t.active])
    if active_targets == 0 or (game_time > 3.0 and random.random() < 0.01):  # 1% chance per frame after 3 seconds
        if active_targets < 3:  # Max 3 targets at once
            spawn_target()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Position camera at shooting position
    gluLookAt(0, 0, 5,      # Camera at shooting booth
              0, 0, -10,    # Looking down range
              0, 1, 0)      # Up vector
    
    # Apply slight mouse look for aiming
    mouse_look_x = (mouse_x - window_width/2) * 0.005
    mouse_look_y = (mouse_y - window_height/2) * 0.005
    glRotatef(mouse_look_y * 5, 1, 0, 0)
    glRotatef(mouse_look_x * 5, 0, 1, 0)
    
    # Draw shooting range
    draw_shooting_range()
    
    # Draw targets
    for target in targets:
        target.draw()
    
    # Draw bullets
    for bullet in bullets:
        bullet.draw()
    
    # Draw HUD
    draw_crosshair()
    draw_hud()
    
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
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        shoot()

def keyboard(key, x, y):
    if key == b'\033':  # ESC key
        print(f"Game Over! Final Score: {score}")
        sys.exit()

def timer(value):
    update_game()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)  # ~60 FPS

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glClearColor(0.6, 0.8, 1.0, 1.0)  # Sky blue background
    
    # Spawn first target
    spawn_target()
    
    print("=== Sphere Target Shooting Range ===")
    print("Welcome to the shooting range!")
    print("Targets are colored spheres with different sizes and points:")
    print("- RED (Large): 5 points - Easy to hit")
    print("- BLUE (Medium): 10 points - Medium difficulty") 
    print("- GREEN (Small): 20 points - Hard to hit, highest score!")
    print("Targets disappear after 8 seconds. Use mouse to aim, left click to shoot!")
    print("Good luck!")

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