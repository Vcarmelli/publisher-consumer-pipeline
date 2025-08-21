import json
import os
from dotenv import load_dotenv
from utils import get_redis_client


class Publisher:
    def __init__(self):
        load_dotenv()
        self.articles = None
        self.client = get_redis_client()
        self.queue = os.getenv("QUEUE_NAME", "articles_queue")


    def publish_articles(self, json_file):
        # Load JSON file
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Push each article into Redis queue
        for article in data["articles"]:
            task = {
                "id": article["id"],
                "url": article["url"],
                "source": article["source"],
                "category": article["category"],
                "priority": article["priority"]
            }

            # Store as JSON string in queue
            self.client.rpush(self.queue, json.dumps(task))
            print(f"Pushed article {task['id']} from {task['source']} into queue.")


if __name__ == "__main__":
    publisher = Publisher()
    json_file_path = os.path.join(os.path.dirname(__file__), "articles.json")
    publisher.publish_articles(json_file_path)