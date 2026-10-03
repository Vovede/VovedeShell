def read_script(path: str) -> list[str]:
    with open(path, encoding="utf-8") as file:
        lines = file.readlines()

    return [
        line.strip()
        for line in lines
        if line.strip() and not line.strip().startswith("#")
    ]