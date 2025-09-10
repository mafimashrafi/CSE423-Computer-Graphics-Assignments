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
miss_target = 0
miss_hit = 0

# Colors for Olympic-style targets
WHITE = (1.0, 1.0, 1.0)
BLACK = (0.0, 0.0, 0.0)
RED = (1.0, 0.0, 0.0)
BLUE = (0.0, 0.0, 1.0)
YELLOW = (1.0, 1.0, 0.0)
GREEN = (0.0, 1.0, 0.0)
BROWN = (0.6, 0.3, 0.1)
GRAY = (0.5, 0.5, 0.5)
CYAN = (0.0, 1.0, 1.0)

# ==== Helpers for new targets ====
def draw_filled_triangle(side_len):
    # Equilateral triangle centered at (0,0)
    h = (math.sqrt(3) / 2.0) * side_len
    glBegin(GL_TRIANGLES)
    glVertex3f(-side_len / 2.0, -h / 3.0, 0)
    glVertex3f(side_len / 2.0, -h / 3.0, 0)
    glVertex3f(0.0, 2.0 * h / 3.0, 0)
    glEnd()

def draw_explosion(radius, spokes=12):
    # Quick starburst lines
    glLineWidth(2.0)
    glBegin(GL_LINES)
    for i in range(spokes):
        ang = (2.0 * math.pi * i) / spokes
        glVertex3f(0, 0, 0)
        glVertex3f(radius * math.cos(ang), radius * math.sin(ang), 0)
    glEnd()
    glLineWidth(1.0)
# =================================

game_running = False
game_paused = False
game_over = True
max_score = -math.inf


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
    TargetType((1.0, 1.0, 0.0), 1.2, 15),   # Yellow, very small, highest score (among circles)
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
        global miss_target, game_over, game_running, max_score, score, miss_hit
        if time.time() - self.spawn_time > self.lifetime:
            self.active = False
            if not self.hit:
                miss_target += 1
                miss_hit += 1
                print("Target disappeared! No points.")
                if miss_target >= 3 or miss_hit >= 5:
                    game_over = True
                    game_running = False
                    if score > max_score:
                        max_score = score

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
        if (prev_z > self.z and bullet.z <= self.z) or abs(bullet.z - self.z) < abs(bullet.dz):
            # Interpolate bullet position at target z
            denom = (bullet.z - prev_z)
            t = (self.z - prev_z) / denom if denom != 0 else 0
            bx = bullet.x - bullet.dx + bullet.dx * t
            by = bullet.y - bullet.dy + bullet.dy * t
            dx = self.x - bx
            dy = self.y - by
            distance = math.sqrt(dx * dx + dy * dy)
            return distance <= self.size
        return False


# ==== Triangle (high points) and Bomb (hazard) targets ====
class TriangleTarget(OlympicTarget):
    def __init__(self, x, y, z, size=2.6, color=(1.0, 0.5, 0.0), score=20):
        super().__init__(x, y, z, TargetType(color, size, score))

    def draw(self):
        if self.active:
            glPushMatrix()
            glTranslatef(self.x, self.y, self.z)
            glColor3f(*self.color)
            # Use size as side length
            draw_filled_triangle(self.size)
            glPopMatrix()


class BombTarget(OlympicTarget):
    def __init__(self, x, y, z, size=2.2):
        super().__init__(x, y, z, TargetType(GRAY, size, -15))
        self.lifetime = 7.0
        self.exploding = False
        self.explode_start = 0.0

    def draw(self):
        # Draw either the bomb or its brief explosion after being hit
        if not self.active and not self.exploding:
            return

        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)

        if self.exploding:
            t = time.time() - self.explode_start
            glColor3f(1.0, 0.5, 0.0)
            draw_explosion(self.size * (1.0 + 2.0 * t), spokes=14)
            glPopMatrix()
            if t > 0.35:
                self.exploding = False
            return

        # Bomb body
        glColor3f(0.15, 0.15, 0.15)
        self.draw_filled_circle(self.size * 0.9)

        # Fuse
        glColor3f(0.9, 0.8, 0.2)
        glBegin(GL_LINES)
        glVertex3f(self.size * 0.35, self.size * 0.35, 0)
        glVertex3f(self.size * 0.75, self.size * 0.75, 0)
        glEnd()

        # Spark at the tip
        glPointSize(3.0)
        glBegin(GL_POINTS)
        glVertex3f(self.size * 0.75, self.size * 0.75, 0)
        glEnd()

        glPopMatrix()

    def on_hit(self):
        self.exploding = True
        self.explode_start = time.time()


