from dataStorage import DataBase
from habit import Habit
import os
import random
import re
Data = DataBase()
#hb = habit()


class User: 
    def __init__(self):
        self.userID = None
        self.name = None
        self.email = None
        self.password = None
        self.preference = None
        

    def register(self):

        def is_valid_email(email):
            # Regular expression for validating an Email
            regex = r'^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w+$'
            if re.match(regex, email):
                return True
            else:
                return False
            
        #creating a new User for using the HabitTracker and saving Data into Database
        while True:
            print("Registration:")
            self.name = input("Name: ")
            self.email = input("Email: ")
            if is_valid_email(email=self.email):   
                self.password = input("Password: ")
                
                self.userID = {"ID":"user" ,
                            "name" : self.name,
                            "email": self.email,
                            "password": self.password}

                completedRegistration , user_data = Data.saveData_User(data= self.userID)
                if completedRegistration:
                    os.system('cls')
                    print("Registartion was sucessfull!")
                    return True, user_data
                else:
                    return False, None
            else:
                print(f"{self.email} is an invalid email")
                continue    
    
    def login(self):
        #checked if User is already register
        print("Login")
        self.email = input("Email: ")
        self.password = input("Password: ")

        self.userID = {
                       "email": self.email,
                       "password": self.password
                       }    
        
        user_data = Data.loadData_User(data=self.userID)

        if not user_data:
            return False, None
        else: 
            os.system('cls')
            print("Login was sucessfully")
            dt = user_data
            return True, dt


    def showProfile(self,user_data):
        profie,_ = Data.ShowOnlyUserInformation(user_data)
        #show all Informarion about the User 
        return profie

    def updatePreferences(self, user_data):
        #Updating new Preferences or adding more {have more clear}
        updateNr = input("What do you want to change\n [1] Name \n [2] Email \n [3] Password")
        if updateNr == 1:
            os.system('cls')
            self.userID["name"] = input("Please write your new name")
            check = input(f"Are you sure that you want to change you name into {self.userID["name"]}? \n y/n ")
            if check == "y":
                if not Data.UpdateData_User(data=self.userID): #Update into the DB
                    return False
    
    def deleteUser(self, user_data):
        _, HabitDict = Data.loadData_Habit(user_data)
        if Data.deleteData_User(user_data= user_data,habit_data= HabitDict):
            print("User and all Habit from user deleted! ")
        pass


