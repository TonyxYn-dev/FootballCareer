import json
from pathlib import Path
from engine.clock import WorldClock
from engine.events import EventBus, DomainEvent
from persistence.save_manager import SaveManager, SaveError

SETTINGS = json.loads(Path("config/settings.json").read_text(encoding="utf-8"))

def dashboard(state):
    print("\n" + "=" * 46)
    print("FOOTBALL CAREER: BECOME A LEGEND")
    print("=" * 46)
    print(f"World date : {state['world_date']}")
    print(f"Career     : {state.get('career_name', 'Not created')}")
    print(f"Player     : {state.get('player_name', 'Not created')}")
    print(f"World data : {state.get('world_data_status', 'Not imported')}")
    print("=" * 46)

def new_career():
    career_name = input("Career name: ").strip() or "My Career"
    player_name = input("Player full name: ").strip()
    if not player_name:
        print("A player name is required.")
        return None
    dob = input("Date of birth (YYYY-MM-DD): ").strip()
    nationality = input("Nationality ISO code (e.g. NGA): ").strip().upper()
    position = input("Position code (e.g. ST, CM, CB): ").strip().upper()
    world_date = input("World start date (YYYY-MM-DD): ").strip()
    try:
        WorldClock(world_date)
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return None
    return {
        "career_name": career_name,
        "player_name": player_name,
        "player": {"full_name": player_name, "date_of_birth": dob,
                   "nationality_code": nationality, "position_code": position},
        "world_date": world_date,
        "world_data_status": "Awaiting sourced real-world dataset",
        "events": []
    }

def run():
    saves = SaveManager(SETTINGS["save_directory"])
    bus = EventBus()
    bus.subscribe("career.created", lambda event: print(f"\nCareer initialized: {event.payload['career_name']}"))
    state = None
    while True:
        print("\n1. New career\n2. Load career\n3. View dashboard\n4. Advance world clock (test)\n5. Save career\n0. Exit")
        choice = input("> ").strip()
        if choice == "1":
            state = new_career()
            if state:
                bus.publish(DomainEvent("career.created", {"career_name": state["career_name"]}))
        elif choice == "2":
            slot = input("Save slot [career_1]: ").strip() or "career_1"
            try:
                state = saves.load(slot)
                print("Save loaded.")
            except SaveError as exc:
                print(exc)
        elif choice == "3":
            dashboard(state) if state else print("Create or load a career first.")
        elif choice == "4":
            if not state:
                print("Create or load a career first.")
                continue
            try:
                clock = WorldClock(state["world_date"])
                clock.advance_days(int(input("Days to advance: ")))
                state["world_date"] = clock.current_date
                print(f"World date is now {clock.current_date}")
            except (ValueError, KeyError):
                print("Invalid date or day count.")
        elif choice == "5":
            if not state:
                print("Nothing to save.")
                continue
            slot = input("Save slot [career_1]: ").strip() or "career_1"
            try:
                path = saves.save(slot, state)
                print(f"Saved: {path}")
            except (ValueError, OSError) as exc:
                print(f"Save failed: {exc}")
        elif choice == "0":
            break
        else:
            print("Choose a listed option.")
