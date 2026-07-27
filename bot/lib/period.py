from datetime import timedelta

"""
https://stackoverflow.com/questions/538666/format-timedelta-to-string#62719270
"""


def period(delta: timedelta, pattern: str) -> str:
    d = {"d": delta.days}
    d["h"], rem = divmod(delta.seconds, 3600)
    d["m"], d["s"] = divmod(rem, 60)

    return pattern.format(**d)
