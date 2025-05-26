from User import User
user = User()


print("HABIT TRACKER")
choice = input("Press [r] for registration || press [l] for login ")
if choice == "r":
    user.register()
elif choice == "l":
    user.login()
