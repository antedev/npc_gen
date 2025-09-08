# Obsidian Note Creator

This Python script automatically generates Markdown (`.md`) files formatted for use in Obsidian.

## Features

- Creates `.md` files with YAML frontmatter (title, date, tags).
- Configurable output directory via `config.ini`.
- Example usage included in the script.

## Setup

1.  **Install Python:** Make sure you have Python 3.7+ installed.

2.  **Configure the script:**
    - Open the `config.ini` file.
    - Set `vault_path` to the absolute path of your Obsidian vault.
    - Set `output_folder` to the desired subfolder within your vault where notes will be created.

## Usage

Run the script from your terminal within the `obsidian_creator` directory:

```bash
python create_note.py
```

This will execute the example code in the `if __name__ == '__main__':` block, creating a new note in your specified Obsidian vault location. You can customize this block to generate any note you need.