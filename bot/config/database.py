from ..database import *


for model in (Note, Event, CommandStats, Warn, Poll, Video,
              Pidor, PidorStats):
    model.create_table(True)


db.set_allow_sync(False)