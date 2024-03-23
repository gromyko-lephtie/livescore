#!/usr/bin/env python3

from models.__init__ import CONN, CURSOR
from models.match import Match
from models.event import Event
def seed_database():
    Event.drop_table()
    Match.drop_table()
    Match.create_table()
    Event.create_table()

    # Create seed data
    Uefa = Match.create("Arsenal", "Bayern Munich")
    Carabao = Match.create("Liverpool", "Man Utd")
    Event.create("15th", "Saka scores", Uefa.id)
    Event.create("20th", "Kane equalized", Uefa.id)
    Event.create("50th", "kai scores ", Uefa.id)
    Event.create("1000th", "game over", Uefa.id)
    Event.create("41st", "Onana saves", Carabao.id)
    Event.create("90th", "Salah scores lol", Carabao.id)
    Event.create("93rd", "Anthony comes in", Carabao.id)
    Event.create("95th", "HAHAHAHA game over", Carabao.id)


seed_database()
print("Seeded database")
