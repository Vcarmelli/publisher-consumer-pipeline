
# Publisher Consumer Pipeline

This codebase demonstrates a **publisher–consumer pipeline** for scraping, summarizing, and storing articles using **Redis**, **MySQL**, and the **Hugging Face API**.

---

## How to Run

### Prerequisites
- Python 3.x
- Redis server
- MySQL server
- Dependencies from `requirements.txt`

---

### 1. Install Dependencies
```bash
pip install -r requirements.txt
````

---

### 2. Configure Environment

Create a `.env` file in the project root and add the following:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=articles_db
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

---

### 3. Run Services

* **Start the consumer:**

```bash
python3 app/consumer.py
```

* **Run the publisher:**

```bash
python3 app/publisher.py
```

---

## Database Configuration
The project uses a **MySQL database** to store article metadata and summaries.  
Create the table with the following schema:

```sql
CREATE TABLE IF NOT EXISTS article (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    title VARCHAR(255) NULL,
    source VARCHAR(255) NOT NULL,
    summary TEXT NULL,
    category VARCHAR(255) NOT NULL,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium'
);
```
---

## Additional Features

This includes an **article summarization feature** using the Hugging Face API.

### Summarization Workflow
1. **Retrieve content** – The consumer pops an article task from the Redis queue.  
2. **Limit input** – To avoid exceeding model constraints, only the first 3500 characters of the article are passed to the model.  
3. **Run summarization** – The Hugging Face `facebook/bart-large-cnn` model generates a concise summary of the article.  
4. **Save results** – The consumer also stores the generated summary in the MySQL database.  

---

## Running with Docker

You can run the entire project using Docker.

* **Start the containers:**

```bash
docker-compose up --build
```

* **Stop the containers:**

```bash
docker-compose down
```
