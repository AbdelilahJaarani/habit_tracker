from functools import reduce
from datetime import datetime, timedelta
from dataStorage import DataBase
import time
import os

class Analytics:
    def __init__(self):
        self.db = DataBase()

    def analytics_menu(self, user_id):
        while True:
            os.system('cls')

            choice = int(input(
                "Start with a new Habit!\n" +
                "Press a Number!\n"+""
                "{:<45} [{}]\n".format("Shwoing all habits",1) +
                "{:<45} [{}]\n".format("Show habits by periodicity",2) +
                "{:<45} [{}]\n".format("Show longest streak for all habits",3) +
                "{:<45} [{}]\n".format("Show longest streak for a specific habit",4) +
                "{:<45} [{}]\n".format("Return to main menu",0) +
                "> "))

            if choice == 1:
                habits = self.get_all_habits(user_id["user_id"])
                print("\nAll Habits:")
                for h in habits:
                    print(f"- {h}")
                input("Press any key to go back into the analytics menue. ")

            elif choice == 2:
                periodicity = input("Enter periodicity ('daily' oder 'weekly'): ")
                habits = self.get_habits_by_periodicity(user_id["user_id"], periodicity)
                print(f"\nHabits with periodicity '{periodicity}':")
                for h in habits:
                    print(f"- {h}")
                input("Press any key to go back into the analytics menue. ")

            elif choice == 3:
                streaks = self.longest_streak_all_habits(user_id["user_id"])
                print("\nLongest streaks of all habits:")
                for habit, streak in streaks.items():
                    print(f"{habit}: {streak} periods")
                input("Press any key to go back into the analytics menue. ")

            elif choice == 4:
                habit_name = input("Enter habit name: ").strip()
                _, habits_list = self.db.load_data_Habit({"user_id": user_id["user_id"]})
                habit_id = None
                periodicity = None
                for habit in habits_list:
                    if habit['habit'].lower() == habit_name.lower():
                        habit_id = habit['habit_id']
                        periodicity = habit['periodicity']
                        break
                if habit_id:
                    streak = self.longest_streak_for_habit(habit_id, periodicity)
                    print(f"Longest streak for '{habit_name}': {streak} periods")
                    input("Press any key to go back into the analytics menue. ")
                else:
                    print("Habit not found")
                    input("Press any key to go back into the analytics menue. ")

            elif choice == 0:
                print('Returning...')
                time.sleep(2)
                os.system('cls')
                break
            else:
                print("Invalid input, please try again. ")

    def get_all_habits(self, user_id):
        _, habits = self.db.load_data_Habit({"user_id": user_id})
        return list(map(lambda h: h['habit'], habits))

    def get_habits_by_periodicity(self, user_id, periodicity):
        _, habits = self.db.load_data_Habit({"user_id": user_id})
        filtered = filter(lambda h: h['periodicity'] == periodicity, habits)
        return list(map(lambda h: h['habit'], filtered))

    def longest_streak_for_habit(self, habit_id, periodicity):
        dates = self.db._get_completion_dates(habit_id)
        if not dates:
            return 0

        if periodicity == "daily":
            diff = timedelta(days=1)
        elif periodicity == "weekly":
            diff = timedelta(weeks=1)
        else:
            raise ValueError("Unbekannte Periodizität")

        max_streak = 1
        current_streak = 1

        for i in range(1, len(dates)):
            if dates[i] - dates[i-1] == diff:
                current_streak += 1
            else:
                current_streak = 1
            if current_streak > max_streak:
                max_streak = current_streak

        return max_streak

    def longest_streak_all_habits(self, user_id):
        _, habits = self.db.load_data_Habit({"user_id": user_id})
        streaks = {h['habit']: self.longest_streak_for_habit(h['habit_id'], h['periodicity']) for h in habits}
        return streaks
