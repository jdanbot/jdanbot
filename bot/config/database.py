from ..database import db, Note, Command, \
                       Warn, Poll, Feed, Pidor, User, Chat, ChatMember


db.connect()
db.create_tables((Note, Command, Warn, Poll, Feed, Pidor,
                  User, Chat, ChatMember), safe=True)
db.close()
