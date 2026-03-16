"""File I/O utility functions."""


def read_text_file(file_path, encoding="utf-8"):
    """Read text file and return contents.

    Args:
        file_path: Path to file to read
        encoding: File encoding (default: utf-8)

    Returns:
        String with file contents

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    with open(file_path, encoding=encoding) as f:
        return f.read()


def write_text_file(file_path, content, encoding="utf-8"):
    """Write text content to file.

    Args:
        file_path: Path to file to write
        content: Text content to write
        encoding: File encoding (default: utf-8)

    Returns:
        None
    """
    with open(file_path, "w", encoding=encoding) as f:
        f.write(content)
