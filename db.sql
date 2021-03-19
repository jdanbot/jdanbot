CREATE TABLE events (
    chatid INTEGER,
    id INTEGER,
    name TEXT
);

CREATE TABLE notes (
    chatid INTEGER,
    name TEXT,
    content TEXT
);

CREATE TABLE videos (
    channelid TEXT,
    links TEXT
);

CREATE TABLE warns (
    user_id INTEGER,
    admin_id INTEGER,
    chat_id INTEGER,
    timestamp TEXT,
    reason TEXT
);
