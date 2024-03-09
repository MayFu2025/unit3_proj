# Library

# NOTESNOTES NOTES NOTES! Resources should be a list of dictionaries, [{resource_id : amount}, {resource_id : amount}] NEED TO EDIT ER DIAGRAM BECAUSE I ADDED COLLUMNS


import sqlite3

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from passlib.hash import sha256_crypt
import re


class DatabaseWorker:
    def __init__(self, name: str):
        self.name_db = name

        # Step 1: Create a connection
        self.connection = sqlite3.connect(self.name_db)
        # Step 2: Set cursor/where it inputs into table
        self.cursor = self.connection.cursor()

    def run_query(self, query: str):
        self.cursor.execute(query)  # Run query
        self.connection.commit()  # Save changes

    def search(self, query: str, multiple: bool = False):
        results = self.cursor.execute(query)
        self.run_query(query)
        if multiple:
            return results.fetchall()  # Fetchall returns multiple rows
        else:
            return results.fetchone()  #[0] Fetchone returns single value

    def close(self):
        self.connection.close()


# Functions for hashing/verification
hasher = sha256_crypt.using(rounds=30000)


def make_hash(text: str) -> str:
    return hasher.hash(text)


def check_hash_match(text: str, hashed: str) -> bool:
    return hasher.verify(text, hashed)


# Functions for Login
def check_admin(current_user: list) -> bool:
    """Given the current user, returns True if the user has admin status, returns False if the user doesn't."""
    output = False
    if current_user[2] == 1:
        output = True
    return output


# Function for showing error
def show_popup(screen, messages: list, text: str):
    """Function displays a dialog that prints each message from the list messages."""
    display = "\n".join(messages)
    screen.dialog = MDDialog(
        text=display,
        buttons=[
            MDFlatButton(
                text=text,
                on_press=lambda x: screen.dialog.dismiss()
            )
        ]
    )
    screen.dialog.open()
    return


# Functions for screen change
def try_change(screen, destination: str):
    """Function changes the screen to right destination, based on the name of the button pressed.
    Screen is an object of the MDScreen class"""
    screen.parent.current = f"{destination}"


# Function for calculating sustainability score:
def get_letter_score(score: int)->str:
    """Given the numeric sustainability score, returns the letter grade."""
    if 13 <= score <= 17:
        output = "A"
    elif 18 <= score <= 22:
        output = "B"
    elif 23 <= score <= 27:
        output = "C"
    else:
        output = "D"
    return output
