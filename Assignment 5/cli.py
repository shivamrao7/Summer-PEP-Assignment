from habits import HabitTracker, PersistenceError
from datetime import datetime

FILENAME = "habits.json"


def show_menu():
    print("\n--- Habit Tracker ---")
    print("1. Add new habit")
    print("2. Remove habit")
    print("3. Mark habit done")
    print("4. List all habits")
    print("5. Show streak report")
    print("6. Save & Exit")


def main():
    tracker = HabitTracker()
    try:
        tracker.load(FILENAME)
    except PersistenceError:
        print("Warning: Could not load previous data.")

    while True:
        show_menu()
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                name = input("Habit name: ")
                desc = input("Description: ")
                tracker.add_habit(name, desc)
            elif choice == 2:
                name = input("Habit to remove: ")
                tracker.remove_habit(name)
            elif choice == 3:
                name = input("Habit name: ")
                date = input("Date (YYYY-MM-DD or leave blank for today): ")
                if date:
                    datetime.strptime(date, "%Y-%m-%d")  
                    tracker.mark_done(name, date)
                else:
                    tracker.mark_done(name)
            elif choice == 4:
                for habit in tracker.list_habits():
                    print(habit)
            elif choice == 5:
                report = tracker.report()
                for name, streak in report.items():
                    print(f"{name}: {streak} day(s)")
            elif choice == 6:
                try:
                    tracker.save(FILENAME)
                    print("Progress saved.")
                except PersistenceError:
                    print("Error: Failed to save.")
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()



