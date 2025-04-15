from pathlib import Path
from unzip_kmz import unzip_kmz
from create_geojson import create_db

kmz_path = Path("shared/storage/SEPTARegionalRailStations2016.kmz")
geojson_path = Path("shared/storage/stations_parsed.geojson")
kml_path = Path("shared/storage/temp_kmz")

kml_path.mkdir(parents=True, exist_ok=True)

unzip_kmz(kmz_path, kml_path)
create_db(f"{kml_path}/doc.kml", geojson_path)