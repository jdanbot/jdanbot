from aiosqlite import connect

from .chat import Chat, ChatSettings
from .command import Command
from .member import Member
from .note import Note
from .pidor import PidorTop
from .user import User
from .warn import Warn


async def setup_db():
    async with connect("tortoise.db") as conn:
        await conn.execute("""
CREATE TABLE if not exists "chat" (
	"id"	INTEGER NOT NULL,
	"title"	TEXT NOT NULL,
	"username"	TEXT,
	"language"	TEXT,
	"pidor_id"	INT,
	"settings"	JSONB,
	PRIMARY KEY("id" AUTOINCREMENT)
);          
        """)

        await conn.execute("""
CREATE TABLE if not exists "command" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "chat_id" INT NOT NULL,
    "user_id" INT NOT NULL,
    "name" TEXT NOT NULL,
    "args" TEXT NOT NULL
);           
        """)
        await conn.execute("""
CREATE TABLE if not exists "note" (
	"id"	INTEGER NOT NULL,
	"chat_id"	INT NOT NULL,
	"name"	TEXT NOT NULL,
	"text"	TEXT NOT NULL,
	"author_id"	INT NOT NULL,
	"created_at"	INT DEFAULT CURRENT_TIMESTAMP,
	"editor_id"	INT,
	"updated_at"	INT,
	"is_locked" INT DEFAULT 0,
	UNIQUE("chat_id","name"),
	PRIMARY KEY("id" AUTOINCREMENT)
)
        """)

        await conn.execute("""
CREATE TABLE if not exists "pidor" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "chat_id" INT NOT NULL,
    "is_allowed" INT NOT NULL DEFAULT 1,
    "latest_time" INT,
    "user_id" BIGINT NOT NULL
)           
        """)
        await conn.execute("""
CREATE TABLE if not exists "pidorevent" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "chat_id" INT NOT NULL,
    "caused_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "pidor_id" INT NOT NULL
)           
        """)
        
        await conn.execute("""
CREATE TABLE if not exists "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT,
    "username" TEXT
)           
        """)
        
        await conn.execute("""
CREATE TABLE if not exists "warns" (
	"id"	INTEGER NOT NULL,
	"chat_id"	INTEGER NOT NULL,
	"victim_id"	INTEGER NOT NULL,
	"warn_admin_id"	INTEGER NOT NULL,
	"reason"	VARCHAR(255) NOT NULL,
	"warned_at"	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"unwarn_admin_id"	INTEGER,
	"unwarn_reason"	VARCHAR(255),
	"unwarned_at"	DATETIME,
	PRIMARY KEY("id")
)           
        """)
        await conn.commit()


__all__ = (
    User,
    Chat,
    ChatSettings,
    Member,
    PidorTop,
    Command,
    Note,
    Warn,
    setup_db,
)
