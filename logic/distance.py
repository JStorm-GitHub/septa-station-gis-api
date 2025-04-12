from math import cos, radians
from shapely.geometry import shape, Point
from haversine import haversine

def get_distance(location: tuple[float, float], rtree_idx, features):
    query_point = Point(location[0], location[1]) 

    try:
        candidate_id = next(rtree_idx.nearest((query_point.x, query_point.y, query_point.x, query_point.y), 1))
    except StopIteration:
        return False

    station = features[candidate_id]
    station_geom = shape(station["geometry"])
    station_point = station_geom if station_geom.geom_type == "Point" else station_geom.centroid

    distance = haversine((query_point.x, query_point.y), (station_point.x, station_point.y), unit='mi')
    
    return distance