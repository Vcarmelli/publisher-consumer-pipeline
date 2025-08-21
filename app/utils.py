import redis
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


def get_redis_client():
    load_dotenv()
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_db = int(os.getenv("REDIS_DB", 0))
    return redis.Redis(host=redis_host, port=redis_port,  db=redis_db, decode_responses=True)


def summarize_article(content) -> str:
    load_dotenv()
    if not content:
        return

    try:
        client = InferenceClient(
            provider="hf-inference",
            api_key=os.getenv("HF_TOKEN")
        )

        result = client.summarization(content[:3500], model="facebook/bart-large-cnn") # limit to 3500 characters
        print(f"\nSUMMARY: {result.summary_text}")

        return result.summary_text

    except Exception as e:
        print(f"Summarization failed: {e}")


