from models.match import Match
from models.event import Event


def exit_program():
    print("Goodbye!")
    exit()



def list_matches():
    matches = Match.get_all()
    for match in matches:
        print(match)


def find_match_by_home():
    home = input("Enter the match's home: ")
    match = Match.find_by_home (home)
    print(match) if match else print(
        f'Match {home} not found')


def find_match_by_id():
    # use a trailing underscore not to override the built-in id function
    id_ = input("Enter the matche's id: ")
    match = Match.find_by_id(id_)
    print(match ) if match  else print(f'Natch {id_} not found')


def create_match():
    home = input("Enter the matche's home: ")
    away = input("Enter the matche's away: ")
    try:
        match = Match.create(home, away)
        print(f'Success: {match}')
    except Exception as exc:
        print("Error creating match: ", exc)


def update_match():
    id_ = input("Enter the matche's id: ")
    if match := Match.find_by_id(id_):
        try:
            home = input("Enter the matche's new home team: ")
            match.home = home
            away = input("Enter the matche's new away team: ")
            match.away = away

            match.update()
            print(f'Success: {match}')
        except Exception as exc:
            print("Error updating matcht: ", exc)
    else:
        print(f'Match {id_} not found')


def delete_match():
    id_ = input("Enter the matches' id: ")
    if match := Match.find_by_id(id_):
       match.delete()
       print(f'Match {id_} deleted')
    else:
        print(f'Match {id_} not found')


def list_events():
    event = Event.get_all()
    for event in event:
        print(event)


def find_event_by_time():
    time = input("Enter the event's time: ")
    event = Event.find_by_time(time)
    print(event) if event else print(
        f'Event {time} not found')


def find_event_by_id():
    id_ = input("Enter the event's id: ")
    event = Event.find_by_id(id_)
    print(event) if event else print(f'Event {id_} not found')


def create_event():
    time = input("Enter the event's time: ")
    commentary = input("Enter the event's commentary: ")
    match_id = input("Enter the event's match id: ")
    try:
        event = Event.create(time, commentary, match_id)
        print(f'Success: {event}')
    except Exception as exc:
        print("Error creating event: ", exc)


def update_event():
    id_ = input("Enter the event's id: ")
    if event := Event.find_by_id(id_):
        try:
            time = input("Enter the event's new time: ")
            event.time = time
            commentary = input("Enter the event's new commentary: ")
            event.commentary = commentary
            match_id = input("Enter the event's new match id: ")
            event.match_id = match_id

            event.update()
            print(f'Success: {event}')
        except Exception as exc:
            print("Error updating event: ", exc)
    else:
        print(f'Event {id_} not found')


def delete_event():
    id_ = input("Enter the event's id: ")
    if event := Event.find_by_id(id_):
        event.delete()
        print(f'Event {id_} deleted')
    else:
        print(f'Event {id_} not found')


def list_match_events():
    match_id = input("Enter the match ID: ")
    match = Match.find_by_id(match_id)
    if match:
        events = match.events()
        if events:
            for event in events:
                print(event)
        else:
            print("No events found for this match.")
    else:
        print(f"Match with ID {match_id} not found.")
