import json
import math

def find_closest_point(coords, geojson_data):
    def haversine(coord1, coord2):
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        R = 6371  # km

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lambda = math.radians(lon2 - lon1)

        a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    # def closest_feature(target_coord, geojson_data):
    # with open(geojson_data_path) as f:
    #     geojson_data = json.load(f)
    
    features = geojson_data["features"]

    def feature_coord(feature):
        lon, lat = feature["geometry"]["coordinates"]
        return (lat, lon) 

    return min(features, key=lambda f: haversine(coords, feature_coord(f)))

    # # Example usage
    # with open("stations_parsed.geojson") as f:
    #     geojson_data = json.load(f)

    # target = (39.9526, -75.1652)
    # closest = find_closest_point(target, geojson_data)

    # # print(closest["properties"]["Stop_ID"]) 