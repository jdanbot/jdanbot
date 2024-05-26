from typing import Any, Optional
from tortoise.fields import Field

import pendulum as pdl

from datetime import datetime


def pdl_to_dt(x: pdl.DateTime) -> datetime:
    return datetime.fromisoformat(x.to_iso8601_string())


class PdlField(Field[pdl.DateTime], pdl.DateTime):
    SQL_TYPE = "TIMESTAMP"

    class _db_mysql:
        SQL_TYPE = "DATETIME(6)"

    class _db_postgres:
        SQL_TYPE = "TIMESTAMPTZ"

    class _db_mssql:
        SQL_TYPE = "DATETIME2"

    class _db_oracle:
        SQL_TYPE = "TIMESTAMP WITH TIME ZONE"

    def __init__(
        self,
        auto_now: bool = False,
        auto_now_add: bool = False,
        **kwargs: Any,
    ) -> None:
        if auto_now_add and auto_now:
            raise AttributeError(
                "You can choose only 'auto_now' or 'auto_now_add'"
            )
        super().__init__(**kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now | auto_now_add

    def to_db_value(
        self, value: Optional[pdl.DateTime], instance
    ) -> Optional[datetime]:
        # Only do this if it is a Model instance, not class. Test for guaranteed instance var
        if hasattr(instance, "_saved_in_db") and (
            self.auto_now
            or (
                self.auto_now_add
                and getattr(instance, self.model_field_name) is None
            )
        ):
            setattr(instance, self.model_field_name, value)
            return pdl_to_dt(pdl.now())

        if value is None:
            return value

        return pdl_to_dt(value)

    def to_python_value(
        self, value: datetime
    ) -> Optional[pdl.DateTime | pdl.Date | pdl.Time | pdl.Duration]:
        if value is None:
            return value

        if isinstance(value, datetime):
            return pdl.instance(value)

        return pdl.parse(value)
