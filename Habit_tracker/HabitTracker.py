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


    def KeepGoingOrNot(self): 
        while True:
            ip =  int(input("Press number 0 to go back into the menue!\n"))
            if ip == 0:
                os.system('cls')
                return True
            else:
                print('Wrong Input')

    def StartPLattform(self, UserID):

        choice = True
        while choice: 
            print("Welcome")
            habitChoice = int(input(
                "Start with a new Habit!\n" +
                "Press a Number!\n"+""
                "{:<25} [{}]\n".format("Mark your Habit done",1) +
                "{:<25} [{}]\n".format("Create your own Habit",2) +
                "{:<25} [{}]\n".format("Take a Template Habit",3) +
                "{:<25} [{}]\n".format("Show your Habit",4) +
                "{:<25} [{}]\n".format("Edit a Habit",5) +
                "{:<25} [{}]\n".format("Delete a Habit",6) +
                "{:<25} [{}]\n".format("Back to user menue",0) +
                "> "))
            if habitChoice == 1:
                hb.markAsCompleted(user_data= UserID)
            elif habitChoice == 2:
                hb.add(user_data= UserID)
            elif habitChoice == 3: 
                os.system('cls')
                habitmplte = hb.addHabitTemplate(user_data= UserID)
                if habitmplte == None:
                    pass #if the user press exit you will get here
                else:
                    data.saveData_Habit(habitmplte) #The habits is saved into the Database
            elif habitChoice == 4:
                os.system('cls')
                habitList = hb.showHabit(user=UserID)
                print(habitList)
                self.KeepGoingOrNot()
            elif habitChoice == 5:
                hb.editHabit(user_data= UserID)
            elif habitChoice == 6:
                hb.delete(user_data= UserID)
            elif habitChoice == 0: 
                return True #Back to the user menue
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