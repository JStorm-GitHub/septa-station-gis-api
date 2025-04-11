from fastapi import FastAPI, Query, HTTPException
from contextlib import asynccontextmanager
from filelock import FileLock
from cachetools import TTLCache
from cachetools.keys import hashkey
from geojson import load as geojson_load
import hashlib
import os
from db.create import create_db
from db.unzip import unzip_kmz
from logic.search import find_closest_point

kmz_storage_path = "storage/SEPTARegionalRailStations2016.kmz"
kml_storage_path = "storage/temp_kmz"
geojson_storage_path = "storage/stations_parsed.geojson"

STATION_DATA = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global STATION_DATA
    if not os.path.exists(geojson_storage_path):
        unzip_kmz(kmz_storage_path, kml_storage_path)
        create_db(f"{kml_storage_path}/doc.kml", geojson_storage_path)

    with open(geojson_storage_path, "r") as f:
        STATION_DATA = geojson_load(f)

    yield

app = FastAPI(lifespan=lifespan)

LOCK_DIR = "/tmp/geo_locks"
os.makedirs(LOCK_DIR, exist_ok=True)

cache = TTLCache(maxsize=1000, ttl=60 * 60)  # Cache 1000 items, expire after 1 hour

def location_key(lat: float, lon: float) -> str:
    key = f"{lat:.6f}_{lon:.6f}"
    return hashlib.md5(key.encode()).hexdigest()

def make_cache_key(lat: float, lon: float):
    return hashkey(round(lat, 6), round(lon, 6))

@app.get("/closest-point")
def get_closest_point(
    lat: float = Query(...),
    lon: float = Query(...)
):
    key = make_cache_key(lat, lon)

    if key in cache:
        return cache[key]
    
    lock_name = location_key(lat, lon)
    lock_path = os.path.join(LOCK_DIR, f"{lock_name}.lock")

    with FileLock(lock_path, timeout=10):
        try:
            result = find_closest_point((lat, lon), STATION_DATA)
            cache[key] = result
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
