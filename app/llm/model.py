import getpass
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