# ==== NEW: Moving target (oscillates horizontally or vertically) ====
class MovingTarget(OlympicTarget):
    def __init__(self, x, y, z, axis='x', amplitude=6.0, frequency=0.6, size=2.4, color=CYAN, score=12):
        super().__init__(x, y, z, TargetType(color, size, score))
        self.axis = axis  # 'x' or 'y'
        self.origin_x = x
        self.origin_y = y
        self.amplitude = amplitude
        self.frequency = frequency  # cycles per second
        self.lifetime = 9.0  # a little longer since it's harder

    def update(self):
        # Move in a smooth sine wave based on time since spawn, then apply normal expiry rules
        t = time.time() - self.spawn_time
        offset = self.amplitude * math.sin(2.0 * math.pi * self.frequency * t)
        if self.axis == 'x':
            self.x = self.origin_x + offset
        else:
            self.y = self.origin_y + offset
        super().update()
# ===================================================================


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
    """Spawn circles, triangles, bombs, or moving targets with weighted randomness."""
    global targets
    # Random position on the back wall
    x = random.uniform(-20, 20)
    y = random.uniform(-8, 10)
    z = -39

    roll = random.random()
    if roll < 0.12:
        # ~12% chance: Bomb
        t = BombTarget(x, y, z, size=random.uniform(1.8, 2.6))
        print(f"Bomb spawned at ({x:.1f}, {y:.1f})! Avoid it!")
    elif roll < 0.32:
        # Next 20%: Triangle (high-value)
        t = TriangleTarget(x, y, z, size=random.uniform(2.2, 3.0))
        print(f"Triangle target (+{t.score_value} pts) at ({x:.1f}, {y:.1f})!")
    elif roll < 0.47:
        # Next 15%: Moving target (horizontal or vertical)
        axis = 'x' if random.random() < 0.6 else 'y'
        amp = random.uniform(4.0, 8.0)
        freq = random.uniform(0.4, 0.8)
        t = MovingTarget(x, y, z, axis=axis, amplitude=amp, frequency=freq, size=random.uniform(2.2, 2.8))
        axis_name = "H" if axis == 'x' else "V"
        print(f"Moving target {axis_name}-axis (+{t.score_value} pts) at ({x:.1f}, {y:.1f})!")
    else:
        # Otherwise: existing circular types
        target_type = random.choice(TARGET_TYPES)
        t = OlympicTarget(x, y, z, target_type)
        print(f"New target ({target_type.score} pts) at ({x:.1f}, {y:.1f})!")

    targets.append(t)


