import sqlite3
import pandas as pd
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


    def markComplete_Habit(self,data):
        cursor = self.cursor
        try:
            if data:
                cursor.execute(
                    "INSERT INTO habit_completion (habit_id,completion_date,status,)VALUES (?,?,?,)",
                    (data["habit_id"],data["completion_date"],data["status"])
                )
                self.sqliteConnection.commit()
                return True, data
        except sqlite3.Error as e:
            print(f"Integrity Error: {e}")
            return False, None        
        
        pass

    def check_if_habit_already_done(self,data):
        cursor = self.cursor
        try:
            if data:
                cursor.execute("SELECT habit_id, completion_date FROM habit_completion WHERE habit_id = ? AND completion_date = ?", (data["habit_id"], data["completion_date"]))
                return cursor.fetchone() is not None
                
                user_data = cursor.fetchone()
                if user_data is None:
                    return False
                else:
                    return True
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
        
    
        
    def saveData_Habit(self, data):
        #save Habit into DB 
        cursor = self.cursor
        try:
            if data:
                cursor.execute(
                    "INSERT INTO habits (user_id,category,habit,description,periodicity,status,startDate)VALUES (?,?,?,?,?,?,?)",
                    (data["user_id"],data["category"],data["habit"], data["description"], data["periodicity"], data["status"],data["startDate"])
                )
                self.sqliteConnection.commit()
                return True, data
        except sqlite3.Error as e:
            print(f"Integrity Error: {e}")
            return False, None
        

    def loadData_Habit(self,data):
        cursor = self.cursor
        try:
            if data:
                df = pd.read_sql_query(f"SELECT habit_id,category,habit,description,periodicity,startDate FROM habits WHERE user_id = ?",self.sqliteConnection,params=(data["user_id"],))
                df_to_dict = df.to_dict(orient="records")
                
                return df, df_to_dict
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

    def ShowOnlyHabits(self,data):
        try:
            if data:
                df = pd.read_sql_query("SELECT habit AS 'Habits' FROM habits WHERE user_id = ?",
                                       self.sqliteConnection,
                                       params=(data["user_id"],))
                maxlen = df["Habits"].astype(str).str.len().max()
                formatters = {"Habits":lambda x: f"{x:<{maxlen}}"}
                return df.to_string(formatters= formatters, justify= "center")
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")        

        
    # Not necessary
    # def restoreData_Habit(self):
    #     try:
    #         pass
    #     except sqlite3.IntegrityError as e:
    #         print(f"Integrity Error: {e}")
    #     except sqlite3.OperationalError as e:
    #         print(f"Operational Error: {e}")
    
    def deleteData_Habit(self, data):
        pass
        
        
    def close(self):
        pass

