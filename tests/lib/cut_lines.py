def cut_lines(text: str, lines: int = -1, start_from: int = 0) -> str:
    return "\n".join(text.split("\n")[start_from:lines])
