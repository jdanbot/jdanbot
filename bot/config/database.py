from ..database import db, Note, Event, Command, \
                       Warn, Poll, Feed, Pidor, PidorStats


db.connect()
db.create_tables((Note, Event, Command, Warn, Poll, Feed,
                  Pidor, PidorStats), safe=True)
db.close()
