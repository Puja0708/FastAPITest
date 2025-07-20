from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.openai import OpenAIProvider
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")   
    
conversation_summarizer_llm = GeminiModel(
    'gemini-2.0-flash', 
    provider='google-gla'
)
