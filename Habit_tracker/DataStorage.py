import sqlite3
import pandas as pd
import os
from datetime import datetime

class DataBase:
    def __init__(self):
        DBPATH = r"C:\Users\abdel\Documents\Habit_Tracker\habit_tracker\Habit_Tracker.db"
        self.sqliteConnection = sqlite3.connect(DBPATH)
        self.cursor = self.sqliteConnection.cursor()
        self.date_today = datetime.now().strftime("%Y-%m-%d")


    def save_data_user(self, data):
        """
        Save a new user in the USER table and return the new user row.
        """
        cursor = self.cursor
        try:
            if data:
                cursor.execute(
                    "INSERT INTO USER (name,email,password) VALUES (?, ?, ?)",
                    (data["name"], data["email"], data["password"])
                )
                self.sqliteConnection.commit()
                user_id = cursor.lastrowid
                cursor.execute("SELECT * FROM USER WHERE user_id = ?", (user_id,))
                user_data = cursor.fetchone()
                user_id = {"user_id":user_data[0],"name": user_data[1], "email":user_data[2],"password":user_data[3]}
                return True, user_id
        except sqlite3.IntegrityError as e:
            os.system('cls')
            print(f"The email '{data['email']}' is already used. Please use another one")
            return False, None
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
            return False, None
        

    def load_data_User(self, data):
        """
        Authenticates a user by checking if the combination of email and password exists in the database.
        
        Args:
            data (dict): Must contain 'email' and 'password' as keys. Example:
                {'email': 'user@example.com', 'password': 'userpassword'}
        
        Returns:
            tuple: (True, user_data) if user is found, otherwise (False, None).
                user_data contains the (user_id, email, password) tuple from the USER table.
        
        Side Effects:
            Prints error information if a database problem occurs.
        """
        cursor = self.cursor
        try:
            if data:
                # Remove possible empty spaces for reliability
                email = data["email"].strip()
                password = data["password"].strip()

                cursor.execute(
                    "SELECT user_id, name, email, password FROM USER WHERE email = ? AND password = ?",
                    (email, password)
                )
                user_data = cursor.fetchone()
                if user_data is None:
                    return False, None
                else:
                    user_id = {"user_id":user_data[0],"name": user_data[1], "email":user_data[2],"password":user_data[3]}
                    return True, user_id
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
            return False, None
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
            return False, None


    def update_data_user(self,data,part,update):
        cursor = self.cursor
        try:
            if data:
                cursor.execute(f"UPDATE USER SET {part} = ? WHERE user_id = ?",
                               (update,data["user_id"]))
                self.sqliteConnection.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")

    def show_only_user_information(self,data):
        try:
            if data:
                df = pd.read_sql_query(f"SELECT user_id,name,email FROM USER WHERE user_id = ?",self.sqliteConnection,params=(data["user_id"],))
                df_to_dict = df.to_dict(orient="records")              
                return df, df_to_dict
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
        

    def delete_data_user (self, user_data, habit_data):
        cursor = self.cursor        
        if self.delete_all_habits_after_user_deleted(data=user_data,habitData=habit_data):
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




    ########################################################## Habit Storage #####################################################################


    def mark_complete_habit(self,data):

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
                               (data["habit_id"], self.date_today,1))               
                record = cursor.fetchone()
                if record:
                    return True
                else:
                    return False
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
        
    def check_any_habit_in_db(self,data):

        cursor = self.cursor
        try:
            if data:
                cursor.execute(f"SELECT user_id FROM habits WHERE user_id = ?", 
                               ( data["user_id"],))               
                record = cursor.fetchone()
                if record:
                    return True
                else:
                    return False
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")


        
    def save_data_Habit(self, data):

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
        

    def load_data_Habit(self,data):

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
    
    def get_all_Habit_id(self,data):
        cursor = self.cursor
        try:
            if data:
                cursor.execute(
                    "SELECT habit_id FROM habits",    
                )
                habit_id_list = [row[0] for row in cursor.fetchall()]
                return habit_id_list
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
        except sqlite3.OperationalError as e:
            print(f"Operational Error: {e}")
        

    def update_data_habit(self,data,update,part):

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

    def show_only_habits(self,data):

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

    
    def delete_data_habit(self, data):
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
        
        
    def delete_all_habits_after_user_deleted(self,data,habitData):
        cursor = self.cursor        
        try:
            if data:
                for habit_id in habitData:
                    cursor.execute("DELETE from habit_completion WHERE habit_id = ?",
                                (habit_id,)
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
        
    def _get_completion_dates(self, habit_id):
        cursor = self.cursor
        cursor.execute(
            "SELECT completion_date FROM habit_completion WHERE habit_id = ? AND status = 1 ORDER BY completion_date",
            (habit_id,))
        dates = cursor.fetchall()
        dates_dt = [datetime.strptime(d[0], "%Y-%m-%d") for d in dates]
        return dates_dt