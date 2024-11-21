

import unittest
from habit_tracker import Habit, User

class TestHabitTracker(unittest.TestCase):
    def test_habit_creation(self):
        habit = Habit("Test Habit", "daily")
        self.assertEqual(habit.name, "Test Habit")
        self.assertEqual(habit.frequency, "daily")
        self.assertEqual(habit.streak, 0)

    def test_complete_task(self):
        habit = Habit("Test Habit", "daily")
        habit.complete_task()
        self.assertEqual(habit.streak, 1)

    def test_add_habit(self):
        user = User()
        user.add_habit("Test Habit", "daily")
        self.assertEqual(len(user.habits), 1)

if __name__ == '__main__':
    unittest.main()
