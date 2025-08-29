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

    def UserSetting(self,user_dt):
        choice = True
        while choice: 
            print("Welcome")
            second_choice = int(input(
                "Start with a new Habit!\n" +
                "Press a Number!\n"+""
                "{:<25} [{}]\n".format("Starting the Habittracker",1) +
                "{:<25} [{}]\n".format("Updating your account",2) +
                "{:<25} [{}]\n".format("Deleting a User",3) +
                "{:<25} [{}]\n".format("Showing user information",4) +
                "{:<25} [{}]\n".format("Logging out",0) +
                "> "))

            if second_choice == 1:
                return True
            elif second_choice == 2:
                self.updatePreferences(user_data=user_dt) #tuple (True, {"user_id": 1....}) beispiel
            elif second_choice == 3:
                self.deleteUser(user_data= user_dt)
            elif second_choice == 4:
                print(self.showProfile(user_data=user_dt))
            elif second_choice == 0:  
                    return False
                #Back to the first Page
            else:
                print("Wrong input please write the correct number!")
        

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
        
        bl,user_data = Data.loadData_User(data=self.userID)

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
        #_,userDict = Data.ShowOnlyUserInformation(data=user_data) 
        # 
        #  
        
        def updateInput(clm):
            update = input("Write your change:\n" + "Current: "+ str(clm) + "\n" +
                           ">")
            os.system('cls')
            return update
        # es wird immer nur ein User Informationen gegeben deswegen nicht Noetige die Liste 
        #runter zu ratten 
        while True:
            try: 
                updateNr = int(input(
                            "What do you want to change?\n" +
                            "{:<25} [{}]\n".format("Name",1) +      
                            "{:<25} [{}]\n".format("Email",2) +
                            "{:<25} [{}]\n".format("Password",3)+
                            "{:<25} [{}]\n".format("Exit",0)))
            
                if updateNr == 1:
                    os.system('cls')
                    newName= updateInput(user_data["name"])
                    if Data.UpdateData_User(data=user_data,part="name",update= newName):
                        print(f"Name changed into {newName} !")
                elif updateNr == 2:
                    os.system('cls')
                    newEmail = updateInput(user_data["email"])
                    if Data.UpdateData_User(data=user_data,part="email",update= newEmail):
                        print(f"Email changed into {newEmail} !")
                elif updateNr == 3:
                    os.system('cls')
                    newPassword = updateInput(user_data["password"])
                    if Data.UpdateData_User(data=user_data,part="password",update= newPassword):
                        print(f"Password changed!")                    
                elif updateNr == 0:
                    break
            except ValueError:
                print("Only Number are allowed!")
                break



    def deleteUser(self, user_data):
        _, HabitDict = Data.loadData_Habit(user_data)
        if Data.deleteData_User(user_data= user_data,habit_data= HabitDict):
            print("User and all Habit from user deleted! ")
        pass


