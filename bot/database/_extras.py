from typing import Any

from pypika import Field
from pypika.functions import Function


class JsonSet(Function):
    def __init__(
        self, x: Field | str, path: str, *p, alias=None
    ):
        super(JsonSet, self).__init__(
            "json_set", x, path, *p, alias=alias
        )


class Json(Function):
    def __init__(self, value: Any, alias=None):
        super(Json, self).__init__(
            "json", value, alias=alias
        )


class IsInserted(Function):
    def __init__(self):
        super(IsInserted, self).__init__(
            "_rowid_ = last_insert_rowid"
        )


class Unixepoch(Function):
    def __init__(self):
        super(Unixepoch, self).__init__("unixepoch")


class Random(Function):
    def __init__(self):
        super(Random, self).__init__("random")
