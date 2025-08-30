# Habit Tracker Application (CLI)

## Highlights
- Modular architecture: separation of concerns across user management, habit logic, analytics, and persistence.
- Pure CLI UX with numbered menus and input validation.
- SQLite persistence; pandas-powered formatting for selected outputs.
- Daily/weekly periodicity, optional weekday for weekly habits, and completion logging.
- Analytics for listing, filtering by periodicity, and longest streak calculations.

## Architecture Overview
- main.py: Program entry; authentication loop and routing.
- user.py: User registration/login, profile, preferences update, and deletion.
- habit.py: Habit CRUD, completion marking, and template-assisted creation.
- habitTemplate.py: Categories, periodicities, weekdays, and sample templates.
- habitTracker.py: Main habit platform CLI controller delegating to Habit/Analytics.
- analytics.py: Habit insights and streak computation.
- dataStorage.py: SQLite persistence layer (users, habits, habit_completion).

## CLI Menus
### Authentication
```
------- HABIT TRACKER -------
1) Registration
2) Login
> 
```


### User Settings
```
Welcome!

1) Start Habit Tracker
2) Update Account
3) Show Profile
4) Delete Account
0) Logout
```


### Habit Tracker
```
Welcome
Start with a new Habit! Press a Number!

1) Mark your Habit done
2) Create your own Habit
3) Take a Template Habit
4) Show your Habit
5) Edit a Habit
6) Delete a Habit
7) Analytics
0) Back to user menu
```


### Analytics
```
Start with a new Habit! Press a Number!

1) Showing all habits
2) Show habits by periodicity
3) Show longest streak for all habits
4) Show longest streak for a specific habit
0) Return to main menu
```


## Data Model (SQLite)
- USER(user_id, name, email, password)
- habits(habit_id, user_id, category, habit, description, periodicity, status, startDate, weekday)
- habit_completion(habit_id, completion_date, status)

Notes:
- completion_date format: YYYY-MM-DD.
- status: 1 = done, 0 = not done.

## Control Flow
1) Authentication: Registration or Login via main.py.
2) On success, User Settings menu appears.
3) Start Habit Tracker to manage/track habits.
4) Use Analytics to view lists and streaks.
5) Return to User Settings to view/update/delete account or logout.

## Responsibilities and Best Practices
### main.py
- Orchestrates top-level loop and routing.
- Wrap int conversions with try/except to catch ValueError.
- Clear screen between menus for readability.

### user.py (User)
- Validate email with regex before DB calls.
- Methods:
  - register(): gather inputs, validate, save via DataBase.
  - login(): authenticate via DataBase.load_data_User.
  - user_setting(): route to tracker or account ops; returns boolean to control loop.
  - update_preferences(): update name/email/password; persist via DataBase.update_data_user.
  - delete_user(): cascade delete user and dependent habits via DataBase helpers.
- UX: confirm destructive actions and re-prompt on invalid input.

### habit.py (Habit)
- add(): capture category → name → description → periodicity → weekday (if weekly) → save.
- add_habit_template(): randomized template; accept(y)/skip(n)/exit(x) → save if yes.
- mark_as_completed(): iterate habits not marked today; log completion status to habit_completion.
- show_habit(): display all habits for user.
- edit_habit(): select habit by id; update chosen field; handle weekly weekday.
- delete(): select habit by id; confirm; delete.
- Robust input validation with choose_from_list() and try/except.

### habitTemplate.py (Templates)
- list_catergory(): canonical list of categories.
- list_periodicity(): ["daily","weekly"].
- get_weekdays(): from calendar.day_name.
- template_examples(): random example; used by add_habit_template().

### habitTracker.py (Platform Controller)
- start_plattform(): loop for habit ops; delegates to Habit/Analytics; returns True to go back.
- keep_going_or_not(): waits for 0 to return.

### analytics.py (Insights)
- get_all_habits(): list habit names for user.
- get_habits_by_periodicity(): filter by "daily"/"weekly".
- longest_streak_for_habit(): max consecutive periods using date diffs (1 day for daily, 7 days for weekly).
- longest_streak_all_habits(): dict of habit → longest streak.

### dataStorage.py (Persistence)
- Single sqlite3 connection; commit after write operations.
- Parameterized SQL queries to prevent injection.
- Strip email/password when logging in.
- Handle IntegrityError (e.g., duplicate email) and OperationalError.
- Helpers: check_any_habit_in_db(), check_if_habit_already_done(), _get_completion_dates().[3]

