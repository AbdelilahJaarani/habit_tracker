import random

class HabitTemplate:
    def __init__(self):
        self.category = []
        self.peridicity = []
        
    
    def listCatergory(self):
        habit_categories = [
            "Health & Fitness",
            "Nutrition",
            "Personal Development",
            "Productivity & Work",
            "Household & Organization",
            "Finances",
            "Social & Relationships",
            "Creativity & Hobbies",
            "Self-care & Well-being",
            "Miscellaneous / Custom"
        ]
        self.category = habit_categories
        return self.category
    
    
    def listPeriodicity(self):
        periodicty = ["daily", "weekly", "monthly"]
        self.peridicity = periodicty
        return periodicty

    def ListTemplates(self):
        #able to import other Habit and integrates into the system 
        habits = [
        {
            "category": "Health & Fitness",
            "habits": [
                "Morning stretch routine: 5-10 minutes of stretching after waking up",
                "Interval training (HIIT) 2-3 times per week",
                "Walk at least 10,000 steps daily",
                "Go to bed at the same time every day (aim for 7-8 hours of sleep)"
            ]
        },
        {
            "category": "Nutrition",
            "habits": [
                "Drink at least 2-3 liters of water daily",
                "Prepare meals weekly (meal prep)",
                "Make at least 50% of every meal vegetables",
                "Limit processed sugar and sweets to 1-2 times per week"
            ]
        },
        {
            "category": "Personal Development",
            "habits": [
                "Read for 15-30 minutes every day",
                "Spend 5 minutes journaling every evening",
                "Make weekly progress learning a new skill",
                "Reflect on personal goals and progress for 10 minutes weekly"
            ]
        },
        {
            "category": "Productivity & Work",
            "habits": [
                "Use the Pomodoro technique: 25 minutes work, 5 minutes break",
                "Set the three most important tasks every morning",
                "Check emails only 2-3 times per day",
                "Organize your desk for 5 minutes daily"
            ]
        },
        {
            "category": "Household & Organization",
            "habits": [
                "Spend 10 minutes daily tidying up a specific area",
                "Schedule fixed days for laundry and folding",
                "Declutter one box of items monthly",
                "Check off weekly cleaning tasks in a calendar"
            ]
        },
        {
            "category": "Finances",
            "habits": [
                "Track all expenses immediately or use an app",
                "Automatically save a fixed amount every month",
                "Review income and expenses monthly",
                "Apply the 24-hour rule before major purchases"
            ]
        },
        {
            "category": "Social & Relationships",
            "habits": [
                "Contact at least one person daily (call, message, or meet)",
                "Practice active listening in conversations",
                "Thank someone or give a compliment at least once a week",
                "Regularly schedule time for friends or family"
            ]
        },
        {
            "category": "Creativity & Hobbies",
            "habits": [
                "Reserve 15-30 minutes daily for a hobby",
                "Note down new ideas or inspirations every day",
                "Try a new creative technique or hobby monthly",
                "Participate in creative challenges"
            ]
        },
        {
            "category": "Self-care & Well-being",
            "habits": [
                "Practice meditation or breathing exercises for 5-10 minutes daily",
                "Have one hour of screen-free time each day",
                "Say positive affirmations to yourself in the morning",
                "Take a short break every 60-90 minutes"
            ]
        },
        {
            "category": "Miscellaneous / Custom",
            "habits": [
                "Review progress in all life areas weekly",
                "Write down three things you are grateful for every day",
                "Do one eco-friendly action daily",
                "Practice a foreign language for 5-10 minutes daily"
            ]
        }
        ]
        return habits

hb = HabitTemplate()
rdHabit = hb.ListTemplates()
newTemplate = {}
#newTemplate[random.choice(rdHabit["category"])] = random.choice(rdHabit["habits"])
oneDict = random.choice(rdHabit)
newCategory = oneDict["category"]
newHabit = random.choice(oneDict["habits"])

print(oneDict)
print(newCategory)
print(newHabit)
