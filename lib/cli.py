
from helpers import (
    exit_program,
    list_matches,
    find_match_by_home,
    find_match_by_id,
    create_match,
    update_match,
    delete_match,
    list_events,
    find_event_by_time,
    find_event_by_id,
    create_event,
    update_event,
    delete_event,
    list_match_events
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            list_matches()
        elif choice == "2":
            find_match_by_home()
        elif choice == "3":
            find_match_by_id()
        elif choice == "4":
            create_match()
        elif choice == "5":
            update_match()
        elif choice == "6":
            delete_match()
        elif choice == "7":
            list_events()
        elif choice == "8":
            find_event_by_time()
        elif choice == "9":
            find_event_by_id()
        elif choice == "10":
            create_event()
        elif choice == "11":
            update_event()
        elif choice == "12":
            delete_event()
        elif choice == "13":
            list_match_events()
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. List all matches")
    print("2. Find match by home team")
    print("3. Find match by id")
    print("4: Create match")
    print("5: Update match")
    print("6: Delete match")
    print("7. List all events")
    print("8. Find event by time")
    print("9. Find event by id")
    print("10: Create event")
    print("11: Update event")
    print("12: Delete event")
    print("13: List all events in a match")


if __name__ == "__main__":
    main()
