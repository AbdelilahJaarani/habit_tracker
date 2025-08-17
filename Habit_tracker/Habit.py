from habitTemplate import HabitTemplate
#from habitTracker import HabitTracker
from datetime import datetime
import time
import os
#home = HabitTracker()
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

        NewHabit.update({f"category":choosen_category,"habit":self.name})
        os.system('cls')
        self.description = input("Description: \n")
        if self.description:
            NewHabit.update({"description": self.description})
           
        #Intervall should be choosen
        choosen_interval = self.choose_from_list(prompt= "In which period do you want to ",options= self.periodicity)
        NewHabit.update({"intervall":choosen_interval})
        if choosen_interval == "weekly":
            choosen_day = self.choose_from_list(prompt="Which Weekday should the habit be done?", options= self.weekdays)
            NewHabit.update({"weekday": choosen_day})
        
        NewHabit.update({"status":self.status,"startday":self.startDate})

        print("Habit was created:")
        #Saving into the Database 
        print(NewHabit)



    def addHabitTemplate(self, user_data):
        #creating a new habit from the Templates and save it into the Db
        TemplateHabit = {}
        while check: 
            print(f"Here an example:\n {ht.templatesExamples()["category"]}: {ht.templatesExamples()["habits"]}")
            choice = input("Do want adding this Habit into your list [y] [n]\nFor exit press [x] ? ")
            if choice == "y":
                TemplateHabit.update({"category":ht.templatesExamples()["category"]})
                self.add(ht.templatesExamples())
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

    def markAsCompleted(self):
        #mark the habit as Done if user already has done it. 
        pass

    def showHabit(self):
        #showing specific Habit with all information for the User 
        pass

    def editHabit(self):
        #modify the Habit which is created from the user
        pass

    def setReminder(self):
        #add also an reminder which send a message to the User {LOOKING EXACTLY HOW JET}
        pass