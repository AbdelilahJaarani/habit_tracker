import os
import time
from user import User
from habitTracker import HabitTracker
HABITTRACKER = HabitTracker()
USER = User()
        

def registration_and_login_menue():
    registration = False 
    login = False

    while not (registration or login):
        try:
            choice = int(input("------- HABIT TRACKER -------\n" +
                            "{:<25} [{}]\n".format("Registration",1) +      
                            "{:<25} [{}]\n".format("Login",2)+"> "))
            if choice == 1:
                os.system('cls')
                success , user_data = USER.register()
                if success:
                    os.system('cls')
                    print(f"Welcome {user_data["name"]} !") #the returned tuple (UserId, Name, Email, Password)
                    time.sleep(2)
                    os.system('cls')
                    if USER.user_setting(user_dt=user_data):
                        registration = True
                        return registration, user_data

            elif choice == 2:
                    os.system('cls')
                    success, user_data = USER.login()
                    if  success == False:
                        print("Email or Password are wrong please try again")
                        os.system('cls')
                    elif USER.user_setting(user_dt=user_data): 
                        login = True
                        return login, user_data
                    # Der eigentliche Start kommt jetzt 
            else:
                os.system('cls')
                print("OOps wrong Input please try again! ")
        
        except ValueError:
            os.system('cls')
            print("Only Numbers are allowed !")
            time.sleep(2)
            os.system('cls')

def main():
    stay_on_menue = True
    
    while stay_on_menue:
        sucess, user_data = registration_and_login_menue()
        if sucess:
            result = HABITTRACKER.start_plattform(UserID=user_data)
            if result:
                Userset = USER.user_setting(user_dt=user_data)
                if Userset == False:
                    print("Logging out, returning to login menu...")
                    time.sleep(2)
                    continue
            else:
                print("Failed to start platform.")    
        else:
            print("Login or registration failed. Please try again.")



if __name__ == "__main__":
    main()