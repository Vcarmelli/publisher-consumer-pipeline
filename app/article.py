from mysql.connector import Error

class Article:
    def __init__(self, database):
        self.db_manager = database
        if not self.db_manager.connected:
            self.db_manager.connect()

    def is_duplicate(self, url):

        try:
            cursor = self.db_manager.db.cursor()
            query = "SELECT COUNT(*) FROM article WHERE url = %s"
            cursor.execute(query, (url,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            print(f"Error checking for duplicates: {e}")
            return False

    def save(self, url, title, source, summary, category, priority):

        if self.is_duplicate(url):
            print(f">> Duplicate found. Article already in the database.")
            return 

        try:
            article = {
                'url': url,
                'title': title,
                'source': source,
                'summary': summary,
                'category': category,
                'priority': priority
            }
            self.db_manager.save_article(article)
            return True
        except Error as e:
            print(f"Error saving the article: {e}")
            return False
