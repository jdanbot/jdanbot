import sqlite3
from importlib.machinery import SourceFileLoader
from pathlib import Path

from ..config.logger import logger

db = sqlite3.connect("jdanbot.db")
migrations = sorted(Path("migrations").glob("*.py"))


class MigratorService:
    @classmethod
    def activate_migrations(cls) -> bool:
        migrations_to_activate = (
            cls.get_count_of_available_migrations()
            - cls.get_count_of_active_migrations()
        )

        results: list[bool] = []

        for migration in migrations[
            -migrations_to_activate:
        ]:
            foo = SourceFileLoader(
                "test", migration.__str__()
            ).load_module()

            logger.debug(
                f"runned migration {migration.__str__()}"
            )
            results.append(foo.migrate(db))
            logger.debug(
                f"migration {migration.__str__()} successfuly ended"
            )

        return all(results)

    @classmethod
    def get_count_of_active_migrations(cls) -> int:
        return db.execute(
            "SELECT count(*) FROM migratehistory;"
        ).fetchone()[0]

    @classmethod
    def get_count_of_available_migrations(cls) -> int:
        return len(migrations)
