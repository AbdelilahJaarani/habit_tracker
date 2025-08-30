from dataStorage import DataBase
from habit import Habit
import os
import random
import re
import time
DATABASE = DataBase()


class User: 
    def __init__(self):
        self.userID = None
        self.name = None
        self.email = None
        self.password = None
        self.preference = None

    def user_setting(self,user_dt):
        choice = True
        while choice: 
            print("Welcome")
            second_choice = int(input(
                "Start with a new Habit!\n" +
                "Press a Number!\n"+""
                "{:<25} [{}]\n".format("Starting the Habittracker",1) +
                "{:<25} [{}]\n".format("Updating your account",2) +
                "{:<25} [{}]\n".format("Showing user information",3) +
                "{:<25} [{}]\n".format("Deleting your UserAccount",4) +
                "{:<25} [{}]\n".format("Logging out",0) +
                "> "))

            if second_choice == 1:
                os.system('cls')
                return True
            elif second_choice == 2:
                os.system('cls')
                self.update_preferences(user_data=user_dt)
                input('Press any key to keep further ')
                os.system('cls')
            elif second_choice == 3:
                os.system('cls')
                print(self.show_profile(user_data=user_dt))
                input('Press any key to keep further ')
                os.system('cls')
            elif second_choice == 4:
                os.system('cls')
                if self.delete_user(user_data= user_dt):
                    return False
            elif second_choice == 0:  
                    return False
                #Back to the first Page
            else:
                print("Wrong input please write the correct number!")

    def is_valid_email(self,email):
        # Regular expression for validating an Email
        regex = r'^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(regex, email):
            return True
        else:
            return False
        

    def register(self):     
        #creating a new User for using the HabitTracker and saving Data into Database
        while True:
            print("Registration:")
            self.name = input("Name: ")
            self.email = input("Email: ")
            if self.is_valid_email(email=self.email):   
                self.password = input("Password: ")
                
                self.userID = {"ID":"user" ,
                            "name" : self.name,
                            "email": self.email,
                            "password": self.password}

                completedRegistration , user_data = DATABASE.save_data_user(data= self.userID)
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
        while True:
            print("Login")
            self.email = input("Email: ")
            if self.is_valid_email(email=self.email):
                self.password = input("Password: ")

                self.userID = {
                            "email": self.email,
                            "password": self.password
                            }    
                
                bl,user_data = DATABASE.load_data_User(data=self.userID)

                if not user_data:
                    os.system('cls')
                    print("Email or password is wrong!")
                    time.sleep(2)
                    return False, None
                else: 
                    os.system('cls')
                    print("Login was sucessfully")
                    time.sleep(1)
                    os.system('cls')
                    dt = user_data
                    return True, dt
            else:
                    os.system('cls')
                    print(f"{self.email} is an invalid email")
                    time.sleep(2)
                    os.system('cls')
                    continue 


    def show_profile(self,user_data):
        profie,_ = DATABASE.show_only_user_information(user_data)
        #show all Informarion about the User 
        return profie

    def update_preferences(self, user_data):
        
        def update_input(clm):
            update = input("Write your change:\n" + "Current: "+ str(clm) + "\n" +
                           ">")
            os.system('cls')
            return update
        
        while True:
            try: 
                update_nr = int(input(
                            "What do you want to change?\n" +
                            "{:<25} [{}]\n".format("Name",1) +      
                            "{:<25} [{}]\n".format("Email",2) +
                            "{:<25} [{}]\n".format("Password",3)+
                            "{:<25} [{}]\n".format("Exit",0)))
            
                if update_nr == 1:
                    os.system('cls')
                    newName= update_input(user_data["name"])
                    if DATABASE.update_data_user(data=user_data,part="name",update= newName):
                        user_data["name"] = newName
                        print(f"Name changed into {newName} !")
                elif update_nr == 2:
                    os.system('cls')
                    newEmail = update_input(user_data["email"])
                    if DATABASE.update_data_user(data=user_data,part="email",update= newEmail):
                        print(f"Email changed into {newEmail} !")
                        user_data["email"] = newEmail
                elif update_nr == 3:
                    os.system('cls')
                    newPassword = update_input(user_data["password"])
                    if DATABASE.update_data_user(data=user_data,part="password",update= newPassword):
                        user_data["password"] = newPassword
                        print(f"Password changed!")                    
                elif update_nr == 0:
                    os.system('cls')
                    break
            except ValueError:
                print("Only Number are allowed!")
                break



    def delete_user(self, user_data):
        habit_id_list = DATABASE.get_all_Habit_id(user_data)
        if DATABASE.delete_data_user(user_data= user_data,habit_data= habit_id_list):
            print("User and all Habit from user deleted! ")
            return True


