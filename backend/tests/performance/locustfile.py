from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"

    @task(2)
    def health_check(self):
        self.client.get("/health")

    @task(1)
    def initiate_analysis(self):
        self.client.post("/api/analysis/", json={"url": "https://www.youtube.com/watch?v=perf_test"})

    @task(1)
    def get_non_existent_status(self):
        with self.client.get("/api/status/999999", name="/api/status/[id]", catch_response=True) as response:
            if response.status_code == 404:
                response.success()
            else:
                response.failure(f"Expected 404 but got {response.status_code}")
