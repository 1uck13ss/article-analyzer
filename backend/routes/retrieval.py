from fastapi import APIRouter
from google.cloud import storage
import json

router = APIRouter()

@router.get("/retrieve")
def retrieve_article():
    
    client = storage.Client()
    bucket = client.bucket("reading-tracker-submissions")
    blobs = list(bucket.list_blobs(prefix = "submissions/"))
    blobs.sort(key=lambda b: b.time_created, reverse=True)

    articles = []
    for blob in blobs:
        try:
            content = blob.download_as_text()
            data = json.loads(content)
            metadata = data.get("metadata", {})
            summary = data.get("summary", {})
            articles.append({"metadata": metadata, "summary": summary})        
        except Exception as e:
            print(f"Failed to parse blob {blob.name}: {e}")

    return articles
