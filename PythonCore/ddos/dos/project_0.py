from locust import HttpUser, task, between

class MyUser(HttpUser):
    # Устанавливаем время ожидания между задачами от 0.1 до 0.2 секунд
    wait_time = between(0.1, 0.2)

    @task
    def get_on_client(self):
        # Выполняем GET-запрос к главной странице
        response = self.client.get("/")
        print(f"Response Code: {response.status_code}")

if __name__ == "__main__":
    pass
