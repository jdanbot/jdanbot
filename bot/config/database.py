from ..database import db, Note, Event, CommandStats, \
                       Warn, Poll, Video, Pidor, PidorStats


db.connect()
db.create_tables((Note, Event, CommandStats, Warn, Poll, Video,
                  Pidor, PidorStats), safe=True)
db.close()
