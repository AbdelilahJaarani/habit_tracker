import sqlite3

class DataBase:
    def __init__(self):
        self.sqliteConnection = sqlite3.connect(r"C:\Users\abdel\Documents\Habit_Tracker.db")
        self.cursor = self.sqliteConnection.cursor()


    def saveData(self, data):
        cursor = self.cursor
        try:
            if data["ID"] == "user":
                cursor.execute(f"INSERT INTO USER (name,email,password) VALUES ('{data["name"]}', '{data ["email"]}', '{data["password"]}')")
                self.sqliteConnection.commit()
                print("Query executed successfully.")
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
        

    def loadData(self):
        try:
            pass
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

