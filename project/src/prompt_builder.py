import json
from utils import load_prompt


class PromptBuilder:

    @staticmethod
    def build_discovery_prompt(app_name, seed_url):
        prompt = load_prompt("prompts/discovery.md")
        prompt = prompt.replace("{{APP_NAME}}", app_name)
        prompt = prompt.replace("{{SEED_URL}}", seed_url)
        return prompt

    @staticmethod
    def build_research_prompt(discovery):

        prompt = load_prompt("prompts/researcher.md")

        replacements = {
            "{{APP_NAME}}": discovery["app"],
            "{{OFFICIAL_SITE}}": discovery["official_site"],
            "{{DEVELOPER_DOCS}}": discovery["developer_docs"] or "Not Available",
            "{{API_REFERENCE}}": discovery["api_reference"] or "Not Available",
            "{{AUTH_DOCS}}": discovery["authentication_docs"] or "Not Available",
            "{{PRICING}}": discovery["pricing"] or "Not Available",
            "{{WEBHOOKS}}": discovery["webhooks"] or "Not Available",
            "{{MCP}}": discovery["mcp"] or "Not Available",
        }

        for key, value in replacements.items():
            prompt = prompt.replace(key, str(value))

        return prompt

    @staticmethod
    def build_verification_prompt(discovery_result, research_result):

        prompt = load_prompt("prompts/verifier.md")

        prompt = prompt.replace(
            "{{DISCOVERY_RESULT}}",
            json.dumps(discovery_result, indent=2)
        )

        prompt = prompt.replace(
            "{{RESEARCH_RESULT}}",
            json.dumps(research_result, indent=2)
        )

        return prompt