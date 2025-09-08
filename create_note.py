import configparser
from pathlib import Path
import datetime


def create_obsidian_note(title: str, content: str, tags: list[str] = None):
    """
    Creates a new note in the Obsidian vault specified in the config file.

    Args:
        title: The title of the note. This will also be the filename.
        content: The main content of the note in Markdown format.
        tags: A list of tags to add to the note's frontmatter.
    """
    # 1. Read configuration from config.ini
    config = configparser.ConfigParser()
    config_file = Path(__file__).parent / 'config.ini'

    if not config_file.is_file():
        print(f"Error: Configuration file not found at '{config_file}'")
        _create_default_config(config_file)
        print("A default 'config.ini' has been created. Please edit it with your vault path.")
        return

    config.read(config_file)

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

    full_content = frontmatter + f"# {title}\n\n" + content

    # 4. Write the note to the file
    if output_file.exists():
        print(f"Note '{output_file}' already exists. Skipping creation.")
        return

    try:
        output_file.write_text(full_content, encoding='utf-8')
        print(f"Successfully created note: {output_file}")
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}")


def _create_default_config(config_file: Path):
    """Creates a default config.ini file."""
    config = configparser.ConfigParser()
    config['Obsidian'] = {
        'vault_path': '~/Documents/ObsidianVault',
        'output_folder': 'Notes/Generated'
    }
    try:
        with config_file.open('w') as f:
            config.write(f)
    except IOError as e:
        print(f"Could not create default config file: {e}")


def read_obsidian_note(title: str) -> str | None:
    """
    Reads an existing note from the Obsidian vault.
    It searches the entire vault recursively for a file matching the given title.

    Args:
        title: The title of the note to read. This will be sanitized to create a filename.

    Returns:
        The content of the note as a string if found, otherwise None.
    """
    # 1. Read configuration from config.ini
    config = configparser.ConfigParser()
    config_file = Path(__file__).parent / 'config.ini'

    if not config_file.is_file():
        print(f"Error: Configuration file not found at '{config_file}'")
        return None

    config.read(config_file)

    try:
        # Use .expanduser() to handle '~' in the path
        vault_path = Path(config.get('Obsidian', 'vault_path')).expanduser()
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Error in 'config.ini': {e}")
        print("Please ensure 'config.ini' has an [Obsidian] section with a 'vault_path' key.")
        return None

    # 2. Prepare file name for searching
    # Sanitize title to create a valid filename to search for
    safe_filename = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
    note_filename_to_find = f"{safe_filename}.md"

    # 3. Search for the note file recursively in the vault path
    found_notes = list(vault_path.rglob(note_filename_to_find))

    if not found_notes:
        print(f"Note '{title}' not found in the vault at '{vault_path}'.")
        return None

    if len(found_notes) > 1:
        print(f"Warning: Found multiple notes with the name '{safe_filename}.md'.")
        print("Returning the first one found:")
        for note in found_notes:
            print(f"- {note}")

    note_path = found_notes[0]

    # 4. Read the note content
    try:
        content = note_path.read_text(encoding='utf-8')
        print(f"Successfully read note: {note_path}")
        return content
    except IOError as e:
        print(f"Error reading file {note_path}: {e}")
        return None


if __name__ == '__main__':
    # --- Example Usage ---
    # You can call create_obsidian_note() with your desired title, content, and tags.

    note_title = "My First Auto-Generated Note"
    note_content = (
        "This is a note generated by a Python script.\n\n"
        "It supports standard Markdown:\n"
        "- Lists\n"
        "- **Bold** and *italic* text\n\n"
        "It can also include Obsidian-style [[wikilinks]] to other notes, like [[Another Note]]."
    )
    note_tags = ["python", "automation", "testing"]

    create_obsidian_note(note_title, note_content, note_tags)

    # --- Example of reading a note ---
    print("\n" + "="*20)
    print("DEMO: Reading a note")
    print("="*20)
    # Try to read the note we just created
    read_title = "My First Auto-Generated Note"
    note_content_read = read_obsidian_note(read_title)

    if note_content_read:
        print(f"\n--- Content of '{read_title}' ---\n")
        print(note_content_read)
        print("------------------------------------")

    # Example of reading a note that might not exist
    read_nonexistent_title = "A Note That Does Not Exist"
    print(f"\n--- Attempting to read a non-existent note: '{read_nonexistent_title}' ---")
    read_obsidian_note(read_nonexistent_title)
    print("-----------------------------------------------------------------")