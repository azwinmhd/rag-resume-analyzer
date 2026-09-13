from dotenv import load_dotenv
import os

print("Current folder:", os.getcwd())

loaded = load_dotenv()

print("Dotenv loaded:", loaded)

key = os.getenv("GOOGLE_API_KEY")

print("Loaded:", key is not None)