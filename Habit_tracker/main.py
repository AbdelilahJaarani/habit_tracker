import os
from user import User
user = User()


print("HABIT TRACKER")
registration = False 
login = False

while not registration or not login:
    choice = input("Press [r] for registration || press [l] for login ")
    if choice == "r":
        os.system('cls')
        success , data = user.register()
        if success:
            os.system('cls')
            print(f"Welcome {data["name"]} !")

    elif choice == "l":
            os.system('cls')
            if user.login() == False:
                print("Email or Password are wrong please try again")
                #os.system('cls')
            else: 
                 login = True
    else:
         os.system('cls')
         print("OOps wrong Input please try again! ")
        