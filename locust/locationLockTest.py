from locust import HttpUser, task, between
import random
import json
import logging

with open("../shared/api_key.txt") as f:
    API_KEY = f.read().strip()

class LocationLockTest(HttpUser):
    host = "http://127.0.0.1:8000/"
    wait_time = between(0.5, 1)

    def on_start(self):
        self.headers = {
            "Authorization": API_KEY
        }
    
    def repeat_coords(self):
        lon = -75.149532
        lat = 39.981479
        return lon,lat

    @task
    def get_closest_point(self):
        lon, lat = self.repeat_coords()
        with self.client.get(
            "/closest-point",
            headers=self.headers,
            params={"lon": lon, "lat": lat},
            catch_response=True
        ) as response:
            try:
                data = response.json()
                logging.info("\nResponse body\n")
                logging.info(json.dumps(data, indent=2))
            except Exception as e:
                logging.info(f"\nInvalid JSON response. Status: {response.status_code}")
                logging.info("Raw response:", response.text)