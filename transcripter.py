from openai import OpeanAI
import os
from dotenv import load_dotenv

load_dotenv()

my_key_openai = os.getenv("openai_apikey")

client = OpenAI(
    api_key=my_key_openai
)