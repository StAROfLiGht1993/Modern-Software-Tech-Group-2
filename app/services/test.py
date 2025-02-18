import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("OPENAI_API_KEY"))  # This should print your actual API key
