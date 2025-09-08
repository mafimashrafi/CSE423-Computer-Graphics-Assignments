def draw_crosshair():
#     """Draw simple crosshair for aiming"""
#     glMatrixMode(GL_PROJECTION)
#     glPushMatrix()
#     glLoadIdentity()
#     gluOrtho2D(0, window_width, 0, window_height)
    
#     glMatrixMode(GL_MODELVIEW)
#     glPushMatrix()
#     glLoadIdentity()
    
#     glDisable(GL_DEPTH_TEST)
#     glColor3f(0.0, 1.0, 0.0)  # Green crosshair
#     glLineWidth(1.0)
    
#     # Simple small crosshair
#     size = 8
#     glBegin(GL_LINES)
#     glVertex2f(window_width/2 - size, window_height/2)
#     glVertex2f(window_width/2 + size, window_height/2)
#     glVertex2f(window_width/2, window_height/2 - size)
#     glVertex2f(window_width/2, window_height/2 + size)
#     glEnd()
    
#     glEnable(GL_DEPTH_TEST)
    
#     glPopMatrix()
#     glMatrixMode(GL_PROJECTION)
#     glPopMatrix()
#     glMatrixMode(GL_MODELVIEW)