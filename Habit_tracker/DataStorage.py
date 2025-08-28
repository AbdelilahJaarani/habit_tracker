import sqlite3
import pandas as pd
import os
from datetime import datetime

class DataBase:
    def __init__(self):
        self.sqliteConnection = sqlite3.connect(r"C:\Users\abdel\Documents\Habit_Tracker.db")
        self.cursor = self.sqliteConnection.cursor()
        self.dayToday = datetime.now().strftime("%Y-%m-%d")


    def saveData_User(self, data):
        #save data for 
        cursor = self.cursor
        try:
            if data:
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
            if data:
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

    def ShowOnlyUserInformation(self,data):
        try:
            if data:
                df = pd.read_sql_query(f"SELECT user_id,name,email FROM USER WHERE user_id = ?",self.sqliteConnection,params=(data["user_id"],))
                df_to_dict = df.to_dict(orient="records")              
                return df, df_to_dict
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
        

    def deleteData_User (self, user_data, habit_data):
        cursor = self.cursor        
        if self.deleteAllHabitsAfterUserDeleted(data=user_data,habitData=habit_data):
            try:
                if user_data:
                    cursor.execute("DELETE from USER WHERE user_id = ?",
                                (user_data["user_id"],)
                                )
                    self.sqliteConnection.commit()
                    return True
                    
            except sqlite3.IntegrityError as e:
                print(f"Integrity Error: {e}")
            except sqlite3.OperationalError as e:
                print(f"Operational Error: {e}")
            pass
    ########################### Habit Storage ########################################


    def markComplete_Habit(self,data):

        # """
        # Insert a new completion record for a habit on a given date with completion status.

        # Args:
        #     data (dict): A dictionary with keys:
        #         - 'habit_id': int, the unique ID of the habit completed
        #         - 'completion_date': str, the date the habit was completed (format 'YYYY-MM-DD')
        #         - 'status': int, completion status (typically 1 for done, 0 for not done)

        # Returns:
        #     tuple: (True, data) if insertion succeeded and was committed,
        #         (False, None) if there was a database error.

        # Side Effects:
        #     Writes a new record into the 'habit_completion' table and commits the change.
        #     Prints error messages if the operation fails.
        # """

        cursor = self.cursor
        try:
            if data:
                cursor.execute(
                    "INSERT INTO habit_completion (habit_id, completion_date, status) VALUES (?, ?, ?)",
                    (data["habit_id"],data["completion_date"],data["status"])
                )
                self.sqliteConnection.commit()
                return True, data
        except sqlite3.Error as e:
            print(f"Integrity Error: {e}")
            return False, None        
        
        pass

    def check_if_habit_already_done(self,data):

        # """
        # Check if a habit has already been marked as completed for today.

        # Args:
        #     data (dict): A dictionary with at least 'habit_id'.
        #         Assumes self.dayToday provides the current date as a string.

        # Returns:
        #     bool: True if the habit is already completed for today and status=1, False otherwise.

        # Side Effects:
        #     Queries the 'habit_completion' table.
        #     Prints errors if the query fails.
        # """

        cursor = self.cursor
        try:
            if data:
                cursor.execute(f"SELECT habit_id FROM habit_completion WHERE habit_id = ? AND completion_date = ? AND status = ?", 
                               (data["habit_id"], self.dayToday,1))               
                record = cursor.fetchone()
                if record:
                    return True
                else:
                    return False
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
        
    
        
    def saveData_Habit(self, data):

        # """
        # Save a new habit record to the 'habits' table in the database.

        # Args:
        #     data (dict): Dictionary containing all fields required for a new habit:
        #         - 'user_id', 'category', 'habit', 'description', 'periodicity', 
        #         'status', 'startDate', 'weekday'

        # Returns:
        #     tuple: (True, data) if successful, (False, None) on failure.

        # Side Effects:
        #     Inserts a new row into 'habits' and commits.
        #     Prints database error messages.
        # """

        cursor = self.cursor
        try:
            if data:
                cursor.execute(
                    "INSERT INTO habits (user_id,category,habit,description,periodicity,status,startDate,weekday)VALUES (?,?,?,?,?,?,?,?)",
                    (data["user_id"],data["category"],data["habit"], data["description"], data["periodicity"], data["status"],data["startDate"],data['weekday'])
                )
                self.sqliteConnection.commit()
                return True, data
        except sqlite3.Error as e:
            print(f"Integrity Error: {e}")
            return False, None
        

    def loadData_Habit(self,data):

        #     """
        # Load all habit records for a specific user from the database.

        # Args:
        #     data (dict): Must contain 'user_id' (the user's identifier)

        # Returns:
        #     tuple: (DataFrame, List[dict]) — the habits as a pandas DataFrame and as a list of dictionaries.
        #     Returns None if an error occurs.

        # Side Effects:
        #     Reads from the 'habits' table.
        #     Prints errors if query fails.
        #     """

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

    def UpdateData_Habit(self,data,update,part):

        # """
        # Update a specific field of a habit in the database.

        # Args:
        #     data (dict): Dictionary with at least 'habit_id' key (target habit).
        #     update (Any): The new value to set.
        #     part (str): The column name to update (must be sanitized before use!).

        # Returns:
        #     None

        # Side Effects:
        #     Updates a field in the 'habits' table, commits the change.
        #     Prints an error if something goes wrong.
        # """
            
        cursor = self.cursor        
        try:
            if data:
                cursor.execute(f"UPDATE habits SET {part} = ? WHERE habit_id = ?",
                               (update,data["habit_id"]))
                self.sqliteConnection.commit()
                
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")

    def ShowOnlyHabits(self,data):

        #"""
        # Return a formatted string of all habit names for the given user.

        # Args:
        #     data (dict): Must contain 'user_id'.

        # Returns:
        #     str: Table of user habits, each left-aligned to the longest habit name.
        #     None if an error occurs.

        # Side Effects:
        #     Reads from the database, prints errors on failure.
        # """
            
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

    
    def deleteData_Habit(self, data):
        #     """
        # Delete a habit from the database based on habit_id.

        # Args:
        #     data (dict): Must contain 'habit_id' (unique identifier for the habit).

        # Returns:
        #     None

        # Side Effects:
        #     Removes the matching habit from the 'habits' table.
        #     Commits the change.
        #     Prints errors if the operation fails.
        # """

        cursor = self.cursor        
        try:
            if data:
                cursor.execute("DELETE from habits WHERE habit_id = ?",
                               (data["habit_id"],)
                               )
                self.sqliteConnection.commit()
                
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
        
        
    def deleteAllHabitsAfterUserDeleted(self,data,habitData):
        cursor = self.cursor        
        try:
            if data:
                cursor.execute("DELETE from habit_completion WHERE habit_id = ?",
                            (habitData["habit_id"],)
                            )
                cursor.execute("DELETE from habits WHERE user_id = ?",
                            (data["user_id"],)
                            )
                self.sqliteConnection.commit()
                return True                   
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
        