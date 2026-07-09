import json

from gemini_client import GeminiClient
from prompt_builder import PromptBuilder
from utils import clean_json_response


class VerificationAgent:

    def __init__(self):
        self.gemini = GeminiClient()

    def verify(self, discovery_result, research_result):

        print("✅ Verifying research...")

        prompt = PromptBuilder.build_verification_prompt(
            discovery_result, research_result
        )

        response = self.gemini.generate(prompt)

        # Proactively fixed to dot notation to avoid dict index crash
        if not response.success:
            print(response.error)
            return None
            
        # Add safety check for empty response
        if not response.content:
            print("❌ Gemini Error: Response content is empty")
            return None

        try:
            # Proactively fixed to dot notation
            cleaned = clean_json_response(
                response.content
            )

            return json.loads(cleaned)

        except Exception:

            print(response.content)
            return None