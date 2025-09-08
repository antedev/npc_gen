import sys
import argparse
import json
import configparser

from modules.config_manager import load_config
from modules.gemini_client import configure_gemini, generate_content_with_gemini
from create_note import create_npc_note


def generate_npc_concept(config: configparser.ConfigParser) -> dict | None:
    """
    Uses Gemini to generate a unique NPC name and description.

    Returns:
        A dictionary with 'name' and 'description' keys, or None on failure.
    """
    prompt = """
You are a fantasy world-building assistant skilled at creating memorable characters.
Your task is to invent a concept for a unique Non-Player Character (NPC).

Provide your response as a JSON object with two keys:
1. "name": A creative and fitting name for the NPC (e.g., "Kaelen the Silent" or "Mistress Vex").
2. "description": A one-sentence description of the NPC's core concept (e.g., "A disgraced royal cartographer selling forged maps to survive.").

Respond ONLY with the JSON object. Do not include any explanatory text or markdown formatting.
"""
    print("Generating a new NPC concept...")
    json_string = generate_content_with_gemini(config, prompt, json_mode=True)
    if not json_string:
        print("Failed to generate NPC concept.")
        return None

    try:
        concept = json.loads(json_string)
        if 'name' in concept and 'description' in concept:
            return concept
        else:
            print("Error: Generated JSON is missing 'name' or 'description' key.")
            return None
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON concept from Gemini.")
        print(f"Received: {json_string}")
        return None


def main():
    """Main execution function for the orchestrator."""
    parser = argparse.ArgumentParser(description="Generate multiple NPC notes for Obsidian using Gemini.")
    parser.add_argument("count", type=int, nargs='?', default=1, help="The number of NPCs to generate (default: 1).")
    args = parser.parse_args()

    config = load_config()
    if not config or not configure_gemini(config):
        sys.exit(1)

    print(f"Starting generation of {args.count} NPC(s).")
    for i in range(args.count):
        print(f"\n--- Generating NPC {i + 1} of {args.count} ---")

        concept = generate_npc_concept(config)

        if concept:
            create_npc_note(config, concept['name'], concept['description'])
        else:
            print("Skipping this NPC due to concept generation failure.")


if __name__ == '__main__':
    main()