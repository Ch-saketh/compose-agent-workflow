import os

from dotenv import load_dotenv
from google import genai
from models import GeminiResponse

load_dotenv()


class GeminiClient:

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model = "gemini-2.5-flash"

    def generate(self, prompt):

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            return GeminiResponse(
                success=True,
                content=response.text,
                usage=getattr(response, "usage_metadata", None),
                error=None
            )

        except Exception as e:

            return GeminiResponse(
                success=False,
                content=None,
                usage=None,
                error=str(e),
            )