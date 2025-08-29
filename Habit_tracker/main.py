import os
import time
from user import User
from habitTracker import HabitTracker
ht = HabitTracker()
user = User()



          

def registrationAndLoginMenue():
    print("HABIT TRACKER")
    registration = False 
    login = False

    while not (registration or login):
        choice = int(input("Press [1] for registration || press [2] for login "))
        if choice == 1:
            os.system('cls')
            success , user_data = user.register()
            if success:
                os.system('cls')
                print(f"Welcome {user_data[1]} !") #the returned tuple (UserId, Name, Email, Password)
                time.sleep(2)
                os.system('cls')
                if user.UserSetting(user_dt=user_data):
                    registration = True
                    return registration, user_data
                
                # Der eigentliche Start kommt jetzt 


        elif choice == 2:
                os.system('cls')
                success, user_data = user.login()
                if  success == False:
                    print("Email or Password are wrong please try again")
                    #os.system('cls')
                elif user.UserSetting(user_dt=user_data): 
                    login = True
                    return login, user_data
                # Der eigentliche Start kommt jetzt 
        else:
            os.system('cls')
            print("OOps wrong Input please try again! ")

def main():
    stayOnMenue = True
    
    while stayOnMenue:
        sucess, user_data = registrationAndLoginMenue()
        if sucess:
            result = ht.StartPLattform(UserID=user_data)
            if result:
                Userset = user.UserSetting(user_dt=user_data)
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