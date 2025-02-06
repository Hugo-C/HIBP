from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    host = "http://localhost"

    @task
    def hello_world(self):
        self.client.get("/api/v1/haveibeenrocked/b6855")

    # TODO ideally we should have something like
    #  90% of hash prefix been requested in a set of 10k password and rest of them random