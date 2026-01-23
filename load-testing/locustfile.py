from locust import HttpUser, task, between

class SignalAPIUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task(3)
    def get_top_signals(self):
        self.client.get("/signals/top?k=5")

    @task(1)
    def get_single_signal(self):
        self.client.get("/signals/BTCUSDT")
