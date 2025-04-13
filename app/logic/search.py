from shapely.geometry import Point

def find_closest_point(location: tuple[float, float], rtree_idx, features):
    query_point = Point(location[0], location[1]) 

    nearest_id = next(rtree_idx.nearest((query_point.x, query_point.y, query_point.x, query_point.y), 1))
    return features[nearest_id]