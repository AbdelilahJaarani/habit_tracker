import sqlite3
import os

class DataBase:
    def __init__(self):
        self.sqliteConnection = sqlite3.connect(r"C:\Users\abdel\Documents\Habit_Tracker.db")
        self.cursor = self.sqliteConnection.cursor()


    def saveData_User(self, data):
        #save data for 
        cursor = self.cursor
        try:
            if data["ID"] == "user":
                cursor.execute(f"INSERT INTO USER (name,email,password) VALUES ('{data["name"]}', '{data ["email"]}', '{data["password"]}')")
                user_id = cursor.lastrowid
                cursor.execute("SELECT * FROM USER WHERE UserID = ?",(user_id,))
                user_data = cursor.fetchone()
                return True, user_data
        except sqlite3.IntegrityError as e:
            os.system('cls')
            print(f"The email '{data['email']}' is already used. Please use another one")
            return False, None
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
            return False, None
        

    def loadData_User(self,data):
        cursor = self.cursor
        try:
            if data["ID"] == "user":
                cursor.execute("SELECT UserID, email, password FROM USER WHERE email = ? AND password = ?", (data["email"], data["password"]))
                user_data = cursor.fetchone()
                if user_data is None:
                    return False
                else:
                    return True, user_data #Result will be the tuple of all things (UserID,email,password )
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")

    def UpdateData_User(self,data):
        cursor = self.cursor
        try:
            pass
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
        

    # def restoreData_User(self):   // Not nacessary  for habti using 
    
    #     try:
    #         pass
    #     except sqlite3.IntegrityError as e:
    #         print(f"Integrity Error: {e}")
    #     except sqlite3.OperationalError as e:
    #         print(f"Operational Error: {e}")
    
    def deleteData_User (self, data):
        pass
    ########################### Habit Storage ########################################
    
        
    def saveData_Habit(self, data):
        #save Habit into DB  
        cursor = self.cursor
        try:
            if data:
                cursor.execute("INSERT INTO habits (user_id,name,category,description,periodicity,status,startDate)VALUES (?,?,?,?,?,?)"
                               (data["name"], data["category"], data["description"], data["periodicity"], data["status"], data["status"],data["startDate"])
                )
                self.sqliteConnection.commit()
                return True, data
        except sqlite3.Error as e:
            print(f"Integrity Error: {e}")
            return False, None
        

    def loadData_Habit(self,data):
        cursor = self.cursor
        try:
            if data["ID"] == "user":
                cursor.execute("SELECT email, password FROM USER WHERE email = ? AND password = ?", (data["email"], data["password"]))
                result = cursor.fetchone()
                if result is None:
                    return False
                else:
                    return True, data
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")

    def UpdateData_Habit(self,data):
        cursor = self.cursor
        try:
            pass
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
        

    def restoreData_Habit(self):
        try:
            pass
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
    
    def deleteData_Habit(self, data):
        pass
        
        
    def close(self):
        pass

