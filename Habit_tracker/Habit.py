from habitTemplate import HabitTemplate
from dataStorage import DataBase
from datetime import datetime
import time
import os
data = DataBase()
ht = HabitTemplate()
local_time = time.localtime()
check = True 


class Habit:
    def __init__(self):
        self.habitID = None
        self.name = None
        self.category = ht.listCatergory()
        self.description = None
        self.periodicity = ht.listPeriodicity()
        self.weekdays = ht.getWeekdays()
        self.status = 0
        self.startDate = datetime.now().strftime("%Y-%m-%d")

    def choose_from_list(self,prompt,options):
        #Helpfunction for secure selection form a list
        
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
        #creating a new Habit by the User
        NewHabit = {}
        os.system('cls')
        print("== New Habit ==")

        #Category should be choosen 
        choosen_category = self.choose_from_list(prompt="Choose a Category",options=self.category)
        self.name = input("What should your habit be?:\n>")

        NewHabit.update({f"user_id":user_data,
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
        
        NewHabit.update({"status":self.status,"startDate":self.startDate})
        # print(NewHabit)
        os.system('cls')
        print("Habit is saving...:\n")
        #Saving into the Database 
        
        time.sleep(2)
        data.saveData_Habit(NewHabit)



    def addHabitTemplate(self, user_data):
        #creating a new habit from the Templates and save it into the Db
        TemplateHabit = {}
        while check: 
            print(f"Here an daily Habit example:\nCategory: {ht.templatesExamples()["category"]} \nHabit: {ht.templatesExamples()["habits"]}\nIntervall: {ht.templatesExamples()["intervall"]}")
            choice = input("Do want adding this Habit into your list [y] [n]\nFor exit press [x] ? ")
            if choice == "y":
                TemplateHabit.update({"user_id": user_data,
                                      "category": ht.templatesExamples()["category"],
                                      "habit": ht.templatesExamples()["habits"], 
                                      "description": "", 
                                      "periodicity": "daily",
                                      "status":self.status,
                                      "startDate":self.startDate})
                #self.add(ht.templatesExamples())
                # print(TemplateHabit)
                os.system('cls')
                print("Template is saving...")
                time.sleep(2)
                if data.saveData_Habit(TemplateHabit):
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
        

    def delete(self):
        #deleting habit which is used by the user 
        pass

    def markAsCompleted(self,user_data):

        def bold(text):
            return f"\033[1m{text}\033[0m"
        
        #mark the habit as Done if user already has done it. 
        while True:
            _, habitDict = data.loadData_Habit(data=user_data)
            for dict in habitDict:
                mark = int(input("Did you complete today:\n"+
                            f"{bold(dict["habit"])}""\n"+
                            "{:<25} [{}]\n".format("Yes",1) +
                            "{:<25} [{}]\n".format("No",2)))
                if mark == 1:
                    pass
                elif mark ==2:
                    pass
                else: 
                    os.system('cls')
                    print("Wrong input!")
                    time.sleep(1)
                    os.system('cls')

        #print(bold(habitDict))
        print(type(habitDict))
        # print(data.ShowOnlyHabits(data=user_data))
        # print(type(data.ShowOnlyHabits(data=user_data)))

    def showHabit(self,user):
        #strUser = str(user)
        habitString,_ = data.loadData_Habit(user)
        return habitString
        

    def editHabit(self):
        #modify the Habit which is created from the user
        pass


# SetReminder not nessarry 
    # def setReminder(self):
    #     #add also an reminder which send a message to the User {LOOKING EXACTLY HOW JET}
    #     pass