import configparser
from pathlib import Path
import datetime

def create_obsidian_note(config: configparser.ConfigParser, title: str, content: str, tags: list[str] = None):
    """
    Creates a new note in the Obsidian vault specified in the config file.

    Args:
        config: The application's configuration object.
        title: The title of the note. This will also be the filename.
        content: The main content of the note in Markdown format.
        tags: A list of tags to add to the note's frontmatter.
    """
    # 1. Get paths from configuration
    try:
        # Use .expanduser() to handle '~' in the path
        vault_path = Path(config.get('Obsidian', 'vault_path')).expanduser()
        output_folder = config.get('Obsidian', 'output_folder', fallback='.')
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Error in 'config.ini': {e}")
        print("Please ensure 'config.ini' has an [Obsidian] section with a 'vault_path' key.")
        return

    # 2. Prepare file path and name
    # Sanitize title to create a valid filename
    safe_filename = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
    output_dir = vault_path / output_folder
    output_file = output_dir / f"{safe_filename}.md"

    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # 3. Prepare note content with YAML frontmatter (common in Obsidian)
    frontmatter = f"---\n"
    frontmatter += f"title: {title}\n"
    frontmatter += f"date: {datetime.datetime.now().isoformat()}\n"
    if tags:
        frontmatter += f"tags:\n"
        for tag in tags:
            frontmatter += f"  - {tag}\n"
    frontmatter += f"---\n\n"

    full_content = frontmatter + content

    # 4. Write the note to the file
    if output_file.exists():
        print(f"Note '{output_file}' already exists. Skipping creation.")
        return

    try:
        output_file.write_text(full_content, encoding='utf-8')
        print(f"Successfully created note: {output_file}")
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}")