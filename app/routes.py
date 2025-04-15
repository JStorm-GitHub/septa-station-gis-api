from fastapi import APIRouter, Query, Request, HTTPException
from cachetools import TTLCache
from cachetools.keys import hashkey
from app.logic.search import find_closest_point
from app.logic.distance import get_distance
from app.logic.nearby import is_nearby
from app.redis_client import r

router = APIRouter()

MAX_DISTANCE_MILES = 50
cache = TTLCache(maxsize=1000, ttl=60 * 60)

def make_cache_key(lon: float, lat: float):
    return hashkey(round(lon, 6), round(lat, 6))

@router.get("/closest-point")
def get_closest_point(
    request: Request,
    lon: float = Query(..., ge=-180, le=180),
    lat: float = Query(..., ge=-90, le=90)
):
    key = make_cache_key(lon, lat)

    if key in cache:
        return cache[key]

    redis_key = f"geo-lock:{key}"
    lock = r.lock(redis_key, timeout=10)
    got_lock = lock.acquire(blocking=True, blocking_timeout=10)
    if not got_lock:
        raise HTTPException(status_code=503, detail="Another request is processing this location")

    try:
        if key in cache:
            return cache[key]

        tree = request.app.state.STATION_TREE
        features = request.app.state.STATION_FEATURES

        result = find_closest_point((lon, lat), tree, features)
        distance = get_distance((lon, lat), tree, features)

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
    finally:
        lock.release()
