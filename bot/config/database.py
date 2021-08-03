from ..database import *


db.connect()
db.create_tables((Note, Event, CommandStats, Warn, Poll, Video,
                  Pidor, PidorStats), safe=True)
db.close()

db.set_allow_sync(False)