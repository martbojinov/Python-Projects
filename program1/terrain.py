
import math
import random
import turtle

# Note: For this example, we are using hardcoded points/vertices to test the functionality of the viewer and animation.
# For Program 1, you need to replace the code between the tags # BEGIN and # END with your code.
# Your code should generate the VERTICES and TRIANGLES using your recursive "midpoint_displacement" function.
# This setup is optimized for points values generated in the range -1.00 to 1.00.
# You may need the adjust the value of FOV to generate points with higher ranges.


# BEGIN
# =====================================================================
num = 0  # used to number the triangles in the TRIANGLES list
VERTICES = []  # meant to contain all the vertices of the triangles
TRIANGLES = []  # meant to tell the program what vertices to draw


def midpoint(p1, p2):
    """ Takes in 2 points and outputs the midpoint
        The output is an ordered triple. The method for computing the midpoint uses vector calculus."""

    # norm_u = length from one point to another
    norm_u = math.sqrt((p1[0] - p2[0]) ** 2 +
                       (p1[1] - p2[1]) ** 2 +
                       (p1[2] - p2[2]) ** 2)
    # vector_u is directional vector from one point to another
    vector_u = (p1[0] - p2[0],
                p1[1] - p2[1],
                p1[2] - p2[2])
    # unit vector created by dividing vector by norm, has a length of 1
    unit_vector = (vector_u[0] / norm_u,
                   vector_u[1] / norm_u,
                   vector_u[2] / norm_u)
    # unit vector used to solve for new points (multiplied by 1/2 for midpoint)
    mp = (p1[0] - (unit_vector[0] * (1 / 2) * norm_u),
          p1[1] - (unit_vector[1] * (1 / 2) * norm_u),
          p1[2] - (unit_vector[2] * (1 / 2) * norm_u))

    return mp


def displacement(p1, dimension, magnitude=0):
    """ Takes in one point of (x, y, z) and adds or subtracts a random number between -0.5 and 0.7.
        The function does this to all x, y, and z. Input can be a list or tuple but outputs a tuple.
        The magnitude parameter is used to increase the amount of scaling at higher levels of recursion.
        The dimension parameter is used to specify 3D vs 2D; setting it to true will cause the function to not displace
        the z axis. The dimension parameter is handled in the midpoint_displacement function and simply passed in."""

    l1 = list(p1)  # turn into list for mutability

    # displacing each coordinate by a random amount
    if magnitude > 0:  # if magnitude (recursion level) == 0, then there will be no displacement; mag. must be > 0
        l1[0] += random.uniform(-0.07 * magnitude, 0.07 * magnitude)
        l1[1] += random.uniform(-0.07 * magnitude, 0.07 * magnitude)
        if dimension == False:  # if dimension == False --> 2D, no need to change z axis
            l1[2] += random.uniform(-0.07 * magnitude, 0.07 * magnitude)
    else:  # executes when magnitude is 0 so that there is still displacement at the lowest level of recursion
        l1[0] += random.uniform(-0.05, 0.05)
        l1[1] += random.uniform(-0.05, 0.05)
        if dimension == False:  # if dimension == False --> 2D, no need to change z axis
            l1[2] += random.uniform(-0.05, 0.05)

    p1 = tuple(l1)  # back to tuple for output
    return p1


def midpoint_displacement(level, p1, p2, p3, dimension=False):
    """ The recursive function that creates all the triangles. Takes in level for recursion depth. The three points are
        the corners of the triangles that are operated upon. Function produces no output but instead adds vertices
        and triangles to VERTICES and TRIANGLES lists. To make triangles 2D instead of 3D, set dimension to True."""

    global num  # used for numbering of triangles in TRIANGLES

    # calculation of midpoints and their displacement;
    m1 = displacement(midpoint(p1, p2), dimension, level)
    m2 = displacement(midpoint(p2, p3), dimension, level)
    m3 = displacement(midpoint(p3, p1), dimension, level)

    # test cases with no displacement (completely flat 2D)
    # m1 = midpoint(p1, p2)
    # m2 = midpoint(p2, p3)
    # m3 = midpoint(p3, p1)

    if level > 0:  # recursive part of function; 4 smaller triangles created within normal triangle
        midpoint_displacement(level - 1, p1, m1, m3, dimension)  # creates top triangle
        midpoint_displacement(level - 1, p2, m2, m1, dimension)  # creates bottom left triangle
        midpoint_displacement(level - 1, p3, m3, m2, dimension)  # creates bottom right triangle
        midpoint_displacement(level - 1, m1, m2, m3, dimension)  # creates middle triangle

    else:  # once function reaches level 0, add vertices and triangles to respective lists for printing

        VERTICES.append(p1)
        VERTICES.append(p2)
        VERTICES.append(p3)

        TRIANGLES.append((num, num + 1, num + 2))
        num += 3

    return None  # function returns no output because numbers are directly added to their respective lists


# =====================================================================
# END


def transform(x, y, z, angle, tilt):
    # Animation control (around y-axis). For a view of earth from space, it's moving over the equator.
    s, c = math.sin(angle), math.cos(angle)
    x, y = x * c - y * s, x * s + y * c

    # Camera tilt  (around x-axis). For a view of earth from space, the tilt angle is measure from the equator.
    s, c = math.sin(tilt), math.cos(tilt)
    z, y = z * c - y * s, z * s + y * c

    # Setting up View Parameters
    y += 5  # Fixed Distance from top
    FOV = 1000  # Fixed Field of view
    f = FOV / y
    sx, sy = x * f, z * f
    return sx, sy


def main():
    # Create terrain using turtle
    terrain = turtle.Turtle()
    terrain.pencolor("blue")
    terrain.pensize(2)

    # Turn off move time for instant drawing
    turtle.tracer(0, 0)
    terrain.up()
    angle = 0

    while True:
        # Clear the screen
        terrain.clear()

        # Transform the terrain
        VERT2D = []
        for vert3D in VERTICES:
            x, y, z = vert3D
            sx, sy = transform(x, y, z, angle, -0.2)  # 1.5708 for 90 degree (2D); -0.25 for 3D
            VERT2D.append((sx, sy))

        # Draw the terrain
        for triangle in TRIANGLES:
            points = []
            points.append(VERT2D[triangle[0]])
            points.append(VERT2D[triangle[1]])
            points.append(VERT2D[triangle[2]])

            # Draw the triangle
            terrain.goto(points[0][0], points[0][1])
            terrain.down()

            terrain.goto(points[1][0], points[1][1])
            terrain.goto(points[2][0], points[2][1])
            terrain.goto(points[0][0], points[0][1])
            terrain.up()

        # Update screen
        turtle.update()

        # Control the speed of animation
        angle += 0.0015


if __name__ == "__main__":
    turtle.bgcolor("#5C5C5C")  # background color set to grey to be easier on the eyes

    # be sure to run the midpoint_displacement function first and then main
    # For 2D, add True to the end of midpoint_displacement --> midpoint_displacement(lvl, p1, p2, p3, True)
    # For top down view set tilt to 1.5708 in main()
    midpoint_displacement(3, (1, 0, 0), (-1, -1.7, 0), (-1, 1.7, 0))  # recursion level 3 yields best results

    main()  # transform function that actually draws the terrain and rotates around it.
