# Habit Tracker

Habit Tracker is a Python command-line application designed to help users track and manage habits. It supports user registration, login, and habit creation either from custom input or from pre-defined templates, with all data stored locally in an SQLite database.

***

## Features

- **User Management**
  - Register new users with a unique email address.
  - Login with email and password.
  - View and update user profile information (name, email, password) (partial support).
  - User deletion (not yet implemented).

- **Habit Management**
  - Create custom habits with category, description, periodicity (daily or weekly), and select specific weekdays if weekly.
  - Add habits from a selection of categorized templates.
  - Save habits to SQLite database (has some database query issues currently).
  - Placeholders exist for editing, deleting, and marking habits as completed.

- **Habit Templates**
  - Provides multiple categories such as Health & Fitness, Nutrition, Productivity, and more.
  - Random habit suggestions are available for inspiration.

- **History Tracking**
  - A scaffolded module exists to track habit completion history with options to filter by date and habit, though not implemented yet.

- **Command-Line Interface**
  - Step-by-step menus guide users through registration, login, and habit management processes.

***

## Project Structure

```
habit-tracker/
│── main.py            # Entry point handling login and main menu flow
│── user.py            # User registration, login, and profile update logic
│── habit.py           # Habit creation and management
│── habitTemplate.py   # Predefined habit categories and example habits
│── habitTracker.py    # Main habit tracking interface logic
│── history.py         # Habit completion history management (to be implemented)
│── dataStorage.py     # SQLite database interface for users and habits
│── test.py            # Test script to quickly launch habit tracker interface
```

***

## Setup Instructions

### Prerequisites

- Python 3.x installed on your system.

### Database Initialization

Before starting, create the SQLite database and required tables. You can initialize this via a Python shell:

```python
import sqlite3
con = sqlite3.connect("Habit_Tracker.db")
con.execute("""
CREATE TABLE IF NOT EXISTS USER (
  UserID INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  email TEXT UNIQUE,
  password TEXT
)
""")
con.execute("""
CREATE TABLE IF NOT EXISTS habits (
  HabitID INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  name TEXT,
  category TEXT,
  description TEXT,
  periodicity TEXT,
  status INTEGER,
  startDate TEXT
)
""")
con.commit()
con.close()
```

### Running the Application

Run the main program with:

```bash
python main.py
```

Follow on-screen prompts to register, login, and start managing your habits.

***

## Usage Example (CLI)

```
HABIT TRACKER
Press [r] for registration || press [l] for login
> r

Registration:
Name: Alice
Email: alice@example.com
Password: ********

Registration was successful!
Welcome Alice!

Press [1] for starting the Habittracker
Press [2] for updating your account information
Press [3] for deleting a user
Press [4] for showing user information
Press  for logging out
> 1

Welcome
Start with a new Habit!
If you want to create your own Habit please press [1]
If you want to take a Template please press [2]
Press [3] for back to user menu
> 1

== New Habit ==
Choose a Category
[1]: Health & Fitness
[2]: Nutrition
...

> 2
What should your habit be?
> Eat Salad for Lunch

Description:
> Make sure at least half the plate is veggies.

In which period do you want to...
[1]: daily
[2]: weekly
> 1

Habit was created:
{'category': 'Nutrition', 'habit': 'Eat Salad for Lunch', 'description': 'Make sure at least half the plate is veggies.', 'intervall': 'daily', 'status': 0, 'startday': '2025-08-17'}
```

*Note: Some database operations and habit saving features are still under development and may not fully work.*

***

## Known Issues & Limitations

- Habit-saving database query has errors and is currently broken; requires fixing.
- Key methods like editing, deleting habits, marking completion, and user deletion are placeholders.
- Passwords are stored as plain text; no hashing is implemented yet (security risk).
- Input validation and error handling need enhancement, especially for registration and habit creation.
- Notification system and reminders are not implemented.
- History tracking is scaffolded but not functional.
- The app runs in the command line only; no graphical user interface available.

***

## Future Development Roadmap

- Fix and optimize database queries for habit saving and updating.
- Implement habit editing, deletion, and completion features.
- Complete user deletion functionality.
- Develop notification and reminder systems.
- Add export/import data support (CSV or JSON).
- Build comprehensive history and progress reports.
- Improve input validation and error messages.

***

