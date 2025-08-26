from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import math

Grid_length = 60
player_rotation = 0
player_x, player_y, player_z = 0, 0, 0 
player_moving_unit, player_rotating_unit, enemie_moving_unit = 10, 5, 1

camera_pos = (400, 0, 600)
first_person = False

border_collision_count = 0
single_bullet = None
bullet_list = []
shoot_bullet = False
max_border_hits = 10
kill_count = 0

pause = False
game_over = False

enemie = [[random.randint(-550, 550),random.randint(-550, 550), 40], [random.randint(-550, 550),random.randint(-550, 550), 40],
          [random.randint(-550, 550),random.randint(-550, 550), 40], [random.randint(-550, 550),random.randint(-550, 550), 40],
          [random.randint(-550, 550),random.randint(-550, 550), 40]]

def draw_bullet_list():
    global single_bullet

    if single_bullet:
        dx, dy, dz, _, _ = single_bullet
        glPushMatrix()
        glColor3f(1, 0, 0)
        glTranslatef(dx, dy, dz)
        glutSolidSphere(15, 10, 10)
        glPopMatrix()

def respawn_enemy():
    return [random.randint(-550, 550), random.randint(-550, 550), 40]    

def enemies(enemy_x, enemy_y, enemy_z):

    glPushMatrix()
    glColor(1, 0, 0)
    glTranslatef(enemy_x, enemy_y, enemy_z)
    glutSolidSphere(40, 10, 10)
    # glPopMatrix()

    # glPushMatrix()
    glColor(0, 1, 0)
    glTranslatef(0, 0, 50)
    glutSolidSphere(20, 10, 10)
    glPopMatrix()

def borders_of_grid():

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

def make_player():
    global player_x, player_y, player_z, player_rotation

    glPushMatrix()
    glTranslatef(player_x, player_y, player_z)
    glRotatef(player_rotation, 0, 0, 1)

    
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(-20, 0, 0)  
    gluCylinder(gluNewQuadric(), 10, 15, 20, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(20, 0, 0)  
    gluCylinder(gluNewQuadric(), 10, 15, 20, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 1, 0)
    glTranslatef(0, 0, 60)
    glScalef(1.2, 0.5, 1.3)
    glutSolidCube(60)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(0, 0, 120) 
    glutSolidSphere(20, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(0, 0, 60)
    glRotatef(-90, 0, 1, 0) 
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 15, 5, 80, 10, 10)
    glPopMatrix()

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

# Add this function after the global variables
def reset_game():
    """Reset all game elements to initial state"""
    global player_x, player_y, player_z, player_rotation
    global enemie, border_collision_count, single_bullet
    global pause, shoot_bullet, game_over

    # Reset player position and rotation
    player_x, player_y, player_z = 0, 0, 0
    player_rotation = 0

    # Reset camera
    global camera_pos, fovY
    camera_pos = (400, 0, 600)
    fovY = 120

    # Reset enemies
    enemie = [
        [random.randint(-550, 550), random.randint(-550, 550), 40],
        [random.randint(-550, 550), random.randint(-550, 550), 40],
        [random.randint(-550, 550), random.randint(-550, 550), 40],
        [random.randint(-550, 550), random.randint(-550, 550), 40],
        [random.randint(-550, 550), random.randint(-550, 550), 40]
    ]

    # Reset game states
    kill_count = 0
    game_over = False
    border_collision_count = 0
    single_bullet = None
    shoot_bullet = False
    pause = False

    glutPostRedisplay()

def draw_hud():
    """Draw Heads-Up Display with game information and controls"""
    # Save current matrix
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 1000, 800, 0, -1, 1)  # 2D orthographic projection
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Text settings
    left_margin = 20
    top_margin = 40
    line_spacing = 20

    # Display game controls and information
    if not pause:
        text_lines = [
            f"Kills: {kill_count}",
            f"Missed fire: {border_collision_count}/{max_border_hits}",
            f"Direction: {player_rotation}°",
            "Controls:",
            "W - Move Forward",
            "S - Move Backward",
            "A - Rotate Left",
            "D - Rotate Right",
            "V - Toggle View",
            "Space - Pause Game",
            "R - Restart Game",
            "Left Click - Shoot"
        ]
    else:
        text_lines = [
            f"Kills: {kill_count}",
            f"Missed fire: {border_collision_count}/{max_border_hits}",
            f"Direction: {player_rotation}°",
            "V - Toggle View",
            "Space - Pause Game",
            "R - Restart Game",
            "Left Click - Shoot"
        ]

    glColor3f(1, 1, 1)  # White text color
    for i, line in enumerate(text_lines):
        glRasterPos2f(left_margin, top_margin + (i * line_spacing))
        for c in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))

    # Game over message in center if game is over
    if game_over:
        glColor3f(1, 0, 0)  # Red color
        reason = "Too many missed shots!" if border_collision_count >= max_border_hits else "Enemy collision!"
        message = f"GAME OVER - {reason} Press 'R' to restart"
        
        # Center the text
        text_width = len(message) * 9  # Approximate width of text
        x = (1000 - text_width) / 2
        y = 400
        
        glRasterPos2f(x, y)
        for c in message:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))

    # Restore matrices
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

