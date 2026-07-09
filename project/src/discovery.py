import json

from gemini_client import GeminiClient
from prompt_builder import PromptBuilder
from utils import clean_json_response


class DiscoveryAgent:

    def __init__(self):
        self.gemini = GeminiClient()

    def discover(self, app_name, seed_url):

        print(f"🔍 Discovering documentation for {app_name}...")

        # Build the prompt
        prompt = PromptBuilder.build_discovery_prompt(
            app_name,
            seed_url
        )

        # Send prompt to Gemini
        response = self.gemini.generate(prompt)

        # Check if Gemini request succeeded
        if not response.success:
            print(f"❌ Gemini Error: {response.error}")
            return None
            
        if not response.content:
            print("❌ Gemini Error: Response content is empty")
            return None

        # Parse Gemini JSON response
        try:
            cleaned_content = clean_json_response(response.content)
            discovery_data = json.loads(cleaned_content)
            discovery_data["app"] = app_name
            discovery_data["official_site"] = seed_url
            return discovery_data

        except json.JSONDecodeError:

            print("❌ Gemini did not return valid JSON.\n")
            print("Raw Response:\n")
            print(response.content)

            return None