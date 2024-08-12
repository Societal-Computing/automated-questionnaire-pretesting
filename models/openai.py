import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
MODEL = os.getenv("MODEL")
