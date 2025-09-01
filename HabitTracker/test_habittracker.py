import pytest
from unittest.mock import patch
from user import User
from habit import Habit
from habitTracker import HabitTracker
from datetime import datetime, timedelta
from analytics import Analytics


@pytest.fixture
def four_weeks_daily_dates():
    """
    Returns a list of 28 consecutive datetime objects, representing 
    daily completions for a habit over 4 weeks (ending Aug 31, 2025).
    """
    base = datetime(2025, 8, 31)
    return sorted([base - timedelta(days=i) for i in range(28)])

@pytest.fixture
def mock_get_daily_completion_dates(four_weeks_daily_dates):
    """
    Monkeypatch replacement function for Analytics.db._get_completion_dates,
    always returns a 28-day streak for any habit_id.
    """
    def _mock(habit_id):
        return four_weeks_daily_dates
    return _mock

@pytest.fixture
def four_weeks_weekly_dates():
    """
    Returns a list of 4 consecutive weekly datetime objects,
    representing weekly completions for a habit.
    """
    base = datetime(2025, 8, 31)
    return sorted([base - timedelta(weeks=i) for i in range(4)])

@pytest.fixture
def mock_get_weekly_completion_dates(four_weeks_weekly_dates):
    """
    Monkeypatch replacement for weekly habit completions.
    """
    def _mock(habit_id):
        return four_weeks_weekly_dates
    return _mock

@pytest.fixture
def user():
    """Provide a fresh User instance for tests."""
    return User()

@pytest.fixture
def habit():
    """Provide a fresh Habit instance for tests."""
    return Habit()

@pytest.fixture
def habit_tracker():
    """Provide a fresh HabitTracker instance for tests."""
    return HabitTracker()

def test_user_register_success(user, mocker):
    """Register succeeds when inputs are valid and persistence returns success."""
    # Simulate inputs: name, email, password.
    mocker.patch('builtins.input', side_effect=['TestUser', 'testuser@example.com', 'password123'])
    # Mock DB save success.
    mocker.patch('dataStorage.DataBase.save_data_user', return_value=(True, {'user_id':1, 'name':'TestUser', 'email':'testuser@example.com', 'password':'password123'}))
    # Pretend email validation passes.
    mocker.patch.object(User, 'is_valid_email', return_value=True)
    
    success, user_data = user.register()
    assert success is True
    assert user_data['name'] == 'TestUser'

def test_user_login_success(user, mocker):
    """Login succeeds with valid email and matching credentials in storage."""
    mocker.patch('builtins.input', side_effect=['testuser@example.com', 'password123'])
    mocker.patch.object(User, 'is_valid_email', return_value=True)
    mocker.patch('dataStorage.DataBase.load_data_User', return_value=(True, {'user_id':1, 'name':'TestUser', 'email':'testuser@example.com', 'password':'password123'}))
    
    success, user_data = user.login()
    assert success is True
    assert user_data['email'] == 'testuser@example.com'

def test_habit_choose_from_list_valid(habit, mocker):
    """Choose_from_list returns the correct option when input matches a valid index."""
    mocker.patch('builtins.input', side_effect=['1'])
    choice = habit.choose_from_list("Choose:", ["OptionA", "OptionB"])
    assert choice == "OptionA"

def test_habit_choose_from_list_invalid_then_valid(habit, mocker):
    """Choose_from_list reprompts on invalid index and then returns the valid selection."""
    mocker.patch('builtins.input', side_effect=['3', '2'])
    choice = habit.choose_from_list("Choose:", ["OptionA", "OptionB"])
    assert choice == "OptionB"

def test_habit_tracker_keep_going_or_not(habit_tracker, mocker):
    """keep_going_or_not returns True when the user enters 0."""
    mocker.patch('builtins.input', side_effect=['0'])
    assert habit_tracker.keep_going_or_not() == True

def test_habit_tracker_start_plattform_mark_done_and_return(habit_tracker, mocker):
    """start_plattform handles 'mark done' then exits when user selects 0."""
    mocker.patch('builtins.input', side_effect=['1', '0'])
    mocker.patch('habit.Habit.mark_as_completed', return_value=None)
    
    result = habit_tracker.start_plattform({'user_id': 1})
    assert result == True

def test_analytics_longest_streak_daily(monkeypatch, mock_get_daily_completion_dates):
    """
    Tests: longest streak for a daily habit is 28 when all days are complete.
    """
    analytics = Analytics()
    monkeypatch.setattr(analytics.db, "_get_completion_dates", mock_get_daily_completion_dates)
    result = analytics.longest_streak_for_habit(habit_id=1, periodicity="daily")
    assert result == 28

def test_analytics_longest_streak_weekly(monkeypatch, mock_get_weekly_completion_dates):
    """
    Tests: longest streak for a weekly habit is 4 when four consecutive weeks are complete.
    """
    analytics = Analytics()
    monkeypatch.setattr(analytics.db, "_get_completion_dates", mock_get_weekly_completion_dates)
    result = analytics.longest_streak_for_habit(habit_id=2, periodicity="weekly")
    assert result == 4
