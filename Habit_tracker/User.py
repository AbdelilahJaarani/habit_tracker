from DataStorage import DataBase
Data = DataBase()


class User: 
    def __init__(self):
        self.userID = None
        self.name = None
        self.email = None
        self.password = None
        self.preference = None

    def register(self):
        #creating a new User for using the HabitTracker and saving Data into Database
        print("Registration:")
        self.name = input("Name: ")
        self.email = input("Email: ")
        self.password = input("Password: ")
        
        self.userID = {"ID": "user",
                       "name" : self.name,
                       "email": self.email,
                       "password": self.password}

        Data.saveData(data= self.userID)



        
    
    def login(self):
        #checked if User is already register, 
        pass

    def showProfile(self):
        #show all Informarion about the User 
        return self.userID

    def updatePreferences(self):
        #Updating new Preferences or adding more {have more clear}
        pass


    def addHabit(self):
        #adding Habit from the Class Habit.py into the Database
        pass

    def viewHabits(self):
        #showing all Habits which are created 
        pass


    def deleteHabit(self):
        #deleting Habit which is created from the User
        pass


