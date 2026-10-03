def parse_command(line: str) -> tuple[str, list[str]]:
    """Split command line into command and arguments."""
    parts = line.strip().split()

    if not parts:
        return "", []

    return parts[0], parts[1:]