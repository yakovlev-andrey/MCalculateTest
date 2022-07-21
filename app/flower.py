import os
import requests

flower_url = os.environ.get("FLOWER_URL", "http://flower:5555")


class FlowerAPI:
    def __init__(self, url):
        self.url = url

    def tasks(self, params: dict = None) -> dict:
        r = requests.get(
            f"{self.url}/api/tasks",
            params=params,
        )
        return r.json()

    def task(self, task_id: int) -> dict:
        r = requests.get(f"{self.url}/api/task/result/{task_id}")
        return r.json()


flower = FlowerAPI(url=flower_url)
