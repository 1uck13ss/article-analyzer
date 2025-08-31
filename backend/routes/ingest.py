from fastapi import APIRouter
from pydantic import BaseModel
from newspaper import Article
from services.extract_metadata import extract_metadata
from services.extract_text import extract_text
from storage.store_submission import store_submission
from services.get_summary_and_topic import get_summary_and_topics
from google.cloud import storage
import hashlib
import json
import logging

router = APIRouter()

class Submission(BaseModel):
    user_id: str
    content: str

def generate_submission_id(text):
    return hashlib.sha256(text.encode()).hexdigest()

def check_submission_exists(submission_id):
    try:
        client = storage.Client()
        bucket = client.bucket("reading-tracker-submissions")
        blob = bucket.blob(f"submissions/{submission_id}.json")
        return blob.exists()

    except Exception as e:
        logging.error(f"Error checking submission: {str(e)}")
        return False

@router.post("/submit")
def submit_article(submission: Submission):
    try:
        article = Article(submission.content)
        article.download()
        article.parse()
        metadata = extract_metadata(article)
        text = extract_text(article)
        submission_id = generate_submission_id(text)

        client = storage.Client()
        bucket = client.bucket("reading-tracker-submissions")
        blob = bucket.blob(f"submissions/{submission_id}.json")
        if blob.exists():
            return json.loads(blob.download_as_text())
        
        result = get_summary_and_topics(text)
        summary = result["summary"]
        topics = result["topics"]
        store_submission(submission.user_id, submission_id, metadata, summary, topics)
        return {"submission_id": submission_id, "metadata": metadata, "summary": summary, "topics": topics}
    except Exception as e:
        logging.error(f"Error processing article: {str(e)}")