import pytest
from unittest.mock import patch
from user import User
from habit import Habit
from habitTracker import HabitTracker


@pytest.fixture
def user():
    return User()

@pytest.fixture
def habit():
    return Habit()

@pytest.fixture
def habit_tracker():
    return HabitTracker()

def test_user_register_success(user, mocker):
    # Eingaben simulieren: Name, Email, Passwort
    mocker.patch('builtins.input', side_effect=['TestUser', 'testuser@example.com', 'password123'])
    # Datenbank-Mock: speichert User erfolgreich
    mocker.patch('dataStorage.DataBase.save_data_user', return_value=(True, {'user_id':1, 'name':'TestUser', 'email':'testuser@example.com', 'password':'password123'}))
    # Email validieren - true zurückgeben
    mocker.patch.object(User, 'is_valid_email', return_value=True)
    
    success, user_data = user.register()
    assert success is True
    assert user_data['name'] == 'TestUser'

def test_user_login_success(user, mocker):
    mocker.patch('builtins.input', side_effect=['testuser@example.com', 'password123'])
    mocker.patch.object(User, 'is_valid_email', return_value=True)
    mocker.patch('dataStorage.DataBase.load_data_User', return_value=(True, {'user_id':1, 'name':'TestUser', 'email':'testuser@example.com', 'password':'password123'}))
    
    success, user_data = user.login()
    assert success is True
    assert user_data['email'] == 'testuser@example.com'

def test_habit_choose_from_list_valid(habit, mocker):
    mocker.patch('builtins.input', side_effect=['1'])
    choice = habit.choose_from_list("Choose:", ["OptionA", "OptionB"])
    assert choice == "OptionA"

def test_habit_choose_from_list_invalid_then_valid(habit, mocker):
    mocker.patch('builtins.input', side_effect=['3', '2'])
    choice = habit.choose_from_list("Choose:", ["OptionA", "OptionB"])
    assert choice == "OptionB"

def test_habit_tracker_keep_going_or_not(habit_tracker, mocker):
    mocker.patch('builtins.input', side_effect=['0'])
    assert habit_tracker.keep_going_or_not() == True

def test_habit_tracker_start_plattform_mark_done_and_return(habit_tracker, mocker):
    mocker.patch('builtins.input', side_effect=['1', '0'])
    mocker.patch('habit.Habit.mark_as_completed', return_value=None)
    
    result = habit_tracker.start_plattform({'user_id': 1})
    assert result == True
