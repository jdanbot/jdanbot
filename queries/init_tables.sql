-- name: init_tables#
CREATE TABLE IF NOT EXISTS "chats" (
    "id"       INTEGER    PRIMARY KEY NOT NULL,
    "username" TEXT,
    "title"    TEXT       NOT NULL,
    "language" VARCHAR(2),
    "pidor_id" INTEGER,
    "settings" JSONB      NOT NULL DEFAULT "{}"
);

CREATE TABLE IF NOT EXISTS "commands" (
    "id"          INTEGER   PRIMARY KEY NOT NULL,
    "chat_id"     INTEGER   NOT NULL,
    "user_id"     INTEGER   NOT NULL,
    "name"        TEXT      NOT NULL,
    "args"        TEXT      NOT NULL,
    "executed_at" TIMESTAMP NOT NULL DEFAULT (unixepoch())
);

CREATE TABLE IF NOT EXISTS "notes" (
    "id"         INTEGER     PRIMARY KEY NOT NULL,
    "chat_id"    INTEGER     NOT NULL,
    "name"       VARCHAR(50) NOT NULL,
    "text"       TEXT        NOT NULL,
    "author_id"  INTEGER     NOT NULL,
    "created_at" TIMESTAMP   NOT NULL DEFAULT (unixepoch()),
    "editor_id"  INTEGER,
    "updated_at" TIMESTAMP,
    "is_locked"  BOOLEAN     DEFAULT 0,
                 UNIQUE ("chat_id", "name")
);

CREATE TABLE IF NOT EXISTS "pidors" (
    "id"          INTEGER PRIMARY KEY NOT NULL,
    "chat_id"     INTEGER NOT NULL,
    "user_id"     INTEGER NOT NULL,
    "is_allowed"  BOOLEAN NOT NULL DEFAULT 1,
    "latest_time" INTEGER,
                  UNIQUE ("chat_id", "user_id")
);

CREATE TABLE IF NOT EXISTS "pidor_events" (
    "id"        INTEGER   PRIMARY KEY NOT NULL,
    "chat_id"   INTEGER   NOT NULL,
    "pidor_id"  INTEGER   NOT NULL,
    "caused_at" TIMESTAMP NOT NULL DEFAULT (unixepoch())
);

CREATE TABLE IF NOT EXISTS "users" (
    "id"         INTEGER PRIMARY KEY NOT NULL,
    "first_name" TEXT    NOT NULL,
    "last_name"  TEXT,
    "username"   TEXT
);

CREATE TABLE IF NOT EXISTS "warns" (
    "id"              INTEGER      PRIMARY KEY NOT NULL,
    "chat_id"         INTEGER      NOT NULL,
    "victim_id"       INTEGER      NOT NULL,
    "warn_admin_id"   INTEGER      NOT NULL,
    "reason"          VARCHAR(255) NOT NULL,
    "warned_at"       TIMESTAMP    NOT NULL DEFAULT (unixepoch()),
    "unwarn_admin_id" INTEGER,
    "unwarn_reason"   VARCHAR(255),
    "unwarned_at"     TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "members" (
    "id"                INTEGER   PRIMARY KEY NOT NULL,
    "chat_id"           INTEGER   NOT NULL,
    "user_id"           INTEGER   NOT NULL,
    "pidor_id"          INTEGER,
    "joined_at"         TIMESTAMP DEFAULT (unixepoch()),
    "is_captcha_passed" BOOLEAN   DEFAULT 0,
    "is_admin"          INTEGER,
                        UNIQUE(chat_id, user_id)
);
