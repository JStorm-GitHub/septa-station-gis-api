# septa-station-gis-api Project Setup

This project uses Docker to manage dependencies and services. Follow the steps below to get started.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed  
- [Docker Compose](https://docs.docker.com/compose/install/) installed  
- Python (for running the key generation script)

## Setup Instructions

1. **Generate the API key**

   This step creates a key file required by the application:

   ```bash
   python3 generate_key.py
   ```

2. **Build the Docker containers**

   Build the images defined in `docker-compose.yml`:

   ```bash
   sudo docker compose build
   ```

3. **Start the application**

   Run the services:

   ```bash
   sudo docker compose up
   ```

   The application can be reached at `http://localhost:8000`

## Notes

- The `generate_key.py` script must be run **before** building the Docker image so the key is available during the container build process.
- To stop the services, press `Ctrl+C` and then run:

   ```bash
   sudo docker compose down
   ```

## Locust Test 

Locust is a tool used to test api endpoints. It's recommended to open a new console and run separately.

```bash
cd locust
```

1. **Build Locust Docker**

    Build
    ```bash
    chmod +x build_docker.sh
    ./build_docker.sh
    ```

3. **Go to http://localhost:8089 and perform tests**