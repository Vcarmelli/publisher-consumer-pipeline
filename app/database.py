import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


class Database:
    def __init__(self):
        self.connected = False
        
        self.db_host = os.getenv("MYSQL_HOST", "localhost")
        self.db_user = os.getenv("MYSQL_USER", "root")
        self.db_password = os.getenv("MYSQL_PASSWORD", "")
        self.db_name = os.getenv("MYSQL_DATABASE", "consumer_articles")

        conn = mysql.connector.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password
        )

        # Create database if it doesn't exist
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS consumer_articles")

    def connect(self):
        load_dotenv()

        if self.connected:
            return

        self.db = mysql.connector.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name
        )
        self.connected = True
        self.create_table()
        print(f"Connected to database {self.db.database} successfully.\n")

    def create_table(self):
        try:
            cursor = self.db.cursor()
            create_table_query = """
                CREATE TABLE IF NOT EXISTS article (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    url VARCHAR(255) NOT NULL,
                    title VARCHAR(255) NULL,
                    source VARCHAR(255) NOT NULL,
                    summary TEXT NULL,
                    category VARCHAR(255) NOT NULL,
                    priority ENUM('low', 'medium', 'high') DEFAULT 'medium'
                )
            """
            cursor.execute(create_table_query)
            self.db.commit()
        except Error as e:
            print(f"Error creating table: {e}")
            return False
        
    def save_article(self, article):
        if not self.connected:
            raise Exception("Database not connected. Call connect() first.")

        try:
            cursor = self.db.cursor()
            insert_query = """
                INSERT INTO article (url, title, source, summary, category, priority)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                article['url'],
                article['title'],
                article['source'],
                article['summary'],
                article['category'],
                article['priority']
            ))
            self.db.commit()
            print(f">> Article saved: {article['title'] if article['title'] else 'No title'}")
        except Error as e:
            print(f"Error saving article: {e}")

    def close(self):
        if self.connected:
            self.db.close()
            self.connected = False