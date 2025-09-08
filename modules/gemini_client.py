import configparser
import google.generativeai as genai
from google.generativeai.types import GenerationConfig

def configure_gemini(config: configparser.ConfigParser) -> bool:
    """Configures the Gemini API with the key from the config."""
    try:
        api_key = config.get('Gemini', 'api_key')
        genai.configure(api_key=api_key)
        return True
    except (configparser.NoSectionError, configparser.NoOptionError):
        # This case should be caught by load_config, but is here for safety
        print("Error: Could not find Gemini API key in configuration.")
        return False
    except Exception as e:
        print(f"An error occurred during Gemini configuration: {e}")
        return False


def generate_content_with_gemini(config: configparser.ConfigParser, prompt: str, json_mode: bool = False) -> str | None:
    """
    Generates content using the Gemini API based on a prompt.

    Args:
        config: The application's configuration object.
        prompt: The prompt to send to the Gemini API.
        json_mode: If True, configures the model to output JSON.

    Returns:
        The generated text content as a string, or None if an error occurs.
    """
    # Assumes genai.configure() has already been called.
    try:
        model_name = config.get('Gemini', 'model', fallback='gemini-1.5-flash')
        print(f"Generating content with Gemini model: {model_name}...")

        generation_config = None
        if json_mode:
            # This tells the model to format its response as a JSON object.
            generation_config = GenerationConfig(response_mime_type="application/json")

        model = genai.GenerativeModel(model_name, generation_config=generation_config)
        response = model.generate_content(prompt)
        print("Content generated successfully.")
        return response.text
    except Exception as e:
        # This can catch a wide range of API errors, including authentication issues
        print(f"An error occurred while generating content with Gemini: {e}")
        return None