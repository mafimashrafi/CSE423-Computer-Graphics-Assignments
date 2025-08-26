from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import math

Grid_length = 60
player_rotation = 0
fpps = False
player_x, player_y, player_z = 0, 0, 0 
player_moving_unit, player_rotating_unit, enemie_moving_unit = 10, 10, 1
camera_pos = (400, 0, 600)
fovY = 120
border_collision_count = 0
single_bullet = None
bullet_list = []
shoot_bullet = False
pause = True

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
    make_player()

    # glColor3f(1, 1, 1)
    # glRasterPos2f(450, 550)
    # for c in f"Border Hits: {border_collision_count}":
    #     glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    for i in enemie:
        x, y, z = i
        enemies(x, y, z)

    draw_bullet_list()
        
    glutSwapBuffers()

def keyborad_listener(key, x, y):
    global player_x, player_y, player_z, pause, player_moving_unit, player_rotation, player_rotation, player_rotating_unit

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
        fovY = 150
        camera_pos = (player_x, player_y, player_z+ 65)

    if key  == b't':
        fovY = 120
        camera_pos = (0, 400, 500)

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
    global single_bullet, border_collision_count, pause


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
        ex += dx * enemie_moving_unit
        ey += dy * enemie_moving_unit

        # Save new position
        enemie[i] = [ex, ey, ez]

    if not pause:
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
                dx = single_bullet[0] - ex
                dy = single_bullet[1] - ey
                dist = math.sqrt(dx*dx + dy*dy)
                
                if dist < 40:  # Enemy radius is 40
                    enemie.pop(i)  # Remove hit enemy
                    single_bullet = None  # Remove bullet
                    break

            # Check collision with borders
            if single_bullet:
                x, y = single_bullet[0], single_bullet[1]
                if abs(x) >= 600 or abs(y) >= 600:
                    border_collision_count += 1
                    single_bullet = None

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