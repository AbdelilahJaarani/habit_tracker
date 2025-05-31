import random

class HabitTemplate:
    def __init__(self):
        self.category = []
        self.peridicity = []
        
    
    def listCatergory(self):
        #list of category that the user can use
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
        #list of periodicity that the user can use
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
                "Interval training (HIIT)",
                "Walk at least 10,000 steps",
                "Go to bed at the same time (aim for 7-8 hours of sleep)"
            ]
        },
        {
            "category": "Nutrition",
            "habits": [
                "Drink at least 2-3 liters of water",
                "Prepare meals",
                "Make at least 50% of every meal vegetables",
                "Limit processed sugar and sweets"
            ]
        },
        {
            "category": "Personal Development",
            "habits": [
                "Read for 15-30 minutes ",
                "Spend 5 minutes journaling ",
                "Make progress learning a new skill",
                "Reflect on personal goals and progress for 10 minutes "
            ]
        },
        {
            "category": "Productivity & Work",
            "habits": [
                "Use the Pomodoro technique: 25 minutes work, 5 minutes break",
                "Set the three most important tasks every morning",
                "Check emails only 2-3 times",
                "Organize your desk for 5 minutes "
            ]
        },
        {
            "category": "Household & Organization",
            "habits": [
                "Spend 10 minutes daily tidying up a specific area",
                "Schedule fixed days for laundry and folding",
                "Declutter one box of items",
                "Check off weekly cleaning tasks in a calendar"
            ]
        },
        {
            "category": "Finances",
            "habits": [
                "Track all expenses immediately or use an app",
                "Automatically save a fixed amount ",
                "Review income and expenses",
                "Apply the 24-hour rule before major purchases"
            ]
        },
        {
            "category": "Social & Relationships",
            "habits": [
                "Contact at least one person (call, message, or meet)",
                "Practice active listening in conversations",
                "Thank someone or give a compliment",
                "Regularly schedule time for friends or family"
            ]
        },
        {
            "category": "Creativity & Hobbies",
            "habits": [
                "Reserve 15-30 minutes daily for a hobby",
                "Note down new ideas or inspirations ",
                "Try a new creative technique or hobby ",
                "Participate in creative challenges"
            ]
        },
        {
            "category": "Self-care & Well-being",
            "habits": [
                "Practice meditation or breathing exercises for 5-10 minutes",
                "Have one hour of screen-free time each day",
                "Say positive affirmations to yourself in the morning",
                "Take a short break every 60-90 minutes"
            ]
        },
        {
            "category": "Miscellaneous / Custom",
            "habits": [
                "Review progress in all life areas ",
                "Write down three things you are grateful",
                "Do one eco-friendly action ",
                "Practice a foreign language for 5-10 minutes"
            ]
        }
        ]
        return habits
    
    def TemplatesExamples(self):
        #creating a example template for us if he needs an inspiration
        rdHabit = self.ListTemplates()
        newTemplate = {}
        oneDict = random.choice(rdHabit)
        newCategory = oneDict["category"]
        newHabit = random.choice(oneDict["habits"])
        newTemplate[newCategory] = newHabit
        return newTemplate
