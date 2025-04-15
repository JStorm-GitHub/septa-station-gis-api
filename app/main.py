from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import router
from app.middleware import auth_and_rate_limit
from geojson import load as geojson_load
from shapely.geometry import shape
from rtree import index

STATION_TREE = None
STATION_FEATURES = None
geojson_storage_path = "shared/storage/stations_parsed.geojson"

@asynccontextmanager
async def lifespan(app: FastAPI):
    ### This function runs at start and generates an r-tree from the GeoJSON file
    ### This r-tree is then loaded into app state memory
    global STATION_TREE, STATION_FEATURES

    with open(geojson_storage_path, "r") as f:
        data = geojson_load(f)

    STATION_FEATURES = data["features"]
    STATION_TREE = index.Index()

    for i, feature in enumerate(STATION_FEATURES):
        geometry = shape(feature["geometry"])
        point = geometry if geometry.geom_type == "Point" else geometry.centroid
        STATION_TREE.insert(i, (point.x, point.y, point.x, point.y))

    app.state.STATION_TREE = STATION_TREE
    app.state.STATION_FEATURES = STATION_FEATURES
    yield

app = FastAPI(lifespan=lifespan)

app.middleware("http")(auth_and_rate_limit)

app.include_router(router)
