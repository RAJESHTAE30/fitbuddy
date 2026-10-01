from functools import lru_cache
from .config import GEMINI_API_KEY, WORKOUT_MODEL, TIP_MODEL

@lru_cache(maxsize=1)
def get_client():
    if not GEMINI_API_KEY:
        return None
    from google import genai
    return genai.Client(api_key=GEMINI_API_KEY)

def generate_text(prompt: str, model: str) -> str:
    client = get_client()
    if client is None:
        raise RuntimeError(
            "Gemini API key is not configured. Add GEMINI_API_KEY to your .env file."
        )
    response = client.models.generate_content(model=model, contents=prompt)
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
