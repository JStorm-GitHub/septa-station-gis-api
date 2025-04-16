#!/bin/sh
set -e

# Check if the file exists in the mounted directory,
# If not, copy it from the backup location.
if [ ! -f /app/shared/storage/stations_parsed.geojson ]; then
    echo "GeoJSON file not found in /app/shared/storage. Copying from backup..."
    cp /app/default_geojson/stations_parsed.geojson /app/shared/storage/stations_parsed.geojson
fi

# Start the main process (adjust command as needed)
exec "$@"