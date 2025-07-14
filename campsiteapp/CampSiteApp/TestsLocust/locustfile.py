import threading
from locust import HttpUser, task, between
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DRF_TOKEN = "c9ea84f31a264b226e2327ace58d75797531238f"

number_lock = threading.Lock()
global_number = 0

class CreateUserTest(HttpUser):
    wait_time = between(1, 2)

    @task
    def create_user(self):
        global global_number
        with number_lock:
            current_number = global_number
            global_number += 1

        payload = {
            "username": f"newusertest{current_number}",
            "password": "test",
            "email": f"newusertest{current_number}@example.com"
        }

        headers = {
            "Authorization": f"Token {DRF_TOKEN}",
            "Content-Type": "application/json"
        }

        with self.client.post(
            "/api/v1/admin/",
            json=payload,
            headers=headers,
            verify=False,
            catch_response=True
        ) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Unexpected response: {response.status_code} - {response.text}")
