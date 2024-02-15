# Library

import sqlite3

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from passlib.hash import sha256_crypt
import re

class DatabaseWorker:
    def __init__(self, name:str):
        self.name_db = name

        # Step 1: Create a connection
        self.connection = sqlite3.connect(self.name_db)
        # Step 2: Set cursor/where it inputs into table
        self.cursor = self.connection.cursor()

    def run_query(self, query:str):
        self.cursor.execute(query)  # Run query
        self.connection.commit()  # Save changes

    def insert(self, query:str):
        self.run_query(query)

    def search(self, query:str, multiple:bool = False):
        results = self.cursor.execute(query)
        self.run_query(query)
        if multiple:
            return results.fetchall()  # Fetchall returns multiple rows
        else:
            return results.fetchone()  # Fetchone returns single value

    def close(self):
        self.connection.close()


# Functions for hashing/verification
hasher = sha256_crypt.using(rounds=30000)
def make_hash(text: str) -> str:
    return hasher.hash(text)

def check_hash_match(text: str, hashed: str) -> bool:
    return hasher.verify(text, hashed)


# Functions for Login
def check_email(email: str) -> bool:
    """Check if user input is in email format. Return True if it is, False if it is not."""
    output = False
    if re.match(r"[^@]+@[^@]+\.[^@]", email):
        output = True
    return output

def check_username(username: str) -> bool:
    """Check if username is available for use. Return True if it is, False if it is not."""
    output = False
    db = DatabaseWorker("database.db")
    result = db.search(query=f"SELECT username FROM users WHERE username = '{username}'")
    print(result)
    if result is None:
        output = True
    return output


# Function for showing error
def show_popup(screen, messages: list):
    """Function displays a dialog that prints each error from the list errors."""
    display = "\n".join(messages)
    screen.dialog = MDDialog(
        text=display,
        buttons=[
            MDFlatButton(
                text="OK",
                on_press=lambda x: screen.dialog.dismiss()
            )
        ]
    )
    screen.dialog.open()
    return


#Functions for screen change
def try_change(screen, destination:str):
    """Function changes the screen to right destination, based on the name of the button pressed.
    Screen is an object of the MDScreen class"""
    screen.parent.current = f"{destination}"