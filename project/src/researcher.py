import json

from gemini_client import GeminiClient
from prompt_builder import PromptBuilder
from utils import clean_json_response


class ResearchAgent:

    def __init__(self):
        self.gemini = GeminiClient()

    def research(self, discovery_result):

        print(f"🧠 Researching {discovery_result['app']}...")

        prompt = PromptBuilder.build_research_prompt(
            discovery_result
        )

        response = self.gemini.generate(prompt)

        if not response.success:
            print(response.error)
            return None
            
        if not response.content:
            print("❌ Gemini Error: Response content is empty")
            return None

        try:
            cleaned_content = clean_json_response(response.content)
            return json.loads(cleaned_content)

        except json.JSONDecodeError:

            print("❌ Invalid JSON from Gemini\n")
            print(response.content)

            return None