def shoot():
    global bullets, mouse_x, mouse_y, window_width, window_height

    # Camera position
    cam_x, cam_y, cam_z = 0, 0, 5

    # Calculate mouse look direction (same as display)
    mouse_look_x = (mouse_x - window_width / 2) * 0.005
    mouse_look_y = (mouse_y - window_height / 2) * 0.005

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
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(1.0)

    size = 8
    glBegin(GL_LINES)
    glVertex2f(window_width / 2 - size, window_height / 2)
    glVertex2f(window_width / 2 + size, window_height / 2)
    glVertex2f(window_width / 2, window_height / 2 - size)
    glVertex2f(window_width / 2, window_height / 2 + size)
    glEnd()

    glEnable(GL_DEPTH_TEST)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_text_3d(text, x, y):
    """Draw text at a 3D position on a wall (x, y are offsets in wall space)"""
    glRasterPos3f(x, y, 0)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def draw_hud():
    global game_paused, game_running, max_score
    glDisable(GL_DEPTH_TEST)

    # --- Score on the back wall (top center) ---
    glColor3f(*WHITE)
    glPushMatrix()
    glTranslatef(0, 13.5, -39)  # Center top of back wall
    draw_text_3d(f"Score: {score}", 0, 0)
    if game_paused:
        draw_text_3d("PAUSED", 0, -5)
    if not game_over:
        glColor3f(*RED)
        glTranslatef(-7, 12, -39)
        draw_text_3d("Game Over: Press TAB Start", -6, -3)
    glColor3f(*RED)
    glTranslatef(0, 15, 30)
    draw_text_3d(f"Max Score: {max_score}", 0, 0)
    draw_text_3d("You Might Break Your NECK", -3, -3)
    draw_text_3d("Look Downard", 0, -6)
    glPopMatrix()

    # --- Left wall HUD (in world coordinates) ---
    glColor3f(*WHITE)
    glPushMatrix()
    glTranslatef(-29.5, 10, -20)  # Near top of left wall
    glRotatef(90, 0, 1, 0)        # Face toward the range
    draw_text_3d(f"Points: {score}", 0, 0)
    active_targets = len([t for t in targets if t.active])
    draw_text_3d(f"Active Targets: {active_targets}", 0, -2)
    draw_text_3d("Target types:", 0, -4)
    y_offset = -6
    for tt in TARGET_TYPES:
        glColor3f(*tt.color)
        draw_text_3d(f"{tt.score} pts", 0, y_offset)
        y_offset -= 2

    # Legend for new targets
    glColor3f(1.0, 0.5, 0.0)
    draw_text_3d("Triangle: 20 pts", 0, y_offset); y_offset -= 2

    glColor3f(*GRAY)
    draw_text_3d("Bomb: -15 pts", 0, y_offset); y_offset -= 2

    glColor3f(*CYAN)
    draw_text_3d("Moving: 12 pts", 0, y_offset); y_offset -= 2
    glColor3f(*WHITE)

    glPopMatrix()

    # --- Right wall HUD (in world coordinates) ---
    glColor3f(*WHITE)
    glPushMatrix()
    glTranslatef(29.5, 10, -20)   # Near top of right wall
    glRotatef(-90, 0, 1, 0)       # Face toward the range
    draw_text_3d("Space: Play/Pause", 0, 0)
    draw_text_3d("Tab: Restart", 0, -2)
    draw_text_3d("ESC: Quit", 0, -4)
    draw_text_3d("Left Click: Shoot", 0, -6)
    status = "Paused" if game_paused else ("Running" if game_running else "Stopped")
    draw_text_3d(f"Game Status: {status}", 0, -8)
    glPopMatrix()

    glEnable(GL_DEPTH_TEST)


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
        if not target.active and not getattr(target, "exploding", False):
            # Remove only if not in explosion phase
            targets.remove(target)

    # Check collisions and update score
    for bullet in bullets[:]:
        for target in targets[:]:
            if target.is_hit_by(bullet):
                target.hit = True
                bullet.active = False
                if bullet in bullets:
                    bullets.remove(bullet)

                # Apply scoring (bombs negative)
                score += target.score_value
                if isinstance(target, BombTarget):
                    target.on_hit()
                    target.active = False  # stop being a hittable target
                    print(f"BOOM! -{abs(target.score_value)} points. Total score: {score}")
                else:
                    target.active = False
                    print(f"SCORE UPDATE! +{target.score_value} points! Total score: {score}")

                glutPostRedisplay()
                break  # Only one target per bullet

    # Spawn new targets occasionally
    active_targets = len([t for t in targets if t.active])
    if active_targets == 0 or (game_time > 3.0 and random.random() < 0.01):
        if active_targets < 3:
            spawn_target()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Calculate mouse look direction
    mouse_look_x = (mouse_x - window_width / 2) * 0.005
    mouse_look_y = (mouse_y - window_height / 2) * 0.005

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
    global mouse_x, mouse_y, game_running
    if game_running:
        mouse_x = x
        mouse_y = y

        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            shoot()


def keyboard(key, x, y):
    global game_running, game_paused, score, bullets, targets, game_time, game_over
    global max_score

    if key == b'\033':  # ESC
        glutDestroyWindow(glutGetWindow())
        sys.exit(0)

    if game_over:
        if key == b' ':  # Space bar toggles play/pause (only when game_over True per your logic)
            if game_running:
                game_paused = not game_paused
                print("Paused" if game_paused else "Resumed")
            else:
                game_running = True
                game_paused = False
                print("Game Started")

    if key == b'\t':   # Tab key restarts the game
        if max_score < score:
            max_score = score
        game_over = True
        score = 0
        bullets.clear()
        targets.clear()
        game_time = 0
        # Reset misses when restarting
        globals()['miss_target'] = 0
        globals()['miss_hit'] = 0
        game_running = False
        game_paused = False
        spawn_target()
        print("Game Restarted")
        glutPostRedisplay()


def timer(value):
    if game_running and not game_paused:
        update_game()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)  # ~60 FPS


def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glClearColor(0.6, 0.8, 1.0, 1.0)  # Sky blue background

    if game_running and game_over:
        spawn_target()

    print("=== Olympic Shooting Range ===")
    print("Welcome to the Olympic shooting range!")
    print("Targets will appear randomly and disappear after 8 seconds.")
    print("Scoring: Bullseye=10, Inner=9, Red=7, Blue=5, Outer=1")
    print("Use mouse to aim, left click to shoot. Good luck!")
    print("NEW: Triangle +20, Moving +12, Bomb -15 (avoid!)")


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
