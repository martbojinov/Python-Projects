# covid scenario 1
############################################################################
#  This is where I display the dots and have them interact with each       #
#  other. Scenario 1 requires bubbles around dots so that they get sick    #
#  when breaking social distancing of six feet.                            #
#                                                                          #
#  Author:  Martin Bojinov                                                 #
#  References:  https://www.pygame.org/docs/ref/sprite.html                #
############################################################################

import pygame  # Import and initialize the pygame library
import random  # import random library to create random points
import dot  # imports the required dot class

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                                       Setting up the drawing window                                              #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
pygame.init()
screen = pygame.display.set_mode([500, 500])  # screen size
timer = pygame.time.Clock()  # set up clock so that tick rate can be changed
sound_beep = pygame.mixer.Sound('beep-07.wav')  # set up the sound clip

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#            Create 5 groups of sprites, each to represent the different group in the COVID pandemic               #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
blues = pygame.sprite.Group()  # unexposed; blue has an 80% chance of turning orange if colliding with orange or red
oranges = pygame.sprite.Group()  # infected; orange has a 50% chance of turning red after 5 days, or green after 15 days
reds = pygame.sprite.Group()  # sick; do not move; red has 2% change to become black or 98% chance to become green
blacks = pygame.sprite.Group()  # dead; do not move and do not infect other dots anymore.
greens = pygame.sprite.Group()  # immune; cannot spread the virus

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                              Creating dot objects that will be filled into the groups                            #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
for b in range(94):  # creates 94 blues dots
    pt1 = ((random.randint(0, 500)), (random.randint(0, 500)))
    pt2 = ((random.randint(0, 500)), (random.randint(0, 500)))
    blues.add(dot.Dot("images/blueBubble.png", 30, pt1, pt2))

for g in range(5):  # creates 5 green dots
    pt1 = ((random.randint(0, 500)), (random.randint(0, 500)))
    pt2 = ((random.randint(0, 500)), (random.randint(0, 500)))
    greens.add(dot.Dot("images/greenBubble.png", 30, pt1, pt2))

# create the one red dot
pt_r1 = ((random.randint(0, 500)), (random.randint(0, 500)))
pt_r2 = ((random.randint(0, 500)), (random.randint(0, 500)))
reds.add(dot.Dot("images/redBubble.png", 30, pt_r1, pt_r2))

'''# create the one orange dot
pt_r1 = ((random.randint(0, 500)), (random.randint(0, 500)))
pt_r2 = ((random.randint(0, 500)), (random.randint(0, 500)))
oranges.add(dot.Dot("images/orangeBubble.png", 30, pt_r1, pt_r2))

# Test points
ptA = (100, 100)
ptB = (400, 400)
ptC = (150, 150)

# Test cases
d1 = dot.Dot("images/orangeBubble.png", 30, ptB, ptA)
d2 = dot.Dot("images/blueBubble.png", 30, ptA, ptB)
d_r = dot.Dot("images/redBubble.png", 30, ptC, ptB)

# Adding test cases
oranges.add(d1)
blues.add(d2)
reds.add(d_r)'''

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                          Adding dot groups to dot super lists that will be used later                            #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
dots = [blues, oranges, reds, blacks, greens]  # in order of pandemic flowchart
movable_dots = [blues, greens, oranges]  # only the dots that can move

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                    Begin loop that runs all the collision, movement, status , etc. code                          #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

screen.fill((255, 255, 255))  # Fill the background with white
tick_rate = 20  # number must be a multiple of 20 for program to work

