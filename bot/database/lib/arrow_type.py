from sqlalchemy.types import DateTime
import datetime as dt
import arrow


class ArrowType(DateTime):
    @property
    def python_type(self):
        print(self)
        print("test")
        return arrow.get
        return dt.datetime

    def get_dbapi_type(self, dbapi):
        print(dbapi)
        return dbapi.DATETIME

    def _resolve_for_literal(self, value):
        print("TEST")
        with_timezone = value.tzinfo is not None
        if with_timezone and not self.timezone:
            return DATETIME_TIMEZONE
        else:
            return self

    def literal_processor(self, dialect):
        print("TeSt")
        return self._literal_processor_datetime(dialect)
