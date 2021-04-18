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
    timestamp INTEGER,
    reason TEXT
);

CREATE TABLE pidors (
    chat_id INTEGER,
    user_id INTEGER,
    timestamp INTEGER
);

CREATE TABLE pidorstats (
    chat_id INTEGER,
    user_id INTEGER,
    username TEXT,
    count INTEGER
);

CREATE TABLE polls (
    chat_id INTEGER,
    user_id INTEGER,
    poll_id INTEGER,
    description TEXT,
    timestamp INTEGER
);
