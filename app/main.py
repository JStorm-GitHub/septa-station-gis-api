from fastapi import FastAPI, Query, HTTPException, Depends
from contextlib import asynccontextmanager
from filelock import FileLock
from cachetools import TTLCache
from cachetools.keys import hashkey
from geojson import load as geojson_load
from shapely.geometry import shape, Point
from rtree import index
import hashlib
import os
from db.create import create_db
from db.unzip import unzip_kmz
from logic.search import find_closest_point
from logic.distance import get_distance
from logic.nearby import is_nearby
from auth import verify_api_key

### FORMAT IS (LON,LAT)

kmz_storage_path = "storage/SEPTARegionalRailStations2016.kmz"
kml_storage_path = "storage/temp_kmz"
geojson_storage_path = "storage/stations_parsed.geojson"

STATION_TREE = None
STATION_FEATURES = None
MAX_DISTANCE_MILES = 50

@asynccontextmanager
async def lifespan(app: FastAPI):
    global STATION_TREE, STATION_FEATURES
    
    if not os.path.exists(geojson_storage_path):
        unzip_kmz(kmz_storage_path, kml_storage_path)
        create_db(f"{kml_storage_path}/doc.kml", geojson_storage_path)

    with open(geojson_storage_path, "r") as f:
        data = geojson_load(f)

    STATION_FEATURES = data["features"]
    STATION_TREE = index.Index()

    for i, feature in enumerate(STATION_FEATURES):
        geometry = shape(feature["geometry"])
        point = geometry if geometry.geom_type == "Point" else geometry.centroid
        STATION_TREE.insert(i, (point.x, point.y, point.x, point.y))

    yield

app = FastAPI(lifespan=lifespan)

LOCK_DIR = "/tmp/geo_locks"
os.makedirs(LOCK_DIR, exist_ok=True)

cache = TTLCache(maxsize=1000, ttl=60 * 60)  

def location_lock_key(lon: float, lat: float) -> str:
    key = f"{lon:.6f}_{lat:.6f}"
    return hashlib.md5(key.encode()).hexdigest()

def make_cache_key(lon: float, lat: float):
    return hashkey(round(lon, 6), round(lat, 6))

@app.get("/closest-point",dependencies=[Depends(verify_api_key)])
def get_closest_point(
    lon: float = Query(...,ge=-180, le=180, description="Longitude must be between -180 and 180."),
    lat: float = Query(...,ge=-90, le=90, description="Latitude must be between -90 and 90.")
):
    key = make_cache_key(lon, lat)

    # if key in cache:
    #     return cache[key]
    
    lock_name = location_lock_key(lon, lat)
    lock_path = os.path.join(LOCK_DIR, f"{lock_name}.lock")

    with FileLock(lock_path, timeout=10):
        try:
            result = find_closest_point((lon, lat), STATION_TREE, STATION_FEATURES)

            distance = get_distance((lon, lat), STATION_TREE, STATION_FEATURES)

            if not is_nearby(distance, max_distance=MAX_DISTANCE_MILES): 
                result = {
                    "type": "Feature",
                    "geometry": None,
                    "properties": {
                        "name": None,
                        "message": "No SEPTA stations found within 50 miles."
                    }
                }
            cache[key] = result
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
