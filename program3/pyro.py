import random
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from Firework import Firework, Particle


def terrain():
    ''' Draws a simple square as the terrain '''
    glBegin(GL_QUADS)
    glColor4fv((0, 0, 1, 1))  # Colors are now: RGBA, A = alpha for opacity
    glVertex3fv((10, 0, 10))  # These are the xyz coords of 4 corners of flat terrain.
    glVertex3fv((-10, 0, 10))  # If you want to be fancy, you can replace this method
    glVertex3fv((-10, 0, -10))  # to draw the terrain from your prog1 instead.
    glVertex3fv((10, 0, -10))
    glEnd()


def main():
    pygame.init()

    # Set up the screen
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Firework Simulation")
    glEnable(GL_DEPTH_TEST)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0, -5, -25)
    # glRotatef(10, 2, 1, 0)

    play = True
    sim_time = 0

    # A clock object for keeping track of fps
    clock = pygame.time.Clock()

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glRotatef(-10, 0, 1, 0)
                if event.key == pygame.K_RIGHT:
                    glRotatef(10, 0, 1, 0)

                if event.key == pygame.K_UP:
                    glRotatef(-10, 1, 0, 0)
                if event.key == pygame.K_DOWN:
                    glRotatef(10, 1, 0, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 1.0)

                if event.button == 5:
                    glTranslatef(0, 0, -1.0)

        glRotatef(0.10, 0, 1, 0)
        # glTranslatef(0, 0.1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        terrain()

        if 0 < sim_time <= 1000:
            f1.drawPath()
        if 500 < sim_time <= 1500:
            f2.drawPath()
            f3.drawPath()
        if 1000 < sim_time <= 1500:
            f4.drawPath()
            f5.drawPath()
        if 1500 < sim_time:
            sim_time = 0

        if sim_time == 0:
            """ This is where the fireworks are initialized. Changing the n changes the amount of particles
                per firework. Color changes the color of all the particles in the firework; entering 'random'
                will choose a random color for every particle instead of one random color for all the particles.
                Lifetime changes how long the particle lives for, you generally want a lifetime above 120 or
                else the firework wont explode (I recommend around 400). For no lifetime, enter -1."""

            # firework 1: random, 100 count w/ trails
            n = 100
            f1_color = 'random'         # use (random.random(), random.random(), random.random(), 1) for random 1 color
            f1_lifetime = 400
            f1_trail = True
            f1_trail_len = 10
            f1 = Firework(0, 0, 0, n, f1_color, f1_lifetime, f1_trail, f1_trail_len)

            # firework 2: red, 250 count, shorter life
            n = 175
            f2_color = (1, 0, 0, 1)
            f2_lifetime = 310
            f2 = Firework(-5, 0, 5, n, f2_color, f2_lifetime)

            # firework 3: random color, 100 count, trails
            n = 100
            f3_color = 'random'         # use (random.random(), random.random(), random.random(), 1) for random 1 color
            f3_lifetime = 400
            f3_trail = True
            f3_trail_len = 20
            f3 = Firework(-5, 0, -5, n, f3_color, f3_lifetime, f3_trail, f3_trail_len)

            # firework 4: green, 150 count, trails
            n = 150
            f4_color = (0, 1, 0, 1)
            f4_lifetime = 400
            f4_trail = True
            f4_trail_len = 20
            f4 = Firework(5, 0, -5, n, f4_color, f4_lifetime, f4_trail, f4_trail_len)

            # firework 5: random colors, 100 count, long lifetime
            n = 100
            f5_color = 'random'         # use (random.random(), random.random(), random.random(), 1) for random 1 color
            f5_lifetime = 600
            f5_trail = False
            f5_trail_len = 0
            f5 = Firework(5, 0, 5, n, f5_color, f5_lifetime, f5_trail, f5_trail_len, )

        pygame.display.flip()
        sim_time += 1
        clock.tick(150)

    pygame.quit()


if __name__ == "__main__":
    main()