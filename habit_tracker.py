# Habit Tracker App
# Developed by Zohreh Mosahebfard
# A command-line application to manage and track habits



import json
from datetime import datetime, timedelta
from functools import reduce

# Habit class
class Habit:
    """
    Represents a habit with attributes for name, frequency, last completion date, and streak.
    """
    def __init__(self, name, frequency, last_completed=None, streak=0):
        self.name = name
        self.frequency = frequency
        self.last_completed = datetime.strptime(last_completed, '%Y-%m-%d') if last_completed else None
        self.streak = streak

    def complete_task(self):
        now = datetime.now()
        if self.last_completed:
            delta = (now - self.last_completed).days
            if (self.frequency == 'daily' and delta <= 1) or (self.frequency == 'weekly' and delta <= 7):
                self.streak += 1
            else:
                self.streak = 1
        else:
            self.streak = 1
        self.last_completed = now
        print(f"Habit '{self.name}' completed! Current streak: {self.streak}")

    def to_dict(self):
        return {
            "name": self.name,
            "frequency": self.frequency,
            "last_completed": self.last_completed.strftime('%Y-%m-%d') if self.last_completed else None,
            "streak": self.streak
        }

    @staticmethod
    def from_dict(data):
        return Habit(data["name"], data["frequency"], data["last_completed"], data["streak"])


# User class
class User:
    """
    Manages a collection of habits.
    """
    def __init__(self, storage_file='habits.json'):
        self.storage_file = storage_file
        self.habits = []
        self.load_habits()

    def add_habit(self, name, frequency):
        if any(habit.name == name for habit in self.habits):
            print(f"Habit '{name}' already exists.")
        else:
            habit = Habit(name, frequency)
            self.habits.append(habit)
            print(f"Habit '{name}' ({frequency}) added!")

    def list_habits(self):
        if not self.habits:
            print("No habits found!")
        else:
            for habit in self.habits:
                print(f"{habit.name} ({habit.frequency}) - Streak: {habit.streak}")

    def complete_habit(self, name):
        for habit in self.habits:
            if habit.name == name:
                habit.complete_task()
                return
        print(f"Habit '{name}' not found.")

    def delete_habit(self, name):
        self.habits = [habit for habit in self.habits if habit.name != name]
        print(f"Habit '{name}' deleted.")

    def save_habits(self):
        with open(self.storage_file, 'w') as f:
            json.dump([habit.to_dict() for habit in self.habits], f)

    def load_habits(self):
        try:
            with open(self.storage_file, 'r') as f:
                self.habits = [Habit.from_dict(habit) for habit in json.load(f)]
        except FileNotFoundError:
            self.habits = []

    # Analytics module (functional programming)
    def longest_streak_all(self):
        return reduce(lambda x, y: max(x, y.streak), self.habits, 0)

    def longest_streak_habit(self, name):
        for habit in self.habits:
            if habit.name == name:
                return habit.streak
        return 0

    def filter_by_frequency(self, frequency):
        return list(filter(lambda habit: habit.frequency == frequency, self.habits))


# Main function
def main():
    user = User()

    # Predefined habits
    predefined_habits = [
        {"name": "Exercise", "frequency": "daily"},
        {"name": "Reading Book", "frequency": "daily"},
        {"name": "Practice German", "frequency": "daily"},
        {"name": "Meditation", "frequency": "weekly"},
        {"name": "Learning Python", "frequency": "weekly"}
    ]

    for habit in predefined_habits:
        user.add_habit(habit["name"], habit["frequency"])

    while True:
        print("\nHabit Tracker Menu:")
        print("1. Add a Habit")
        print("2. Complete a Habit")
        print("3. View All Habits")
        print("4. Delete a Habit")
        print("5. Analyze Habits")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter habit name: ")
            frequency = input("Enter frequency (daily/weekly): ")
            user.add_habit(name, frequency)
        elif choice == "2":
            name = input("Enter habit name to complete: ")
            user.complete_habit(name)
        elif choice == "3":
            user.list_habits()
        elif choice == "4":
            name = input("Enter habit name to delete: ")
            user.delete_habit(name)
        elif choice == "5":
            print("Longest streak across all habits:", user.longest_streak_all())
            name = input("Enter habit name to check longest streak: ")
            print(f"Longest streak for '{name}':", user.longest_streak_habit(name))
        elif choice == "6":
            user.save_habits()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
