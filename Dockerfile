FROM python:3.11-slim AS builder
WORKDIR /app

COPY app/ ./app/
COPY scripts/ ./scripts/
COPY shared/ ./shared/
COPY requirements.txt .
RUN pip install --no-cache-dir -r scripts/kml_requirements.txt

RUN python scripts/process_kml.py

FROM python:3.11-slim
WORKDIR /app

COPY --from=builder /app/shared/storage/stations_parsed.geojson /app/default_geojson/stations_parsed.geojson
COPY app/ ./app/
COPY shared/ ./shared/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
