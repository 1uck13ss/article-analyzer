from google.cloud import language_v1
from google import genai
from google.genai.types import HttpOptions

def call_vertex_ai_summary(text):
    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"summarise this text, {text}",
    )
    return response.text

def get_topics(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )
    response = client.classify_text(request={"document": document})
    return [{"name": c.name, "confidence": c.confidence} for c in response.categories]

def get_summary_and_topics(text):
    summary = call_vertex_ai_summary(text)
    topics = get_topics(text)
    return {
        "summary": summary,
        "topics": topics
    }