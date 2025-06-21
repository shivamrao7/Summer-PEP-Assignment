import json
from datetime import datetime


class PersistenceError(Exception):
    """Raised when saving/loading habits fails."""
    pass


class Habit:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.__history = []

    def mark_done(self, date: str):
        if date not in self.__history:
            self.__history.append(date)
            self.__history.sort() 

    def streak(self) -> int:
        if not self.__history:
            return 0
        dates = [datetime.strptime(d, "%Y-%m-%d") for d in self.__history]
        dates.sort(reverse=True)
        streak = 1
        for i in range(1, len(dates)):
            if (dates[i-1] - dates[i]).days == 1:
                streak += 1
            else:
                break
        return streak

    def __str__(self):
        return f"{self.name}: {self.description} (Streak: {self.streak()})"

    def __repr__(self):
        return f"Habit(name={self.name!r}, description={self.description!r})"

    def to_dict(self):
        return {"name": self.name, "description": self.description, "history": self.__history}

    @classmethod
    def from_dict(cls, data):
        h = cls(data["name"], data["description"])
        h.__history = data["history"]
        return h


class HabitTracker:
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self):
        self.habits = {}

    def add_habit(self, name: str, desc: str):
        self.habits[name] = Habit(name, desc)

    def remove_habit(self, name: str):
        if name in self.habits:
            del self.habits[name]

    def mark_done(self, name: str, date: str = None):
        if not date:
            date = datetime.today().strftime(self.DATE_FORMAT)
        if name in self.habits:
            self.habits[name].mark_done(date)

    def list_habits(self):
        return list(self.habits.values())

    def report(self):
        return {name: habit.streak() for name, habit in self.habits.items()}

    def __add__(self, other):
        merged = HabitTracker()
        merged.habits = {**self.habits}
        for name, habit in other.habits.items():
            if name in merged.habits:
                for date in habit._Habit__history:
                    merged.habits[name].mark_done(date)
            else:
                merged.habits[name] = habit
        return merged

    def save(self, filename: str):
        try:
            with open(filename, "w") as f:
                data = {name: habit.to_dict() for name, habit in self.habits.items()}
                json.dump(data, f, indent=4)
        except OSError:
            raise PersistenceError("Failed to save data.")

    def load(self, filename: str):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.habits = {name: Habit.from_dict(h) for name, h in data.items()}
        except FileNotFoundError:
            self.habits = {}
        except json.JSONDecodeError:
            raise PersistenceError("Corrupted JSON file.")


def summarize(obj):
    print(f"{obj.name}: Streak = {obj.streak()}")
