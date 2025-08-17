#Which creates UI for everything
from user import User
from dataStorage import DataBase as data
from habit import Habit
import os
import time
hb = Habit()

class HabitTracker:
    def __init__(self):
        self.trackerID = None
        self.createdHabit = None

    def StartPLattform(self, UserID):

        print(" Welcome")
        choice = True
        while choice: 
            habitChoice = int(input(" Start with a new Habit!\n If you want to create your own Habit please press [1]\n \
                                If you want to take a Template please press [2]\n Press [3] for back to user menue"))
            if habitChoice == 1:
                hb.add(user_data= UserID)
            elif habitChoice == 2: 
                os.system('cls')
                habitmplte = hb.addHabitTemplate(user_data= UserID)
                if habitmplte == None:
                    pass #if the user press exit you will get here
                else:
                    data.saveData_Habit(habitmplte) #The habits is saved into the Database
            elif habitChoice == 3:
                return True #Unlogging 
            else:
                os.system('cls')
                print("Wrong Input!")
                time.sleep(1)
                os.system('cls')
                
                    
    def sendNotification(self):
        #via mail sending notifcation to check the habits
        pass

    def generateReport(self):
        pass

    def importData(self):
        pass

    def exportData(self):
        pass