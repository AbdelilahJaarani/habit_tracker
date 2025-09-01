from habitTemplate import HabitTemplate
from dataStorage import DataBase
from datetime import datetime
import time
import os
DATABASE = DataBase()
HABIT_TEMPLATE = HabitTemplate()
LOCAL_TIME = time.localtime()
CHECK = True 


class Habit:
    """Interactively create, list, edit, complete, and delete habits for a user."""

    def __init__(self):
        """Initialize habit properties and fetch template options (categories, periodicity, weekdays)."""
        self.habit_id = None
        self.name = None
        self.category = HABIT_TEMPLATE.list_catergory()
        self.description = None
        self.periodicity = HABIT_TEMPLATE.list_periodicity()
        self.weekdays = HABIT_TEMPLATE.get_weekdays()
        self.status = 0
        self.startDate = datetime.now().strftime("%Y-%m-%d")

    def choose_from_list(self,prompt,options):
        """
        Prompt for a selection from numbered options and return the chosen value.

        Args:
            prompt (str): Instructional message to display.
            options (list[str]): Options to choose from.
        Returns:
            str: The selected option string.
        """
        while True:
            print(prompt)
            for i, option in enumerate(options,1):
                print(f"[{i}]:{option}")
            try:
                choice = int(input("> "))
                if 1 <= choice < len(options)+1:
                    return options[choice-1] #
                else:
                    print("Invalid number! Please try it again.\n")
            except ValueError:
                print("Please give a number.\n")

    def add(self, user_data):
        """
        Collect inputs to create a new habit and persist it. 

        Args:
            user_data (dict): Must contain 'user_id'. 
        """
        NewHabit = {}
        os.system('cls')
        print("== New Habit ==")

        #Category should be choosen 
        choosen_category = self.choose_from_list(prompt="Choose a Category",options=self.category)
        self.name = input("What should your habit be?:\n>")

        NewHabit.update({f"user_id":user_data["user_id"],
                         "category":choosen_category,
                         "habit":self.name})
        os.system('cls')
        self.description = input("Description: \n")
        if self.description:
            NewHabit.update({"description": self.description})
           
        #Intervall should be choosen
        choosen_interval = self.choose_from_list(prompt= "In which period do you want to ",options= self.periodicity)
        NewHabit.update({"periodicity":choosen_interval})
        if choosen_interval == "weekly":
            choosen_day = self.choose_from_list(prompt="Which Weekday should the habit be done?", options= self.weekdays)
            NewHabit.update({"weekday": choosen_day})
        else:
            NewHabit.update({"weekday": ''})
        
        NewHabit.update({"status":self.status,"startDate":self.startDate})
        os.system('cls')
        print("Habit is saving...:\n")
        #Saving into the Database 
        
        time.sleep(2)
        DATABASE.save_data_Habit(NewHabit)



    def add_habit_template(self, user_data):
        """
        Offer random templates until accepted; save accepted template as a new habit. 

        Args:
            user_data (dict): Must contain 'user_id'. 
        Returns:
            dict | None: Saved template data on success, or None if exited.
        """
        TemplateHabit = {}
        while CHECK: 
            print(f"Here an daily Habit example:\nCategory: {HABIT_TEMPLATE.template_examples()["category"]} \nHabit: {HABIT_TEMPLATE.template_examples()["habits"]}\nIntervall: {HABIT_TEMPLATE.template_examples()["intervall"]}")
            choice = input("Do want adding this Habit into your list [y] [n]\nFor exit press [x] ? ")
            if choice == "y":
                TemplateHabit.update({"user_id": user_data["user_id"],
                                      "category": HABIT_TEMPLATE.template_examples()["category"],
                                      "habit": HABIT_TEMPLATE.template_examples()["habits"], 
                                      "description": "", 
                                      "periodicity": "daily",
                                      "status":self.status,
                                      "startDate":self.startDate,
                                      "weekday":''})
                #self.add(ht.templatesExamples())
                # print(TemplateHabit)
                os.system('cls')
                print("Template is saving...")
                time.sleep(2)
                if DATABASE.save_data_Habit(TemplateHabit):
                    print("Habit Template created :) ! ")

            elif choice == "n":
                os.system('cls')
            elif choice == "x":
                os.system('cls')
                return None
   
            else:
                os.system('cls')
                print("Wrong input!")
                time.sleep(1)
                os.system('cls')
        

    def mark_as_completed(self,user_data):
        """
        For each habit not yet completed today, ask done/not done and record it.

        Args:
            user_data (dict): Must contain 'user_id'. 
        """
        markedHabit = {}

        def bold(text):
            return f"\033[1m{text}\033[0m"
        
        while True:
            if DATABASE.check_any_habit_in_db(data= user_data):

                _, habitDict = DATABASE.load_data_Habit(data=user_data)
                if user_data:
                    for dict in habitDict:
                        if DATABASE.check_if_habit_already_done(dict):
                            continue
                        try:
                            mark = int(input("Did you complete today:\n"+
                                        f"{bold(dict["habit"])}""\n"+
                                        "{:<25} [{}]\n".format("Yes",1) +
                                        "{:<25} [{}]\n".format("No",2)))
                            if mark == 1:
                                # if data.check_if_habit_already_done(data=user_data):
                                #     print("Habit is already marked as done today!")
                                print("GOOD JOB!")
                                markedHabit.update({"habit_id":dict["habit_id"],"completion_date":self.startDate,"status": 1})
                                DATABASE.mark_complete_habit(markedHabit)
                                
                            elif mark ==2:
                                print("DON'T GIVE UP!\nDo it or try it tomorrow")
                                markedHabit.update({"habit_id":dict["habit_id"],"completion_date":self.startDate,"status": 0})
                                DATABASE.mark_complete_habit(markedHabit)
                            else: 
                                os.system('cls')
                                print("Wrong input!")
                                time.sleep(1)
                                os.system('cls')
                        except ValueError:
                            print("Only Numbers please!")
                            continue
                    
                    break
            else:
                print("You don't have any habits! Create first some!")
                break


    def show_habit(self,user):
        """
        Return a printable table string of the user's habits.

        Args:
            user (dict): Must contain 'user_id'.
        Returns:
            str: Table string from the database query.
        """
        habit_str,_ = DATABASE.load_data_Habit(user)
        return habit_str
        

    def edit_habit(self,user_data):
        """
        Interactively update a habit's category, name, description, or periodicity.

        Args:
            user_data (dict): Must contain 'user_id'.
        """
        def update_input(clm):
            update = input("Write your change:\n" + clm + "\n" +
                           ">")
            os.system('cls')
            return update

        while True:
            habitString,AllHabitsInList = DATABASE.load_data_Habit(user_data)

            self.habit_id = input("Which Habit do you want to change?\n"+
                                "Write the habit ID Number please or [x] for exit :\n"+
                                str(habitString)+"\n"+
                                "\n"+">")
            
            if self.habit_id == "x":
                os.system('cls')
                print("back to menue..")
                time.sleep(2)
                os.system('cls')
                break
                
            try:
                habit_id = int(self.habit_id)
            except ValueError:
                print("Only Numbers or x for exit")
                continue
            
            for dict in AllHabitsInList:
                if habit_id == dict["habit_id"]:
                    try:
                        changeInfo = int(input(
                                    "What do you want to change?\n" +
                                    "{:<25} [{}]\n".format("Category",1) +      
                                    "{:<25} [{}]\n".format("Habitname",2) +
                                    "{:<25} [{}]\n".format("Description",3)+
                                    "{:<25} [{}]\n".format("Periodicity",4)+
                                    "{:<25} [{}]\n".format("Exit",0)))
                        if changeInfo == 1:
                            choosen_category = self.choose_from_list(prompt="Choose the new Category",options=self.category)
                            DATABASE.update_data_habit(data=dict,update=choosen_category,part="category")
                        elif changeInfo == 2:
                            change = update_input(clm=dict["habit"])
                            DATABASE.update_data_habit(data=dict,update= change, part="habit")
                        elif changeInfo == 3:
                            change = update_input(clm=dict["description"])
                            DATABASE.update_data_habit(data=dict,update= change, part="description")
                        elif changeInfo == 4:
                            choosen_interval = self.choose_from_list(prompt= "In which period do you want to change ",options= self.periodicity)
                            if choosen_interval == "weekly":
                                choosen_day = self.choose_from_list(prompt="Which Weekday should the habit be done?", options= self.weekdays)
                                DATABASE.update_data_habit(data=dict,update=choosen_interval,part="periodicity")
                                DATABASE.update_data_habit(data=dict,update=choosen_day,part="weekday")
                            else:
                                DATABASE.update_data_habit(data=dict,update=choosen_interval,part="periodicity")
                        elif changeInfo == 0:
                            break
                        else:
                            os.system('cls')
                            print("Wrong Input")
                                  
                    except ValueError:
                        print("Only Numbers are allowed")
                        break

                


    def delete(self,user_data):
        """
        Prompt for a habit id, confirm, and delete the habit if confirmed.

        Args:
            user_data (dict): Must contain 'user_id'.
        """
        while True:
            habit_str,all_habits_in_list = DATABASE.load_data_Habit(user_data)

            self.habit_id = input("Which Habit do you want to delete?\n"+
                                "Write the habit ID Number please or [x] for exit :\n"+
                                str(habit_str)+"\n"+
                                "\n"+">")
            
            if self.habit_id == "x":
                os.system('cls')
                print("back to menue..")
                time.sleep(2)
                os.system('cls')
                break
            
                
            try:
                habit_id = int(self.habit_id)
            except ValueError:
                print("Only Numbers or x for exit")
                os.system('cls')
                continue
            
            for dict in all_habits_in_list:
                if habit_id == dict["habit_id"]:
                    try:
                        os.system('cls')
                        mark = int(input("Are you sure to delete :\n"+
                        f"{(dict["habit"])}""\n"+
                        "{:<25} [{}]\n".format("Yes",1) +
                        "{:<25} [{}]\n".format("No",2)))

                        if mark == 1:
                            os.system('cls')
                            print("Deleting...")
                            time.sleep(2)
                            if DATABASE.delete_data_habit(data=dict):
                                os.system('cls')
                                print("Habit deleted!")
                                os.system('cls')
                        elif mark == 2: 
                            break
                        else: 
                            os.system('cls')
                            print("Wrong input!")
                            time.sleep(1)
                            os.system('cls')
                            break        
                    except ValueError:
                        print("Only Numbers are allowed")
                        break
        