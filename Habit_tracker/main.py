import os
from User import User
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
            if user.login():
                os.system('cls')
                login = True
    else:
         os.system('cls')
         print("OOps wrong Input please try again! ")
        


