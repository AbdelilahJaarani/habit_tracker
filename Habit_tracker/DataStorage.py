import sqlite3
import os

class DataBase:
    def __init__(self):
        self.sqliteConnection = sqlite3.connect(r"C:\Users\abdel\Documents\Habit_Tracker.db")
        self.cursor = self.sqliteConnection.cursor()


    def saveData(self, data):
        cursor = self.cursor
        try:
            if data["ID"] == "user":
                cursor.execute("SELECT email FROM USER WHERE email = ?", (data["email"],))
                result = cursor.fetchone()
                if result:
                    os.system('cls')
                    print(f"The email: '{data["email"]}' is already used. Please use another one")
                    return False, data
                else:
                    cursor.execute(f"INSERT INTO USER (name,email,password) VALUES ('{data["name"]}', '{data ["email"]}', '{data["password"]}')")
                    self.sqliteConnection.commit()
                    print("Registartion was sucessfull!")
                    return True, data
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
            return False, None
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
            return False, None
        

    def loadData(self,data):
        cursor = self.cursor
        try:
            if data["ID"] == "user":
                cursor.execute("SELECT email, password FROM USER WHERE email = ? AND password = ?", (data["email"], data["password"]))
                result = cursor.fetchone()
                if result is None:
                    return False
                else:
                    print("Login was sucessfull")
                    return True, data
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")

    def backupData(self):
        try:
            pass
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
        

    def restoreData(self):
        try:
            pass
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
    
    def deleteData(self, data):
        pass
        

    def close(self):
        pass

