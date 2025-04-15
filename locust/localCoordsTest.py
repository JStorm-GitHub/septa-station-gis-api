from locust import HttpUser, task, between
import random
import json
import logging

with open("api_key.txt") as f:
    API_KEY = f.read().strip()

class LocalCoordsTest(HttpUser):
    host = "http://127.0.0.1:8000/"
    wait_time = between(1, 2)

    def on_start(self):
        self.headers = {
            "Authorization": API_KEY
        }

    def random_coordinates(self):
        lon = random.uniform(-75.3, -75.1)
        lat = random.uniform(39.95, 40.05)
        return lon, lat

    @task
    def get_closest_point(self):
        lon, lat = self.random_coordinates()
        with self.client.get(
            "/closest-point",
            headers=self.headers,
            params={"lon": lon, "lat": lat},
            catch_response=True
        ) as response:
            try:
                data = response.json()
                logging.info(f"\nSelected Coords: lat:{lat}, lon:{lon}\n")
                logging.info("\nResponse body\n")
                logging.info(json.dumps(data, indent=2))
            except Exception as e:
                logging.info(f"\nInvalid JSON response. Status: {response.status_code}")
                logging.info(f"Raw response: {response.text}")