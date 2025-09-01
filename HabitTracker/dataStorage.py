import sqlite3
import pandas as pd
import os
from datetime import datetime

class DataBase:
    # """Lightweight SQLite wrapper for user and habit persistence.

    # IMPORTANT:
    # - The database path (DBPATH) below is set for the local machine only.
    # - Each user should adjust DBPATH to point to their own database file location.
    # - Example for Windows:  r"C:\Users\<yourName>\path\to\Habit_Tracker.db"
    # - Example for Mac/Linux:  "/home/<yourName>/path/to/Habit_Tracker.db"
    # - Alternatively, you can use a relative path (e.g., "Habit_Tracker.db" in the current working directory).
    # """

    def __init__(self):
        """Opens a SQLite connection and initializes helper objects (cursor, today’s date).

        NOTE:
        - Please adjust the DBPATH to your own local path where your SQLite database is stored.
        - Use the format shown above for your operating system.
        """
        DBPATH = "C:\\Users\\abdel\\Documents\\Habit_Tracker.db"
        self.sqliteConnection = sqlite3.connect(DBPATH)
        self.cursor = self.sqliteConnection.cursor()
        self.date_today = datetime.now().strftime("%Y-%m-%d")


    def save_data_user(self, data):
        """
        Create a new user row and return the stored record.

        Args:
            data (dict): Keys 'name', 'email', 'password'.
        Returns:
            tuple[bool, dict | None]: (True, user_dict) on success; else (False, None).
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
        """
        Update a single user field and commit.

        Args:
            data (dict): Must contain 'user_id'.
            part (str): Column name to update.
            update (Any): New value for the column.
        Returns:
            bool: True if update executed (exceptions print errors).
        """
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
        """
        Return basic profile info for a user as DataFrame and dict.

        Args:
            data (dict): Must contain 'user_id'.
        Returns:
            tuple[pd.DataFrame, list[dict]]: (df, records) with user_id, name, email.
        """
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
        """
        Delete a user and their related habit records.

        Args:
            user_data (dict): Must contain 'user_id'.
            habit_data (list[int]): Habit IDs owned by the user.
        Returns:
            bool: True if user row was deleted and committed.
        """
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
        """
        Insert a habit completion record for a given date and status.

        Args:
            data (dict): {'habit_id': int, 'completion_date': 'YYYY-MM-DD', 'status': int}.
        Returns:
            tuple[bool, dict | None]: (True, data) on success; else (False, None).
        """
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
        """
        Return True if the habit is already completed today (status=1).

        Args:
            data (dict): Must contain 'habit_id'.
        Returns:
            bool: True if a completion exists for today; otherwise False.
        """
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
        """
        Return whether the user has at least one habit in storage.

        Args:
            data (dict): Must contain 'user_id'.
        Returns:
            bool: True if a habit row exists; otherwise False.
        """
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
        """
        Insert a new habit for the user.

        Args:
            data (dict): Keys 'user_id','category','habit','description','periodicity','status','startDate','weekday'.
        Returns:
            tuple[bool, dict | None]: (True, data) on success; else (False, None).
        """
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
        """
        Load all habits for a user as DataFrame and dict records.

        Args:
            data (dict): Must contain 'user_id'.
        Returns:
            tuple[pd.DataFrame, list[dict]]: (df, records) with habit fields.
        """
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
        """
        Return a list of all habit IDs.

        Args:
            data (dict): Unused; kept for interface consistency.
        Returns:
            list[int]: Habit IDs across all users.
        """
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
        """
        Update a single habit field and commit.

        Args:
            data (dict): Must contain 'habit_id'.
            update (Any): New value to set.
            part (str): Column name to update.
        """
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
        """
        Return a left-aligned table string of habit names for the user.

        Args:
            data (dict): Must contain 'user_id'.
        Returns:
            str: Formatted table of habit names.
        """
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
        """
        Delete a habit row by its id.

        Args:
            data (dict): Must contain 'habit_id'.
        """
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
        """
    Delete all habit data for a user after the user record is removed.

    Deletes completions for each habit_id in habitData, then deletes the
    user's habits, and commits the transaction.
    Args:
        data (dict): User dict containing 'user_id'.
        habitData (list[int] | list[str]): Habit IDs associated with the user.
    Returns:
        bool: True if deletion and commit succeeded; otherwise None.
    Raises:
        sqlite3.IntegrityError: If a foreign key or integrity constraint fails.
        sqlite3.OperationalError: For SQL execution or database operation issues.
    """
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
        """
    Return ordered completion dates (as datetime) for a given habit.

    Fetches status=1 completions for habit_id and converts them from
    'YYYY-MM-DD' strings to datetime objects, sorted ascending.
    Args:
        habit_id (int | str): The habit identifier.
    Returns:
        list[datetime]: Completion dates ordered by completion_date.
    """
        cursor = self.cursor
        cursor.execute(
            "SELECT completion_date FROM habit_completion WHERE habit_id = ? AND status = 1 ORDER BY completion_date",
            (habit_id,))
        dates = cursor.fetchall()
        dates_dt = [datetime.strptime(d[0], "%Y-%m-%d") for d in dates]
        return dates_dt