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
        writer.writerow(["Username", "Action", "Timestamp", "Money", "Status"])  # Header for login history

class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.attributes('-fullscreen', True)  # Make the window full screen
        self.root.config(bg="#2C3E50")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        frame = tk.Frame(root, bg="#2C3E50")
        frame.pack(expand=True)

        tk.Label(frame, text="Login", font=("Arial", 24), fg="#ECF0F1", bg="#2C3E50").pack(pady=20)

        tk.Label(frame, text="Username:", font=("Arial", 16), fg="#ECF0F1", bg="#2C3E50").pack()
        self.username_entry = tk.Entry(frame, textvariable=self.username_var, font=("Arial", 16))
        self.username_entry.pack(pady=10)

        tk.Label(frame, text="Password:", font=("Arial", 16), fg="#ECF0F1", bg="#2C3E50").pack()
        self.password_entry = tk.Entry(frame, textvariable=self.password_var, font=("Arial", 16), show="*")
        self.password_entry.pack(pady=10)

        tk.Button(frame, text="Login", command=self.login, font=("Arial", 16), bg="#3498DB", fg="white", width=15).pack(pady=10)
        tk.Button(frame, text="Go to Register", command=self.open_register, font=("Arial", 16), bg="#2ECC71", fg="white", width=15).pack()

        tk.Button(self.root, text="Exit", command=self.root.destroy, font=("Arial", 14), bg="#E74C3C", fg="white", width=10).pack(pady=20)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        user_found = False
        user_money = 50  # Default money value if not found in history

        # Open the user data file to check credentials
        with open(data_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == username and row[1] == password:
                    user_found = True
                    break

        if user_found:
            # Get the most recent balance from login history
            with open(history_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                lines = list(reader)
                for row in reversed(lines):  # Go backwards to find the latest login
                    if row[0] == username:
                        user_money = int(row[3])  # Use the money from the most recent entry
                        break

            # Record login action with the current state of money
            timestamp = datetime.now().strftime("%I:%M:%S %p, %B %d, %Y")
            with open(history_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, "logged in", f'"{timestamp}"', user_money, "active"])

            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.root.destroy()
            self.start_game_app(username, user_money)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def open_register(self):
        self.root.destroy()
        root = tk.Tk()
        RegisterForm(root)
        root.mainloop()

    def start_game_app(self, username, user_money):
        root = tk.Tk()
        app = ColorGameApp(root, username, user_money)
        root.mainloop()

class RegisterForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.attributes('-fullscreen', True)  # Make the window full screen
        self.root.config(bg="#2C3E50")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        frame = tk.Frame(root, bg="#2C3E50")
        frame.pack(expand=True)

        tk.Label(frame, text="Register", font=("Arial", 24), fg="#ECF0F1", bg="#2C3E50").pack(pady=20)

        tk.Label(frame, text="Username:", font=("Arial", 16), fg="#ECF0F1", bg="#2C3E50").pack()
        self.username_entry = tk.Entry(frame, textvariable=self.username_var, font=("Arial", 16))
        self.username_entry.pack(pady=10)

        tk.Label(frame, text="Password:", font=("Arial", 16), fg="#ECF0F1", bg="#2C3E50").pack()
        self.password_entry = tk.Entry(frame, textvariable=self.password_var, font=("Arial", 16), show="*")
        self.password_entry.pack(pady=10)

        tk.Button(frame, text="Register", command=self.register, font=("Arial", 16), bg="#2ECC71", fg="white", width=15).pack(pady=10)
        tk.Button(frame, text="Go to Login", command=self.open_login, font=("Arial", 16), bg="#3498DB", fg="white", width=15).pack()

        tk.Button(self.root, text="Exit", command=self.root.destroy, font=("Arial", 14), bg="#E74C3C", fg="white", width=10).pack(pady=20)

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
            writer.writerow([username, "registered", f'"{timestamp}"', 50, "active"])

        messagebox.showinfo("Success", "Registration successful! You can now log in.")

    def open_login(self):
        self.root.destroy()
        root = tk.Tk()
        LoginForm(root)
        root.mainloop()

class ColorGameApp:
    def __init__(self, root, username, user_money):
        self.root = root
        self.username = username
        self.money = user_money  # Initialize with the money from history

        self.root.title("Color Game")
        self.root.attributes('-fullscreen', True)  # Make the window full screen
        self.root.config(bg="#2C3E50")

        self.custom_font = font.Font(family="Arial", size=16)

        self.main_frame = tk.Frame(root, bg="#2C3E50")
        self.main_frame.pack(expand=True)

        self.user_label = tk.Label(self.main_frame, text=f"Player: {self.username}",
                                    font=self.custom_font, fg="#ECF0F1", bg="#2C3E50")
        self.user_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.money_label = tk.Label(self.main_frame, text=f"Your Money: ₱{self.money}",
                                    font=self.custom_font, fg="#ECF0F1", bg="#2C3E50")
        self.money_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.start_button = tk.Button(self.main_frame, text="Start Game", command=self.start_game, 
                                      font=self.custom_font, bg="#3498DB", fg="white", relief="solid", width=20)
        self.start_button.grid(row=2, column=0, pady=10)

        self.play_button = tk.Button(self.main_frame, text="Do you want to play?", command=self.ask_play, 
                                      font=self.custom_font, bg="#3498DB", fg="white", relief="solid", width=20, state="disabled")
        self.play_button.grid(row=2, column=1, pady=10)

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

    def update_money_label(self):
        self.money_label.config(text=f"Your Money: ₱{self.money}")

    def start_game(self):
        self.play_button.config(state="normal")
        self.check_colors_button.config(state="normal")  # Enable the check colors button
        self.bet_text.config(text="Choose the colors you want to bet on.")
        self.start_button.config(state="disabled")

    def ask_play(self):
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
        timestamp = datetime.now().strftime('"%I:%M:%S %p, %B %d, %Y"')  # Ensure timestamp is quoted
        with open(history_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.username, "logged out", timestamp, self.money, "inactive"])
        self.root.quit()
        self.root.destroy()  # Close the window

    def logout(self):
        timestamp = datetime.now().strftime('"%I:%M:%S %p, %B %d, %Y"')  # Ensure timestamp is quoted
        with open(history_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.username, "logged out", timestamp, self.money, "inactive"])
        
        # Close the application
        self.root.quit()
        self.root.destroy()  # Close the window as well

if _name_ == "_main_":
    root = tk.Tk()
    app = LoginForm(root)
    root.mainloop()
