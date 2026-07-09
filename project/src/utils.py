import csv
import json
import os


def load_apps(csv_path):

    apps = []

    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            apps.append(row)

    return apps


def load_prompt(prompt_path):

    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()


def save_json(data, filepath):

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def clean_json_response(text):

    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    if text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def apply_verification(research, verification):

    updated = research.copy()

    for change in verification.get("changes", []):
        updated[change["field"]] = change["new"]

    updated["verified"] = verification.get("verified", False)
    updated["confidence"] = verification.get("confidence", 0)
    updated["verification_notes"] = verification.get("notes", "")

    return updated