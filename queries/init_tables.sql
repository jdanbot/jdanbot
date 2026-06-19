-- name: init_tables#
CREATE TABLE if not exists "chats" (
	"id"	INTEGER NOT NULL,
	"title"	TEXT NOT NULL,
	"username"	TEXT,
	"language"	VARCHAR(2),
	"pidor_id"	INT,
	"settings"	JSONB NOT NULL DEFAULT "{}",
	PRIMARY KEY("id" AUTOINCREMENT)
);          

CREATE TABLE if not exists "commands" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "chat_id" INT NOT NULL,
    "user_id" INT NOT NULL,
    "name" TEXT NOT NULL,
    "args" TEXT NOT NULL
);           

CREATE TABLE if not exists "notes" (
	"id"	INTEGER NOT NULL,
	"chat_id"	INT NOT NULL,
	"name"	TEXT NOT NULL,
	"text"	TEXT NOT NULL,
	"author_id"	INT NOT NULL,
	"created_at"	INT NOT NULL DEFAULT (unixepoch()),
	"editor_id"	INT,
	"updated_at"	INT,
	"is_locked" BOOLEAN DEFAULT 0,
	UNIQUE("chat_id","name"),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE if not exists "pidors" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "chat_id" INT NOT NULL,
    "user_id" INT NOT NULL,
    "is_allowed" BOOLEAN NOT NULL DEFAULT 1,
    "latest_time" INT,
	UNIQUE("chat_id","user_id")
);

CREATE TABLE if not exists "pidor_events" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "chat_id" INT NOT NULL,
    "pidor_id" INT NOT NULL,
    "caused_at" INTEGER NOT NULL DEFAULT (unixepoch())
);

CREATE TABLE if not exists "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT,
    "username" TEXT
);

CREATE TABLE if not exists "warns" (
	"id"	INTEGER NOT NULL,
	"chat_id"	INTEGER NOT NULL,
	"victim_id"	INTEGER NOT NULL,
	"warn_admin_id"	INTEGER NOT NULL,
	"reason"	VARCHAR(255) NOT NULL,
	"warned_at"	INTEGER NOT NULL DEFAULT (unixepoch()),
	"unwarn_admin_id"	INTEGER,
	"unwarn_reason"	VARCHAR(255),
	"unwarned_at"	INTEGER,
	PRIMARY KEY("id")
);

CREATE TABLE if not exists "members" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "chat_id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    "pidor_id" INTEGER,
    "when_joined" DATETIME,
    "is_admin" INTEGER
);
