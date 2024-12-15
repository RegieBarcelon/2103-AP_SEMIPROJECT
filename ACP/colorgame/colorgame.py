import random
import tkinter as tk
from tkinter import messagebox, font
import csv
import os
from datetime import datetime

# List of colors
colors = ['Red', 'Blue', 'Green', 'Yellow', 'White', 'Pink']

# Data storage for users and login history
data_file = "user_data.csv"
history_file = "login_history.csv"

# Ensure data file exists
if not os.path.exists(data_file):
    with open(data_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Password"])  # Header for user data

if not os.path.exists(history_file):
    with open(history_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Action", "Timestamp", "Money", "Debt", "Status"])  # Header for login history

class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x200")
        self.root.config(bg="#2C3E50")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(root, text="Login", font=("Arial", 16), fg="#ECF0F1", bg="#2C3E50").pack(pady=10)

        tk.Label(root, text="Username:", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack()
        self.username_entry = tk.Entry(root, textvariable=self.username_var, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Password:", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack()
        self.password_entry = tk.Entry(root, textvariable=self.password_var, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Login", command=self.login, font=("Arial", 12), bg="#3498DB", fg="white").pack(pady=10)
        tk.Button(root, text="Go to Register", command=self.open_register, font=("Arial", 12), bg="#2ECC71", fg="white").pack()

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        user_found = False
        user_money = 50  # Default money in case no data is found
        user_debt = 0     # Default debt in case no data is found

        # Open the user data file to check credentials
        with open(data_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == username and row[1] == password:
                    user_found = True
                    break

        if user_found:
            # Retrieve last login history to set user's money and debt
            with open(history_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                rows = list(reader)
                last_row = rows[-1] if len(rows) > 1 else None  # Get the last row if exists

                # Ensure the row contains enough data
                if last_row and len(last_row) >= 5 and last_row[0] == username:
                    user_money = int(last_row[3])  # Set money to the last saved value
                    user_debt = int(last_row[4])   # Set debt to the last saved value

            # Record login action with the current state of money and debt
            timestamp = datetime.now().strftime("%I:%M:%S %p, %B %d, %Y")
            with open(history_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, "logged in", timestamp, user_money, user_debt, "active"])

            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.root.destroy()
            self.start_game_app(username, user_money, user_debt)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def open_register(self):
        self.root.destroy()
        root = tk.Tk()
        RegisterForm(root)
        root.mainloop()

    def start_game_app(self, username, user_money, user_debt):
        root = tk.Tk()
        app = ColorGameApp(root, username, user_money, user_debt)
        root.mainloop()

class RegisterForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("400x200")
        self.root.config(bg="#2C3E50")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(root, text="Register", font=("Arial", 16), fg="#ECF0F1", bg="#2C3E50").pack(pady=10)

        tk.Label(root, text="Username:", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack()
        self.username_entry = tk.Entry(root, textvariable=self.username_var, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Password:", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50").pack()
        self.password_entry = tk.Entry(root, textvariable=self.password_var, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Register", command=self.register, font=("Arial", 12), bg="#2ECC71", fg="white").pack(pady=10)
        tk.Button(root, text="Go to Login", command=self.open_login, font=("Arial", 12), bg="#3498DB", fg="white").pack()

    def register(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        with open(data_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row[0] == username:
                    messagebox.showerror("Error", "Username already exists.")
                    return

        with open(data_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password])

        # Record the registration action with a timestamp
        timestamp = datetime.now().strftime("%I:%M:%S %p, %B %d, %Y")
        with open(history_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, "registered", timestamp, 50, 0, "active"])

        messagebox.showinfo("Success", "Registration successful! You can now log in.")

    def open_login(self):
        self.root.destroy()
        root = tk.Tk()
        LoginForm(root)
        root.mainloop()

class ColorGameApp:
    def __init__(self, root, username, user_money, user_debt):
        self.root = root
        self.username = username
        self.money = user_money  # Initialize with the money from history
        self.debt = user_debt    # Initialize with the debt from history
        self.max_debt = 200  # Max debt cap

        self.custom_font = font.Font(family="Arial", size=12)

        self.main_frame = tk.Frame(root, bg="#2C3E50")
        self.main_frame.pack(pady=20)

        self.user_label = tk.Label(self.main_frame, text=f"Player: {self.username}",
                                    font=self.custom_font, fg="#ECF0F1", bg="#2C3E50")
        self.user_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.money_label = tk.Label(self.main_frame, text=f"Your Money: ₱{self.money} | Your Debt: ₱{self.debt}",
                                    font=self.custom_font, fg="#ECF0F1", bg="#2C3E50")
        self.money_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.start_button = tk.Button(self.main_frame, text="Start Game", command=self.start_game, 
                                      font=self.custom_font, bg="#3498DB", fg="white", relief="solid", width=20)
        self.start_button.grid(row=2, column=0, pady=10)

        self.play_button = tk.Button(self.main_frame, text="Do you want to play?", command=self.ask_play, 
                                      font=self.custom_font, bg="#3498DB", fg="white", relief="solid", width=20, state="disabled")
        self.play_button.grid(row=2, column=1, pady=10)

        self.borrow_button = tk.Button(self.main_frame, text="Borrow ₱50", command=self.borrow_money,
                                       font=self.custom_font, bg="#E74C3C", fg="white", relief="solid", width=20)
        self.borrow_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.bet_text = tk.Label(self.main_frame, text="", font=self.custom_font, fg="#ECF0F1", bg="#2C3E50")
        self.bet_text.grid(row=4, column=0, columnspan=2)

        self.bets = {}
        self.bet_frame = None

        self.check_colors_button = tk.Button(self.main_frame, text="Check Colors", command=self.check_colors,
                                             font=self.custom_font, bg="#F39C12", fg="white", relief="solid", width=20, state="disabled")
        self.check_colors_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.logout_button = tk.Button(self.main_frame, text="Logout", command=self.logout,
                                       font=self.custom_font, bg="#E74C3C", fg="white", relief="solid", width=20)
        self.logout_button.grid(row=6, column=0, columnspan=2, pady=10)

        if self.money <= 0:
            self.play_button.config(state="disabled")
            self.borrow_button.config(state="normal")  # Enable the borrow button if balance is 0

    def update_money_label(self):
        self.money_label.config(text=f"Your Money: ₱{self.money} | Your Debt: ₱{self.debt}")

    def start_game(self):
        self.play_button.config(state="normal")
        self.borrow_button.config(state="disabled")  # Disable borrow button when game starts
        self.check_colors_button.config(state="normal")  # Enable the check colors button
        self.bet_text.config(text="Choose the colors you want to bet on.")
        self.start_button.config(state="disabled")

    def ask_play(self):
        if self.money <= 0 and self.debt >= self.max_debt:
            messagebox.showerror("Error", "You cannot play without money and you have reached the maximum debt limit.")
            return

        play = messagebox.askquestion("Play?", "Do you want to play?")
        if play == "yes":
            self.draw_colors()
        else:
            self.end_game()

    def draw_colors(self):
        self.correct_colors = random.sample(colors, 3)
        self.bets = {}

        self.bet_text.config(text="Enter your bets for the colors.")

        if self.bet_frame:
            self.bet_frame.destroy()
        self.bet_frame = tk.Frame(self.main_frame, bg="#2C3E50")
        self.bet_frame.grid(row=4, column=0, columnspan=2, pady=20)

        for i, color in enumerate(colors):
            bet_label = tk.Label(self.bet_frame, text=f"{color}: ₱", font=self.custom_font, fg="#ECF0F1", bg="#2C3E50")
            bet_label.grid(row=i, column=0, padx=10, pady=5)
            bet_entry = tk.Entry(self.bet_frame, font=self.custom_font, width=10)
            bet_entry.grid(row=i, column=1, padx=10, pady=5)
            self.bets[color] = bet_entry

    def check_colors(self):
        winnings = 0
        results_message = "Winning Colors: " + ", ".join(self.correct_colors) + "\n\n"

        for color, bet_entry in self.bets.items():
            try:
                bet = int(bet_entry.get())
            except ValueError:
                continue

            if color in self.correct_colors:
                if self.correct_colors.count(color) == 2:
                    winnings += bet * 2
                    results_message += f"You won on {color}! Prize: ₱{bet * 2}\n"
                else:
                    winnings += bet
                    results_message += f"You won on {color}! Prize: ₱{bet}\n"
            else:
                self.money -= bet
                results_message += f"You lost on {color}. Lost: ₱{bet}\n"

        self.money += winnings
        self.update_money_label()

        self.bet_frame.destroy()
        self.bet_text.config(text="")
        messagebox.showinfo("Results", results_message)

        self.play_button.config(state="disabled")
        self.check_colors_button.config(state="disabled")

        if self.money > 0:
            play_again = messagebox.askquestion("Play Again?", "Do you want to play again?")
            if play_again == "yes":
                self.start_game()
            else:
                self.end_game()
        else:
            messagebox.showinfo("Game Over", "You ran out of money!")
            self.end_game()

    def end_game(self):
        timestamp = datetime.now().strftime("%I:%M:%S %p, %B %d, %Y")
        with open(history_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.username, "logged out", timestamp, self.money, self.debt, "inactive"])
        self.root.quit()

    def borrow_money(self):
        if self.debt < self.max_debt:
            self.debt += 50
            self.money += 50
            self.update_money_label()
            messagebox.showinfo("Success", "You borrowed ₱50.")
        else:
            messagebox.showerror("Error", "You cannot borrow more money; maximum debt limit reached.")

    def logout(self):
        if self.debt == self.max_debt:
            # If debt is maximum, prompt the user to pay the debt
            pay_bill = messagebox.askquestion("Pay Bill", "You have an outstanding debt of \u20b1200. Do you want to pay your debt?")
            if pay_bill == "yes":
                if self.money >= self.debt:
                    self.money -= self.debt
                    self.debt = 0
                    self.update_money_label()
                    timestamp = datetime.now().strftime("%I:%M:%S %p, %B %d, %Y")
                    with open(history_file, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([self.username, "logged out (debt paid)", timestamp, self.money, self.debt, "inactive"])
                    messagebox.showinfo("Success", "You have paid your debt. Thank you!")
                    self.root.quit()
                else:
                    messagebox.showerror("Error", "You do not have enough money to pay your debt.")
                    return
            else:
                # If they refuse to pay and debt is at maximum, block logout
                messagebox.showerror("Error", "You cannot log out without paying your debt.")
                return
        else:
            # Proceed with regular logout if debt is not maximum
            timestamp = datetime.now().strftime("%I:%M:%S %p, %B %d, %Y")
            with open(history_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.username, "logged out", timestamp, self.money, self.debt, "inactive"])
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginForm(root)
    root.mainloop()
