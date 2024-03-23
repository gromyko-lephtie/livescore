#!/usr/bin/env python3

import ipdb
from models.__init__ import CONN, CURSOR
from lib.models.match import Match
from lib.models.event import Event

def seed_database():
    # Reset the database
    reset_database()

def reset_database():
 
    Event.drop_table()
    Match.drop_table()

    # Create new tables
    Match.create_table()
    Event.create_table()

    # Create seed data
    uefa_match = Match.create("Arsenal", "Bayern Munich")
    carabao_match = Match.create("Liverpool", "Man Utd")

    Event.create("15th", "Saka scores", uefa_match.id)
    Event.create("20th", "Kane equalized", uefa_match.id)
    Event.create("50th", "Kai scores", uefa_match.id)
    Event.create("100th", "Game over", uefa_match.id)

    Event.create("41st", "Onana saves", carabao_match.id)
    Event.create("90th", "Salah scores lol", carabao_match.id)
    Event.create("93rd", "Anthony comes in", carabao_match.id)
    Event.create("95th", "Game over", carabao_match.id)

reset_database()
ipdb.set_trace()
