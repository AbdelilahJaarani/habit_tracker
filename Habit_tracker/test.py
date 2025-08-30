from habitTracker import HabitTracker
import time 
ht = HabitTracker()
import calendar
from datetime import datetime

# todaysDate = datetime.now()
# formatted_todaysDate = todaysDate.strftime("%Y-%m-%d")


# print(formatted_todaysDate)

#print ("What do you want to change ?\n [1] Name \n [2] Email \n [3] Password")
data = {"user_id": 1}
ht.start_plattform(UserID=data)

# testData= {"name":"Abdelilah", "email": "abdelilah@gmail.com"}

# class test: 
#     def __init__(self):
#         pass

#     def testing (self,data):
#         if data:
#             print(data)
#             print("Hat Funktioniert")


# t = test()

# t.testing(data=testData)
