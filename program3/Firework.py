import random
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *


pygame.init()
effect = pygame.mixer.Sound('firework.wav')  # set up the sound clip


class Particle:
    def __init__(self, x=0, y=0, z=0, color=(0, 1, 0, 1), lifetime=-1, trail=False, trail_len=30):
        # position
        self.x = x
        self.y = y
        self.z = z

        # color
        self.color = color

        # lifetime
        self.lifetime = lifetime

        # if the particle as a trail and its length
        self.trail = trail
        self.trail_len = trail_len
        self.trail_list = []

        # if the particle has exploded
        self.exploded = False

        # sound to be played on explosion
        self.sound = True

        # direction the particle goes in after exploding
        self.velocity = [random.uniform(-.02, .02), random.uniform(-.02, .02), random.uniform(-.02, .02), ]

        # calculate path of a particle
        self.trajectory = [(self.x, self.y, self.z)]

    def draw(self):
        if self.lifetime != 0:
            # draw the trajectory of a particle
            if self.trail and self.exploded:  # activates printing trails after firework pops
                glLineWidth(3)
                glBegin(GL_LINE_STRIP)
                glColor4fv((self.color[0], self.color[1], self.color[2], 0.1))
                for coord in self.trail_list:
                    glVertex3fv(coord)
                glEnd()

            glEnable(GL_POINT_SMOOTH)
            glPointSize(3)
            glBegin(GL_POINTS)
            glColor4fv(self.color)
            glVertex3fv((self.x, self.y, self.z))
            self.update()
            glEnd()
            # decrease lifetime
            self.lifetime -= 1

    def update(self):
        dt = 0.06
        # causes firework to explode after hitting height of 10
        if self.y > 10:
            self.exploded = True
        # fire work has exploded
        if self.exploded:
            # play explosion sound when firework explodes
            if self.sound:  # play sounds effect
                effect.play()
                self.sound = False
            # executes if particle has a trail
            if self.trail:
                self.trail_list.append((self.x, self.y, self.z))  # adds x,y,z coord to end of list
                if len(self.trail_list) >= self.trail_len:
                    self.trail_list.pop(0)  # removes first element of list

            # decides which direction the particle goes
            self.x += self.velocity[0]
            self.y += self.velocity[1] - 0.5 * 9.8 * (dt ** 2)
            self.z += self.velocity[2]
            # if the particle floats below 0 in the y direction, it stays 0
            if self.y < 0:
                self.y = 0
        # particle travels upwards from cannon (point of origin)
        else:
            self.y += 0.1


'''======================================================'''


class Firework(Particle):
    def __init__(self, x, y, z, n, color, lifetime=-1, trail=False, trail_len=30):
        """Firework constructor class"""
        # position
        self.x = x
        self.y = y
        self.z = z

        # number of particles in firework
        self.n = n

        # color
        self.color = color

        # how long particle lives
        self.lifetime = lifetime
        self.trail = trail
        self.trail_len = trail_len

        # empty list of particles
        self.particles = []

        for i in range(n):
            # position position
            x = x
            y = 0
            z = z

            # color
            if color == 'random':
                particle_color = (random.random(), random.random(), random.random(), 1)
            else:
                particle_color = (self.color[0], self.color[1], self.color[2], self.color[3])

            # appending particle to list
            self.particles.append(Particle(x, y, z, particle_color, self.lifetime, self.trail, self.trail_len))

    def drawPath(self):
        # draw blades
        for item in self.particles:
            item.draw()
