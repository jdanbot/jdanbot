import sqlite3
from importlib.machinery import SourceFileLoader
from operator import sub
from pathlib import Path

from loguru import logger

db = sqlite3.connect("jdanbot.db")
migrations = sorted(Path("migrations").glob("*.py"))


class MigratorService:
    @classmethod
    def activate_migrations(cls) -> bool:
        migrations_to_activate = sub(
            cls.get_count_of_available_migrations(),
            cls.get_count_of_active_migrations(),
        )

        results: list[bool] = []
        from_which = (
            len(migrations) - migrations_to_activate
        )

        for migration in migrations[from_which:]:
            foo = SourceFileLoader(
                "test", migration.__str__()
            ).load_module()

            logger.debug(
                f"runned migration {migration.__str__()}"
            )
            results.append(foo.migrate(db))
            logger.debug(
                f"migration {migration.__str__()} successfully ended"
            )
            new_id = int(
                migration.name.split("_", maxsplit=1)[0]
            )
            db.execute(
                "INSERT INTO migratehistory(id, name, migrated_at) "
                f'VALUES ({new_id}, "{migration.name}", CURRENT_TIMESTAMP);'
            )
            db.commit()

        return all(results)

    @classmethod
    def get_count_of_active_migrations(cls) -> int:
        try:
            return db.execute(
                "SELECT count(*) FROM migratehistory;"
            ).fetchone()[0]
        except sqlite3.OperationalError:
            return cls.get_count_of_available_migrations()

    @classmethod
    def get_count_of_available_migrations(cls) -> int:
        return len(migrations)
