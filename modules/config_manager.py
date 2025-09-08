import configparser
from pathlib import Path

CONFIG_FILE_PATH = Path(__file__).parent.parent / 'config.ini'

def _create_default_config(config_file: Path):
    """Creates a default config.ini file."""
    config = configparser.ConfigParser()
    config['Obsidian'] = {
        'vault_path': '~/Documents/ObsidianVault',
        'output_folder': 'Notes/Generated'
    }
    config['Gemini'] = {
        'api_key': 'YOUR_API_KEY_HERE',
        'model': 'gemini-1.5-flash'
    }

    try:
        with config_file.open('w') as f:
            config.write(f)
        print(f"A default 'config.ini' has been created at '{config_file}'.")
        print("Please edit it with your vault path and API key.")
    except IOError as e:
        print(f"Could not create default config file: {e}")


def load_config() -> configparser.ConfigParser | None:
    """
    Loads the configuration from config.ini, creating it if it doesn't exist.

    Returns:
        A ConfigParser object if the config is loaded and valid, otherwise None.
    """
    if not CONFIG_FILE_PATH.is_file():
        print(f"Error: Configuration file not found at '{CONFIG_FILE_PATH}'")
        _create_default_config(CONFIG_FILE_PATH)
        return None

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    # Validate essential sections and keys
    try:
        # Validate Obsidian section
        config.get('Obsidian', 'vault_path')

        # Validate Gemini section and API key
        api_key = config.get('Gemini', 'api_key')
        if not api_key or api_key == 'YOUR_API_KEY_HERE':
            print("Error: Gemini API key not found or not set in 'config.ini'.")
            print("Please get a key from Google AI Studio and add it to the [Gemini] section.")
            return None

    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Error in 'config.ini': {e}")
        print("Please ensure 'config.ini' has an [Obsidian] section with 'vault_path' and a [Gemini] section with 'api_key'.")
        return None

    return config