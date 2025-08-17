import os
import time
from user import User
from habitTracker import HabitTracker
ht = HabitTracker()
user = User()


def UserSetting(user_dt,register,login):
    while True: 
        second_choice = int(input("Press [1] for starting the Habittracker\nPress [2] for Updating your account " \
        "information\nPress [3] for deleting a User\n Press [4] for showing user information\nPress [0] for logging out"))
        if second_choice == 1:
            return True
        elif second_choice == 2:
            user.updatePreferences(user_data=user_dt)
        elif second_choice == 3:
            user.deleteUser()
        elif second_choice == 4:
            user.showProfile()
        elif second_choice == 0: 
            if login:
                return False
            #Back to the first Page
        else:
            print("Wrong input please write the correct number!")
          

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
                print(f"Welcome {user_data[2]} !") #the returned tuple (UserId, Name, Email, Password)
                time.sleep(2)
                os.system('cls')
                if UserSetting(user_dt=user_data):
                    registration = True
                    return registration, user_data
                # Der eigentliche Start kommt jetzt 


        elif choice == 2:
                os.system('cls')
                success, user_data = user.login()
                if  success == False:
                    print("Email or Password are wrong please try again")
                    #os.system('cls')
                elif UserSetting(user_dt=user_data): 
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
                Userset = UserSetting(user_dt=user_data)
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