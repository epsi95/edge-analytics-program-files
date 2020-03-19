# Geo fence detection algorithm based on "crossing number algorithm(cn)"
# The code is written and maintained by Probhakar Sarkar , March18, 2020

from utils import Point, Edge

class GeoFenceDetectorPolygon:
    # pointList is a list of vertices of a polygon of type Point
    # observer is the location of type Point for whom geo-fence crossing should be detected
    # pointList = [Point(), Point(), Point()...]
    def __init__(self, pointList, observer = Point(0,0)):
        self.pointList = pointList
        self.observer = observer


    def isInsideGeoFenceWithObserver(self, observer): # user can check geo-fence breach for specific observer
        crossingNumber = 0
        fromPoint = self.pointList[0]
        for point in self.pointList[1:]:
            if(self.isEdgeHorizontal(fromPoint, point)):
                # do nothing because edhe is horizontal to x axis
                # update the from point and go to next
                fromPoint = point
            else:
                if(self.hasRightSideRayIntersection(Edge(fromPoint, point), observer)):
                    crossingNumber += 1
                    fromPoint = point
                else:
                    fromPoint = point

        if(crossingNumber % 2 == 0):
            return False
        else:
            return True


    def isInsideGeoFence(self): # here observer is static, once class is initialized can not be changed
        crossingNumber = 0
        fromPoint = self.pointList[0]
        for point in self.pointList[1:]:
            if(self.isEdgeHorizontal(fromPoint, point)):
                # do nothing because edhe is horizontal to x axis
                # update the from point and go to next
                fromPoint = point
            else:
                if(self.hasRightSideRayIntersection(Edge(fromPoint, point), self.observer)):
                    crossingNumber += 1
                    fromPoint = point
                else:
                    fromPoint = point

        if(crossingNumber % 2 == 0):
            return False
        else:
            return True


    @ staticmethod
    def isEdgeHorizontal(fromPoint, toPoint):
        if(fromPoint.y == toPoint.y):
            return True
        else:
            return False

    @ staticmethod
    def hasRightSideRayIntersection(edge, point):
        if (point.y > edge.fromPoint.y and point.y < edge.toPoint.y) or (point.y < edge.fromPoint.y and point.y > edge.toPoint.y):
            a1 = edge.fromPoint.x
            a2 = edge.toPoint.x
            b1 = edge.fromPoint.y
            b2 = edge.toPoint.y
            interSectedX = (((a1-a2)/(b1-b2))*(point.y - b1)) + a1 
            if(point.x < interSectedX):
                return True
            else:
                return False
        else:
            return False