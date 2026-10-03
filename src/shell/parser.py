def parse_command(line: str) -> tuple[str, list[str]]:
    parts = line.strip().split()

    if not parts:
        return "", []

    return parts[0], parts[1:]