## Input Validation Patterns
- Wrap int(input()) in try/except ValueError and re-prompt.
- Accept limited sets for yes/no (y, n, x) and re-prompt otherwise.
- Enforce weekday selection for weekly periodicity.

## Error Handling & UX
- Short, clear error messages (e.g., "Wrong input!", "Only numbers allowed!").
- Small sleep delays to improve readability.
- Clear screen between menus.

## Security & Data Considerations
- Current passwords stored in plaintext; for production, hash with bcrypt/argon2/scrypt.
- Enforce unique email with DB constraint and proper handling.
- Keep parameterized queries for safety.

## Portability Notes
- Uses cls for clearing screen (Windows); use clear on Unix-like systems.
- Externalize DB path via config/env instead of hardcoding.
- Date handling: use datetime.now().strftime("%Y-%m-%d").

## How to Run
1) Install Python 3.x and pandas.[3]
2) Ensure SQLite DB exists with tables USER, habits, habit_completion; or run migrations/DDL first.
3) Launch:
   ```
   python main.py
   ```


## Example Session
```
------- HABIT TRACKER -------
1) Registration
2) Login
> 1

Registration:
Name: John
Email: john@example.com
Password: secret123
Registration was successful!

Welcome!
1) Start Habit Tracker
2) Update Account
3) Show Profile
4) Delete Account
0) Logout
> 1

Welcome
Start with a new Habit! Press a Number!
1) Mark your Habit done
2) Create your own Habit
3) Take a Template Habit
4) Show your Habit
5) Edit a Habit
6) Delete a Habit
7) Analytics
0) Back to user menu
> 2

== New Habit ==
Choose a Category:
[1]: Health & Fitness
[2]: Nutrition
...
> 1
What should your habit be?:
> Morning walk
Description:
> Walk 30 minutes daily
In which period do you want to
[1]: daily
[2]: weekly
> 1
Habit is saving...
```


## Testing Strategy
- Pytest with mocks for input() and database to isolate logic.
- Tests cover:
  - Registration/login success paths and email validation.
  - Menu selection with invalid-then-valid flows.
  - choose_from_list() handling.
  - start_plattform() flow returning to menu.
- CI suggestion: lint (ruff/flake8), format (black), run pytest.



## Data Model (Best Practices)

- Schema design
  - Three core tables: USER, habits, habit_completion; single responsibility per table, no redundant storage.
  - Prefer surrogate keys (INTEGER PRIMARY KEY AUTOINCREMENT); use clear, consistent column names.
  - Store dates as ISO 8601 TEXT (YYYY‑MM‑DD) for startDate and completion_date to enable lexicographic sorting and easy parsing.

- Integrity and constraints
  - Use NOT NULL, UNIQUE, and CHECK for domain constraints; restrict periodicity to {'daily','weekly'}.
  - Enable and enforce FOREIGN KEYs in SQLite and use ON DELETE CASCADE to remove dependent habits/completions when a user is deleted.
  - Optionally prevent duplicate “done” entries per (habit_id, completion_date) with a UNIQUE index or enforce via application logic.

- Indexing and performance
  - Add indexes for common filters: USER(email), habits(user_id), habit_completion(habit_id, completion_date).
  - Inspect schema and columns via .schema/PRAGMA table_info to validate deployed structures.

- Recommended DDL (reference)
  ```
  CREATE TABLE IF NOT EXISTS USER (
    user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT    NOT NULL,
    email     TEXT    NOT NULL UNIQUE,
    password  TEXT    NOT NULL
  );

  CREATE TABLE IF NOT EXISTS habits (
    habit_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    category    TEXT    NOT NULL,
    habit       TEXT    NOT NULL,
    description TEXT    NOT NULL DEFAULT '',
    periodicity TEXT    NOT NULL,
    status      INTEGER NOT NULL DEFAULT 0,
    startDate   TEXT    NOT NULL,  -- YYYY-MM-DD
    weekday     TEXT    NOT NULL DEFAULT '',
    FOREIGN KEY (user_id) REFERENCES USER(user_id) 
  );

  CREATE TABLE IF NOT EXISTS habit_completion (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id        INTEGER NOT NULL,
    completion_date TEXT    NOT NULL,  -- YYYY-MM-DD
    status          INTEGER NOT NULL CHECK (status IN (0,1)),  -- 1 = done, 0 = not done
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) 
  );

  ```


## Known Limitations
- Plaintext passwords in DB.
- Hardcoded DB path.
- Screen clear uses Windows-specific command by default.
- Some menu typos/mixed language strings.
