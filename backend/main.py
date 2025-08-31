from routes import ingest, retrieval
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
app = FastAPI()
app.include_router(ingest.router, prefix = "/api", tags = ['Ingestion'])
app.include_router(retrieval.router, prefix = "/api", tags = ['Retrieval'])