# Ralph Lorenz I. Codilan
# BSCpE 1-5
# Object-Oriented Programming | Final Project

# Pseudocode

'''
# Import required libraries

# Create the MainMenu class
    # Initialize the main menu window
    # Set up the theme setting
    # Define methods to toggle themes, show introduction, and display message boxes
    # Handle the start contact tracing button click
        # Close the main menu window
        # Open the ContactTracingApp window

# Create the ContactTracingApp class
    # Initialize the contact tracing app window
    # Create a connection to the SQLite database and create a table to store data
    # Set up UI elements: labels, entry fields, checkboxes, and buttons
    # Implement methods to add entry, search entry, clear fields, clear checkboxes
    # Handle the closeEvent method to prompt a confirmation dialog
    # Define a method to show error messages

# Main function
    # Initialize the PyQt5 application
    # Create and show the MainMenu window
    # Run the application
'''

# Import necessary libraries
import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
     QListWidget, QCheckBox, QMessageBox, QDialog, QHBoxLayout, QTextBrowser, QGridLayout, QStyleFactory
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QColor, QPalette
import csv
import sqlite3
from pyfiglet import Figlet
import datetime

# Define the Contact Tracing App class that inherits the QMainWindow
class ContactTracingApp (QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COVID Contact Tracing App")

        # Create a connection to the SQLite database
        try:
            self.conn = sqlite3.connect('contact_tracing.db')
            self.c = self.conn.cursor()
        except sqlite3.Error as e:
            self.show_error_message("Database Error", str(e))
            sys.exit()
        
        # Create a table to store the contact tracing information
        try:
            self.c.execute('''CREATE TABLE IF NOT EXISTS contacts (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                phone TEXT,
                                email TEXT,
                                address TEXT,
                                last_place_visited TEXT,
                                vaccinated TEXT,
                                symptoms TEXT,
                                exposure TEXT,
                                contact_with_symptoms TEXT,
                                tested TEXT,
                                current_datetime TEXT,
                           )''')
            self.conn.commit()
        except sqlite3.Error as e:
            self.show_error_message("Database Error", str(e))
            sys.exit()
        
        # Create labels and entry fields for input
        self.label_name = QLabel("Name:")
        self.entry_name = QLineEdit()

        self.label_phone = QLabel("Phone:")
        self.entry_phone = QLineEdit()

        self.label_email = QLabel("Email:")
        self.entry_email = QLineEdit()

        self.label_address = QLabel("Address:")
        self.entry_address = QLineEdit()

        self.label_last_place_visited = QLabel("Last Place Visited:")
        self.entry_last_place_visited = QLineEdit()

        