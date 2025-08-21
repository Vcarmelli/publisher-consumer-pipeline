import os
import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from article import Article
from database import Database
from utils import get_redis_client, summarize_article


class Consumer:
    def __init__(self):
        load_dotenv()
        self.client = get_redis_client()
        self.queue = os.getenv("QUEUE_NAME", "articles_queue")


    def pop_task(self) -> dict:
        article_data = self.client.lpop(self.queue)
        if not article_data:
            return None

        task = json.loads(article_data)
        print(f"Popped article {task['id']} → {task['url']}")
        return task
    
    def scrape_content(self, url: str) -> str:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            if response.status_code != 200:
                # print(f"Unable to scrape the article (blocked or restricted)")
                return False
        
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text() for p in paragraphs if p.get_text().strip()])

            if not content:
                return "No content found in the article"
            return content
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return "Error fetching the content"

    def scrape_title(self, url :str) -> str:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            if response.status_code != 200:
                print(f">> Unable to scrape the article (blocked or restricted)")
                return False
        
            title = soup.title.string.strip() if soup.title else "No title found"

            # Clean up the title by removing the source name 
            delimiters = [' - ', ' | ']
            for delimiter in delimiters:
                if delimiter in title:
                    title = title.rsplit(delimiter, 1)[0].strip()
                    break

            return title
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return "Error fetching the title"
        


if __name__ == "__main__":
    consumer = Consumer()
    
    database = Database()
    database.connect()

    #while True:
    task = consumer.pop_task()
    if not task:
        print("No more tasks in the queue.")
        exit(0) # break
    
    title = consumer.scrape_title(task["url"])
    content = consumer.scrape_content(task["url"])
    summary = summarize_article(content) 

    # Save to database
    article = Article(database)
    article.save(
        url=task["url"],
        title=title if title else None,
        source=task["source"],
        summary=summary if summary else None,
        category=task["category"],
        priority=task["priority"]
    )
    database.close()
    #input("\nContinue to next article...\n")