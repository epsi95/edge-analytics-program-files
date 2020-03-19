from utils import Point
from geo_fence_detector import GeoFenceDetectorPolygon as gdp

vertices = [Point(77.0645319, 28.4978804), Point(77.0583883, 28.493911), Point(77.0596883, 28.492272), Point(77.0746443, 28.492991), Point(77.0744833, 28.498492)]
observer = Point(77.0577773, 28.496976)
detector = gdp(vertices, observer)
print(detector.isInsideGeoFence())
dd = [28.494479,77.0613043]
print(detector.isInsideGeoFenceWithObserver(Point(dd[1], dd[0])))