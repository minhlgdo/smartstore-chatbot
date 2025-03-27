import openai

from app.variables import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
client = openai.OpenAI()