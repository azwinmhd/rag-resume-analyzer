import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv("YOUR_SECRET_FILE_NAME")  # if not using .env

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

for model in genai.list_models():
    if "gemini" in model.name.lower():
        print(model.name)