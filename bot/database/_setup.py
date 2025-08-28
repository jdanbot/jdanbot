import os
import sys

from tortoise import Tortoise

is_pytest_session = any("pytest" in arg for arg in sys.argv)


async def setup_db():
    if is_pytest_session:
        db_path = "test.db"
        os.system("rm test.db")
    else:
        db_path = "tortoise.db"

    await Tortoise.init(
        db_url=f"sqlite://{db_path}",
        modules={"models": ["bot.database"]},
    )

    await Tortoise.generate_schemas()
