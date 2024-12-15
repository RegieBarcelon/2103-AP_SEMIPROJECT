import pytest
import csv
import os
from datetime import datetime
from unittest.mock import Mock

# Constants for test data
TEST_USER_DATA_FILE = "test_user_data.csv"
TEST_HISTORY_FILE = "test_login_history.csv"

# Setup and teardown for test files
@pytest.fixture(scope="module")
def setup_test_files():
    # Create test user data file
    with open(TEST_USER_DATA_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Password"])
        writer.writerow(["testuser", "password123"])

    # Create test login history file
    with open(TEST_HISTORY_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Action", "Timestamp", "Money", "Status"])

    yield  # Test runs here

    # Cleanup test files
    os.remove(TEST_USER_DATA_FILE)
    os.remove(TEST_HISTORY_FILE)

# Mocked LoginForm class for testing
class MockLoginForm:
    def __init__(self, username, password):
        self.username_var = Mock()
        self.username_var.get = Mock(return_value=username)
        self.password_var = Mock()
        self.password_var.get = Mock(return_value=password)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        user_found = False

        with open(TEST_USER_DATA_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == username and row[1] == password:
                    user_found = True
                    break

        return user_found

@pytest.mark.usefixtures("setup_test_files")
def test_valid_login():
    form = MockLoginForm("testuser", "password123")
    result = form.login()
    assert result is True, "The user should be able to log in with valid credentials."

@pytest.mark.usefixtures("setup_test_files")
def test_invalid_login():
    form = MockLoginForm("invaliduser", "wrongpassword")
    result = form.login()
    assert result is False, "The user should not be able to log in with invalid credentials."

@pytest.mark.usefixtures("setup_test_files")
def test_registration():
    new_username = "newuser"
    new_password = "newpassword"

    # Simulate registration process
    with open(TEST_USER_DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_username, new_password])

    # Verify the new user exists in the file
    user_found = False
    with open(TEST_USER_DATA_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == new_username and row[1] == new_password:
                user_found = True
                break

    assert user_found is True, "The new user should be successfully registered."

@pytest.mark.usefixtures("setup_test_files")
def test_login_history():
    username = "testuser"
    timestamp = datetime.now().strftime("%I:%M:%S %p, %B %d, %Y")
    
    # Simulate a login action
    with open(TEST_HISTORY_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, "logged in", f'"{timestamp}"', 50, "active"])
    
    # Verify login history entry
    found_history = False
    with open(TEST_HISTORY_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == username and row[1] == "logged in":
                found_history = True
                break

    assert found_history is True, "Login history should contain a 'logged in' action."

@pytest.mark.usefixtures("setup_test_files")
def test_money_tracking():
    username = "testuser"
    initial_money = 50
    bet_amount = 10
    winnings = 20

    # Simulate a bet
    with open(TEST_HISTORY_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, "played game", f'"{datetime.now().strftime("%I:%M:%S %p, %B %d, %Y")}"', initial_money - bet_amount, "active"])

    # Simulate winnings
    with open(TEST_HISTORY_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, "won game", f'"{datetime.now().strftime("%I:%M:%S %p, %B %d, %Y")}"', initial_money + winnings, "active"])

    # Verify money tracking in history
    money_updated = False
    with open(TEST_HISTORY_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == username and row[3] == str(initial_money + winnings):
                money_updated = True
                break

    assert money_updated is True, "Money should be updated correctly after winning the game."
