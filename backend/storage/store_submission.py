from google.cloud import storage
import json

def store_submission(user_id, submission_id, metadata, summary, topics):
    try:
        client = storage.Client()
        bucket = client.bucket("reading-tracker-submissions")
        blob_path = f"submissions/{submission_id}.json"
        blob = bucket.blob(blob_path)
        blob.upload_from_string(json.dumps({"metadata": metadata, "summary": summary, "topics": topics}))
        return submission_id
    except Exception as e:
        logging.error(f"Error storing submission: {str(e)}")