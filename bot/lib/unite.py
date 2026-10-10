def unite(*args, separator: str = " ", end: str = "") -> str:
    return separator.join([*args]) + end
