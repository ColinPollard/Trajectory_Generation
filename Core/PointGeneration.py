# Author: Colin Pollard
# Date: 10/30/2020
# This file encompasses methods to generate various trajectories.
import math


def __polar2rectangular(theta, radius):
    """
    This converts polar coordinates to rectangular coordinates.

    :param theta: Angle
    :param radius: Radius
    :return: X, Y
    """

    x = radius * math.cos(theta)
    y = radius * math.sin(theta)

    return x, y


def circleSet(diameter=0.04, height=0.04, pointDensity=0.001, circlesPerLayer=4, layers=4):
    """
    Creates a new trajectory consisting of stacked layers of concentric circles.

    :param diameter: Diameter of the outer circle
    :param height: Height of the stack
    :param pointDensity: Meters per point
    :param circlesPerLayer: Circles per layer
    :param layers: Layers in the stack
    :return: Lists of x, y, z
    """

    # Lists to hold sublists of points from circle gen
    xLists = []
    yLists = []
    zLists = []

    # Iterate through layers
    for hIndex in range(1, layers + 1) :
        # Iterate through circles
        tempHeight = hIndex * height / layers
        for cIndex in range(1, circlesPerLayer + 1):
            # Calculate the current diameter
            tempDiameter = cIndex * diameter / circlesPerLayer
            # Create circle
            tempX, tempY, tempZ = singleCircle(tempDiameter, pointDensity=pointDensity, heightOffset=tempHeight)
            # Append sublist
            xLists.append(tempX)
            yLists.append(tempY)
            zLists.append(tempZ)

    # Interpolate between sublists and create final output
    xList, yList, zList = appendPaths(xLists, yLists, zLists, pointDensity=pointDensity)
    return xList, yList, zList


def singleCircle(diameter=0.04, pointDensity=0.001, heightOffset=0):
    """
    Creates a new circle trajectory of size diameter with points every pointDensity meters.

    :param diameter: Diameter of the Circle
    :param pointsDensity: Meters per Point
    :param heightOffset: Height to draw circle
    :return: List of x, y, z
    """

    # Create list of points
    xList = []
    yList = []
    zList = []

    # Iterate around the circle
    circumference = math.pi*diameter
    radius = diameter / 2
    pointsPerCircle = int(circumference / pointDensity)
    for index in range(0, pointsPerCircle):
        theta = index * (2*math.pi / pointsPerCircle)
        x, y = __polar2rectangular(theta, radius)
        xList.append(x)
        yList.append(y)
        zList.append(heightOffset)

    return xList, yList, zList


def singleSpiral(diameter=0.04, spiralHeight=0.04, pointsPerSpiral=1000, thetaStart=0, heightOffset=0):
    """
    Create a single spiral in rectangular coordinates.

    :param diameter: Diameter of the spiral
    :param spiralHeight: Height of the spiral
    :param pointsPerSpiral: Number of points in spiral
    :param thetaStart: Starting angle of generation
    :param heightOffset: Starting height of generation
    :return: Lists of x, y, z
    """

    # Create lists to store 2D polar values from spiral
    radiusList = []
    thetaList = []

    # Iterate through spiral points in polar coordinates.
    for index in range(0, pointsPerSpiral):
        # Iterate theta from 0 - 2pi
        theta = index * (2 * math.pi / pointsPerSpiral) + thetaStart
        # Handle wraparound from offset
        if theta > 2*math.pi:
            theta -= 2*math.pi
        # Iterate radius from 0 - diameter
        radius = index * (diameter / pointsPerSpiral)
        # Append values
        radiusList.append(radius)
        thetaList.append(theta)

    # Create list to store 3D, non-offset positions
    xList = []
    yList = []
    zList = []

    # Iterate through polar lists
    for index in range(0, len(radiusList)):
        # Convert polar to rectangular 2D
        x, y = __polar2rectangular(thetaList[index], radiusList[index])
        # Calculate z position within spiral slice
        z = (spiralHeight / pointsPerSpiral) * index + heightOffset
        # Append Values
        xList.append(x)
        yList.append(y)
        zList.append(z)

    return xList, yList, zList


def appendPaths(xLists, yLists, zLists, pointDensity=0.001):
    """
    Appends multiple trajectory paths together and interpolates start and end points.

    :param xLists: A list of XLists to append.
    :param yLists: A list of YLists to append.
    :param zLists: A list of ZLists to append.
    :return: xList, yList, zList
    """

    # Return lists
    xList = []
    yList = []
    zList = []

    # Iterate through the number of lists to append
    for index in range(0, len(xLists)):
        # Iterate through the sublists
        for index2 in range(0, len(xLists[index])):
            xList.append(xLists[index][index2])
            yList.append(yLists[index][index2])
            zList.append(zLists[index][index2])

        # Interpolate to next list.
        if index < len(xLists) - 1:
            prevPoint = [xLists[index][-1], yLists[index][-1], zLists[index][-1]]
            nextPoint = [xLists[index+1][0], yLists[index+1][0], zLists[index+1][0]]
            dx = (nextPoint[0] - prevPoint[0])
            dy = (nextPoint[1] - prevPoint[1])
            dz = (nextPoint[2] - prevPoint[2])
            # Calculate the distance between the last point and next point
            distance = math.sqrt(dx**2 + dy**2 + dz**2)
            # Calculate number of points of uniform density between these
            numPoints = int(distance / pointDensity)

            for interpolationIndex in range(0, numPoints):
                xList.append(prevPoint[0] + (interpolationIndex * dx / numPoints))
                yList.append(prevPoint[1] + (interpolationIndex * dy / numPoints))
                zList.append(prevPoint[2] + (interpolationIndex * dz / numPoints))

    return xList, yList, zList


def compression(verticalDisplacement, lateralDisplacement, pointDensity=0.001):
    """
    Creates a compression trajectory with a lateral displacement at the bottom of the compression region.

    :param verticalDisplacement: Vertical height of the compression
    :param lateralDisplacement: Lateral displacement at bottom of compression
    :param pointDensity: Meters per point
    :return: List of points x, y, z
    """

    xList = []
    yList = []
    zList = []

    distance = math.sqrt(verticalDisplacement**2 + lateralDisplacement**2)
    numPoints = int(distance / pointDensity)

    for index in range(0, numPoints):
        xList.append(index * lateralDisplacement / numPoints)
        yList.append(0)
        zList.append(index * verticalDisplacement / numPoints)

    return xList, yList, zList