# Modify the camera_setup function
def camera_setup():
    global camera_pos, first_person, player_x, player_y, player_z, player_rotation

    if first_person:
        fovY = 150
    else: 
        fovY = 120

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1000/800, 1, 5000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if first_person:
        # Calculate camera position and look-at point for first person view
        angle_rad = math.radians(player_rotation)
        # Position camera at player's head but slightly higher and back
        camera_x = player_x - 20 * math.sin(angle_rad)  # Move camera back a bit
        camera_y = player_y - 20 * math.cos(angle_rad)
        camera_z = player_z + 100  # Lower camera height to see gun

        # Calculate look-at point (where the player is facing)
        look_x = camera_x - 100 * math.sin(angle_rad)
        look_y = camera_y - 100 * math.cos(angle_rad)
        look_z = camera_z

        gluLookAt(camera_x, camera_y, camera_z,
                  look_x, look_y, look_z,
                  0, 0, 1)
    else:
        # Third person view (original top-down view)
        x, y, z = camera_pos
        gluLookAt(x, y, z,
                  0, 0, 0,
                  0, 0, 1)

def display():
    global enemie, first_person

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

    if not first_person: 
        make_player()

    # glColor3f(1, 1, 1)
    # glRasterPos2f(450, 550)
    # for c in f"Border Hits: {border_collision_count}":
    #     glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
   
    for i in enemie:
        x, y, z = i
        enemies(x, y, z)

    draw_bullet_list()

    # Draw HUD on top of 3D scene
    draw_hud()

    glutSwapBuffers()

def keyborad_listener(key, x, y):
    global player_x, player_y, player_z, pause, player_moving_unit, player_rotation, player_rotation, player_rotating_unit
    global game_over, first_person

    if key == b'v':  # 'v' key to toggle view
        first_person = not first_person
        if first_person:
            fovY = 90  # Better FOV for first person
        else:
            fovY = 120  # Original FOV for third person
        glutPostRedisplay()
        return    

    angle_rad = math.radians(player_rotation)

    # Calculate movement direction based on rotation
    dx = math.cos(angle_rad) * player_moving_unit
    dy = math.sin(angle_rad) * player_moving_unit

    strafe_dx = math.cos(angle_rad + math.pi / 2) * player_moving_unit
    strafe_dy = math.sin(angle_rad + math.pi / 2) * player_moving_unit

    if key == b' ':
        pause = not pause

    if key == b'w':
        new_x = player_x - strafe_dx
        new_y = player_y - strafe_dy
        if -550 <= new_x <= 550 and -550 <= new_y <= 550:  # Check grid boundaries
            player_x = new_x
            player_y = new_y
    elif key == b's': 
        new_x = player_x + strafe_dx
        new_y = player_y + strafe_dy
        if -550 <= new_x <= 550 and -550 <= new_y <= 550:  # Check grid boundaries
            player_x = new_x
            player_y = new_y

    if key == b'a':
        player_rotation = (player_rotation + player_rotating_unit) % 360    
    elif key == b'd':
        player_rotation = (player_rotation - player_rotating_unit) % 360 


    if key == b'f':
        fpps = True
        player_y = 60
        fovY = 90
        camera_pos = (player_x, player_y, player_z+ 65)

    if key  == b't':
        fovY = 120
        camera_pos = (0, 400, 500)

    if key == b'r' or key == b'R':  # Allow both upper and lowercase 'r'
        reset_game()
        return
    
    if game_over:
        return

    glutPostRedisplay()