# Run until the user asks to quit: this is where all the movement and drawing happens
running = True
while running:  # Always running

    # How to stop the code so that it doesn't go on forever
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    #                               Code below deals with moving and drawing dots                                      #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    screen.fill((255, 255, 255))  # Fills the screen with white and removes any past dots

    # Draw all the dots
    for e in dots:
        for ee in e:
            screen.blit(ee.image, ee.gps)

    # Move dots; applies to groups that are not dead, sick, or sheltered in place (SIP no implemented yet)
    for e in movable_dots:
        for ee in e:
            ee.update()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    #                               Code below deals with collision between groups                                     #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    # Collisions that involve people who carry the virus and those who do not (blue with orange and red)
    for e in blues:  # people who have not interacted with the virus
        blue_orange_collisions = pygame.sprite.spritecollide(e, oranges, False, pygame.sprite.collide_circle)
        blue_red_collisions = pygame.sprite.spritecollide(e, reds, False, pygame.sprite.collide_circle)
        # print(blue_orange_collisions)
        # print(blue_red_collisions)
        if len(blue_orange_collisions) != 0:  # there's at least 1 collision with an infected person
            chance_infected = (random.randint(1, 100))  # random chance of person getting infected
            if 1 <= chance_infected <= 80:  # dot interacts with someone infected and becomes infected (80% chance)
                # print('Infected')
                blues.remove(e)                                                 # dot is no longer blue
                e.img = pygame.image.load("images/orangeBubble.png").convert()     # change dot to look orange
                e.image = pygame.transform.scale(e.img, (e.size, e.size))
                oranges.add(e)                                                  # add dot to orange bc infected
            else:  # dot interacts with someone sick or infected but does not become infected
                pass
                # print('Safe')
            # sound_beep.play()               # play the beep sound to signify collision

        if len(blue_red_collisions) != 0:   # there's at least 1 collision with a sick person
            chance_infected = (random.randint(1, 100))  # random chance of person getting infected
            if 1 <= chance_infected <= 80:  # dot interacts with someone sick and becomes infected (80% chance)
                # print('Infected')
                blues.remove(e)                                                 # dot is no longer blue
                e.img = pygame.image.load("images/orangeBubble.png").convert()     # change dot to look orange
                e.image = pygame.transform.scale(e.img, (e.size, e.size))
                oranges.add(e)                                                  # add dot to orange bc infected
            else:  # dot interacts with someone sick or infected but does not become infected
                pass
                # print('Safe')
            # sound_beep.play()               # play the beep sound to signify collision

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    #                        Code below deals with groups naturally turning into other groups                          #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    for e in oranges:
        e.day_counter += tick_rate  # add tick_rate to day counter (20 ticks = 1 day)
        if e.day_counter == 100:  # when tick_rate hits 100 (5 days) check if person becomes sick
            chance_sick = (random.randint(1, 100))  # random chance of person getting sick
            if 1 <= chance_sick <= 50:  # infected dot becomes sick after 5 days (80% chance)
                # print('Sick')
                e.day_counter = 0                                         # reset counter for further calculations
                oranges.remove(e)                                         # dot is no longer orange
                e.img = pygame.image.load("images/redBubble.png").convert()  # change dot to look red
                e.image = pygame.transform.scale(e.img, (e.size, e.size))
                reds.add(e)                                               # add dot to red bc sick
            else:
                pass
                # print('Will become immune in 10 more days')
        elif e.day_counter == 300:  # when tick_rate hits 300 (15 days) person recovers
            # print('Recovered, person is now immune.')
            e.day_counter = 0                                             # reset counter for further calculations
            oranges.remove(e)                                             # dot is no longer orange
            e.img = pygame.image.load("images/greenBubble.png").convert()    # change dot to look red
            e.image = pygame.transform.scale(e.img, (e.size, e.size))
            greens.add(e)                                                 # add dot to red bc sick

    for e in reds:
        e.day_counter += tick_rate  # add tick_rate to day counter (20 ticks = 1 day)
        if e.day_counter == 200:  # when tick_rate hits 200 (10 days) check if person will die or recover
            chance_sick = (random.randint(1, 100))  # random chance of person dying
            if 1 <= chance_sick <= 2:  # sick dot dies after 10 days (2% chance)
                # print('Dead')
                e.day_counter = 0                                           # reset counter for further calculations
                reds.remove(e)                                              # dot is no longer red
                e.img = pygame.image.load("images/blackBubble.png").convert()  # change dot to look black
                e.image = pygame.transform.scale(e.img, (e.size, e.size))
                blacks.add(e)                                               # add dot to black bc dead
            else:
                # print('Recovered, person is now immune.')
                e.day_counter = 0                                           # reset counter for further calculations
                reds.remove(e)                                              # dot is no longer red
                e.img = pygame.image.load("images/greenBubble.png").convert()  # change dot to look green
                e.image = pygame.transform.scale(e.img, (e.size, e.size))
                greens.add(e)                                # add dot to greens bc person recovered and is now immune

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    #                     Code below deals with the while loop that iterates on all the code                           #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    pygame.display.flip()  # Flip the display
    timer.tick(tick_rate)  # tick-rate, change number to edit the speed at which the dots move (20 ticks = 1 day)

# Done! Time to quit. Program ends here.
pygame.quit()
