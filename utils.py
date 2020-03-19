# This class implements Point which has x value and y value. In geo-location scenario x can be longitude and y can be latitude
# The code is written and maintained by Probhakar Sarkar , March18, 2020

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distanceWith(self, point2):
        distance = ((self.x - point2.x)**2 + (self.y - point2.y)**2)**0.5
        return distance

class Edge:
    def __init__(self, fromPoint, toPoint):
        self.fromPoint = fromPoint
        self.toPoint = toPoint