#Which creates UI for everything
from analytics import Analytics
from user import User
from dataStorage import DataBase as data
from habit import Habit
import os
import time
HABIT = Habit()
ANALYTICS = Analytics()

class HabitTracker:
    def __init__(self):
        self.trackerID = None
        self.createdHabit = None


    def keep_going_or_not(self): 
        while True:
            ip =  int(input("Press number 0 to go back into the menue!\n"))
            if ip == 0:
                os.system('cls')
                return True
            else:
                print('Wrong Input')


    def start_plattform(self, UserID):

        choice = True
        while choice: 
            print("Welcome")
            habit_choice = int(input(
                "Start with a new Habit!\n" +
                "Press a Number!\n"+""
                "{:<25} [{}]\n".format("Mark your Habit done",1) +
                "{:<25} [{}]\n".format("Create your own Habit",2) +
                "{:<25} [{}]\n".format("Take a Template Habit",3) +
                "{:<25} [{}]\n".format("Show your Habit",4) +
                "{:<25} [{}]\n".format("Edit a Habit",5) +
                "{:<25} [{}]\n".format("Delete a Habit",6) +
                "{:<25} [{}]\n".format("Analytics",7) +
                "{:<25} [{}]\n".format("Back to user menue",0) +
                "> "))
            if habit_choice == 1:
                os.system('cls')
                HABIT.mark_as_completed(user_data= UserID)
            elif habit_choice == 2:
                os.system('cls')
                HABIT.add(user_data= UserID)
            elif habit_choice == 3: 
                os.system('cls')
                habitmplte = HABIT.add_habit_template(user_data= UserID)
                if habitmplte == None:
                    pass #if the user press exit you will get here
                else:
                    data.save_data_Habit(habitmplte) #The habits is saved into the Database
            elif habit_choice == 4:
                os.system('cls')
                habitList = HABIT.show_habit(user=UserID)
                print(habitList)
                self.keep_going_or_not()
            elif habit_choice == 5:
                os.system('cls')
                HABIT.edit_habit(user_data= UserID)
            elif habit_choice == 6:
                os.system('cls')
                HABIT.delete(user_data= UserID)
            elif habit_choice == 7:
                os.system('cls')
                ANALYTICS.analytics_menu(user_id= UserID)
            elif habit_choice == 0: 
                print('Returning..')
                time.sleep(2)
                os.system('cls')
                return True #Back to the user menue
            else:
                os.system('cls')
                print("Wrong Input!")
                time.sleep(1)
                os.system('cls')
                
                