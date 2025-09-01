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
    """
    Command-line interface controller for the habit tracker.

    This class presents a text menu, dispatches actions to the Habit and Analytics
    services, and coordinates simple navigation like clearing the screen and returning
    to the user menu. It does not contain business logic; it orchestrates calls to
    domain services and persistence. 

    Attributes:
        trackerID (str | None): Optional identifier for the tracker session or context. 
        createdHabit (dict | object | None): Reference to a recently created habit, if any. 
    """
    def __init__(self):
        self.trackerID = None
        self.createdHabit = None


    def keep_going_or_not(self):

        """
        Block until the user chooses to return to the menu.

        Prompts for 0, clears the console on success, and signals the caller to resume.
        Returns:
            bool: True once the user entered 0 and the screen was cleared.
        """
        while True:
            ip =  int(input("Press number 0 to go back into the menue!\n"))
            if ip == 0:
                os.system('cls')
                return True
            else:
                print('Wrong Input')


    def start_plattform(self, UserID):
        
        """
        Run the main habit menu loop for the given user.

        Presents actions (mark done, create/edit/delete, templates, list, analytics),
        dispatches to domain services, and exits back to the user menu on 0.
        Args:
            UserID (str | int): Identifier of the authenticated user.
        Returns:
            bool: True when exiting to the higher-level user menu.
        """

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
                
                