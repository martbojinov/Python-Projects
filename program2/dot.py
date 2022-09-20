# Dot class
############################################################################
#  This is where I define my Dot class. The dot class is used for storing  #
#  and displaying the location and state of dots. These dots are meant to  #
#  represent people during the COVID-19 pandemic.                          #
#                                                                          #
#  Author:  Martin Bojinov                                                 #
#  References:  https://www.pygame.org/docs/ref/sprite.html                #
############################################################################

import pygame


class Dot(pygame.sprite.Sprite):
    """ made this be a subclass of Sprite """

    count = 0  # number of dots in population

    def __init__(self, imgfile, size, start=(0, 0), end=(0, 0), sd6=1, sip=0):
        """ Constructor of the class """

        super().__init__()

        self.size = size  # initialized for image calculations
        self.start = start  # starting position of dot
        self.gps = start  # position along the line, begins at the start
        self.goal = end  # end position of dot
        self.sd6 = sd6  # whether or not the dot follows SD6 orders (0 = does not follow, 1 = follows)
        self.sip = sip  # whether or not the dot follows Shelter in place orders (0 = does not follow, 1 = follows)

        if sd6 == 0:
            self.size = self.size // 3

        # initializes the image that will be used to represent the dot
        self.srf = pygame.Surface((32, 32))
        self.img = pygame.image.load(imgfile).convert()
        self.image = pygame.transform.scale(self.img, (self.size, self.size))

        self.radius = size / 2  # to use collide circle

        # initialize the rectangle used for collision and move it to the location of the dot
        self.rect = self.image.get_rect()
        self.rect.x = self.gps[0]
        self.rect.y = self.gps[1]

        # counters used for calculations
        self.dx_counter = 0  # dx and dy counters used for calculating progress to goal and swapping goal and start
        self.dy_counter = 0
        self.day_counter = 0  # day counter used for calculations that involve swapping between groups

    def update(self):
        """ Moves the dot in a straight line from its starting point through the end point """

        dx = self.goal[0] - self.start[0]  # the line which the dot follows on the x-axis
        nx = round(self.gps[0] + 0.02 * dx)

        dy = self.goal[1] - self.start[1]  # the line which the dot follows on the y-axis
        ny = round(self.gps[1] + 0.02 * dy)

        self.gps = (int(nx), int(ny))  # change coordinates to new coordinates that are 2% further on the line

        # A progress counter for the distance of the dot on its line; rounding so that the equation works
        self.dx_counter += round(0.02 * dx, 2)
        self.dy_counter += round(0.02 * dy, 2)
        self.dx_counter = round(self.dx_counter, 2)
        self.dy_counter = round(self.dy_counter, 2)
        # print(self.dx_counter, self.dy_counter, dx, dy)

        # When the dot reaches its destination, its goal and start swap; causes dot to move back and forth
        if self.dx_counter == dx and self.dy_counter == dy:
            self.start, self.goal = self.goal, self.start
            self.dx_counter = 0
            self.dy_counter = 0

        # update the position of the sprite for when it is drawn
        self.rect.x = self.gps[0]
        self.rect.y = self.gps[1]
