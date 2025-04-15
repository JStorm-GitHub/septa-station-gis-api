FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .  

# Make sure the GeoJSON gets generated
RUN python scripts/process_kml.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]