def special_key_listener(key, x, y):
    global player_rotation, player_rotating_unit
    if key == GLUT_KEY_RIGHT:
        player_rotation = (player_rotation - player_rotating_unit) % 360

    if key == GLUT_KEY_LEFT:
        player_rotation = (player_rotation + player_rotating_unit) % 360
    

    glutPostRedisplay()

def mouse_listener(button, state, x, y):
    global shoot_bullet

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            shoot_bullet = True
        else:
            shoot_bullet = False

def animation():
    global enemie, enemie_moving_unit, player_x, player_y, shoot_bullet, bullet_list
    global single_bullet, border_collision_count, pause, game_over, max_border_hits, kill_count

    if game_over:
        glutPostRedisplay()  # Keep refreshing display for game over text
        return
                # Check for collision between player and enemies
    player_radius = 40  # Approximate player size
    for enemy in enemie:
        ex, ey, ez = enemy
        dx = player_x - ex
        dy = player_y - ey
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < (player_radius):  # 40 is enemy radius
            game_over = True
            glutPostRedisplay()
            return
    if pause:       
        for i in range(len(enemie)):
            ex, ey, ez = enemie[i]

            # Direction vector towards player
            dx = player_x - ex
            dy = player_y - ey

            # Distance to normalize
            dist = math.sqrt(dx*dx + dy*dy)

            if dist > 0:  # prevent divide by zero
                dx /= dist
                dy /= dist

            # Move enemy a little step toward player
            ex += (dx * enemie_moving_unit) * 0.1
            ey += (dy * enemie_moving_unit) * 0.1

            # Save new position
            enemie[i] = [ex, ey, ez]

   
        # Fire a bullet if shoot_bullet is True
    if shoot_bullet and single_bullet is None:
        # Calculate bullet starting position from the gun barrel
        angle_rad = math.radians(player_rotation)
        # Position bullet at the end of the gun barrel
        start_x = player_x + 80 * math.cos(angle_rad - math.pi/2)
        start_y = player_y + 80 * math.sin(angle_rad - math.pi/2)
        bullet_dx = math.cos(angle_rad - math.pi/2) * 20  # Bullet speed
        bullet_dy = math.sin(angle_rad - math.pi/2) * 20
        single_bullet = [start_x, start_y, player_z + 60, bullet_dx, bullet_dy]

    # Update bullet position
    if single_bullet:
        single_bullet[0] += single_bullet[3]  # Update x position
        single_bullet[1] += single_bullet[4]  # Update y position

        # Check collision with enemies
        for i, enemy in enumerate(enemie):
            ex, ey, ez = enemy
            dx = (single_bullet[0] - ex) * 0.5
            dy = (single_bullet[1] - ey) 
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < 40:  # Enemy radius is 40
                # enemie.pop(i)
                # if len(enemie) <= 4: 
                kill_count += 1
                enemie[i] = respawn_enemy()  # Remove hit enemy
                single_bullet = None  # Remove bullet
                break

        # Check collision with borders
        if single_bullet:
            x, y = single_bullet[0], single_bullet[1]
            if abs(x) >= 600 or abs(y) >= 600:
                border_collision_count += 1
                single_bullet = None

                if border_collision_count >= max_border_hits:
                    game_over = True
                    return

    glutPostRedisplay()

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
glutKeyboardFunc(keyborad_listener)
glutMouseFunc(mouse_listener)
# glutSpecialFunc(special_key_listener)
glutIdleFunc(animation)

glutMainLoop()