"""
UBC Eye Movement Data Analysis Toolkit (EMDAT), Version 3
Created on 2011-08-25

Commonly used helper methods.

Authors: Samad Kardan (creator), Sebastien Lalle.
Institution: The University of British Columbia.
"""

import math
import ast

def point_inside_polygon(x,y,poly):
    """Determines if a point is inside a given polygon or not

        The algorithm is called "Ray Casting Method".

    Args:
        poly: is a list of (x,y) pairs defining the polgon

    Returns:
        True or False.
    """
    """Determines if a point is inside a given polygon or not
        The algorithm is called "Ray Casting Method".
    Args:
        poly: is a list of (x,y) pairs defining the polgon

    Returns:
        True or False.
    """
    inside = False
    n = len(poly)
    if n == 0:
        return False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    #print inside
    return inside

def stddev(data):
    """Returns the standard deviation of a list of numbers

    Args:
        data: a list of numbers

    returns:
        a float that is the std deviation of the list of numbers or NAN if it is undefined
    """
    if len(data)< 2:
        return float('nan')
    m = mean(data)
    return math.sqrt(sum(map(lambda x: (x-m)**2, data))/float(len(data)-1))


def mean(data):
    """Returns the average of a list of numbers

    Args:
        data: a list of numbers

    returns:
        a float that is the average of the list of numbers
    """
    if len(data)==0:
        return 0
    return sum(data) / float(len(data))
	
def euclidean_distance(point1, point2):
    (x1, y1) = point1
    (x2, y2) = point2

    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)

    return math.sqrt((x1-x2)**2 + (y1-y2)**2)
