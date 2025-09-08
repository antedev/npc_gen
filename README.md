# Obsidian Note Creator

This Python script automatically generates Markdown (`.md`) files formatted for use in Obsidian.

## Features

- Creates `.md` files with YAML frontmatter (title, date, tags).
- Configurable output directory via `config.ini`.
- Example usage included in the script.

## Setup

1.  **Install Python:** Make sure you have Python 3.7+ installed.
2.  **Install Dependencies:** Install the required Python packages.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure the script:**
    - Open the `config.ini` file.
    - In the `[Obsidian]` section, set `vault_path` to the absolute path of your Obsidian vault and `output_folder` to the desired subfolder.
    - In the `[Gemini]` section, set `api_key` to your Gemini API key. You can get a key from Google AI Studio.

    > **Note:** The `config.ini` is ignored by git (via `.gitignore`) to protect your API key.

## Usage

There are two ways to use this tool.

### Generating a Specific NPC

To create a single NPC with a name and concept you provide, use `create_note.py`.

**Syntax:**
```bash
python create_note.py "NPC Name" "Brief description of the NPC"
```

**Example:**

```bash
python create_note.py "Gorok the Blacksmith" "A gruff but skilled blacksmith who lost his family in the war."
```

This will execute the example code in the `if __name__ == '__main__':` block, creating a new note in your specified Obsidian vault location. You can customize this block to generate any note you need.