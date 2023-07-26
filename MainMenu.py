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
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
     QListWidget, QCheckBox, QMessageBox, QDialog, QHBoxLayout, QTextBrowser, QGridLayout, QStyleFactory
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QColor, QPalette
import csv
import sqlite3
from pyfiglet import Figlet

# Define the Main Menu class that inherits from QDialog
class MainMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Space Trace")
        layout = QVBoxLayout()

        # Create buttons and connect them to their respective functions
        self.button_start = QPushButton("Start")
        self.button_start.clicked.connect(self.start_contact_tracing)

        self.button_exit = QPushButton("Exit")
        self.button_exit.clicked.connect(self.close)

        self.button_dark_mode = QPushButton("☾")
        self.button_dark_mode.clicked.connect(self.toggle_dark_mode)

        self.button_overview = QPushButton("?")
        self.button_overview.clicked.connect(self.show_overview)

        # Add buttons to the layout
        layout.addWidget(self.button_start)
        layout.addWidget(self.button_dark_mode)
        layout.addWidget(self.button_overview)
        layout.addWidget(self.button_exit)

        self.setLayout(layout)

        # Initialize the theme setting
        self.is_dark_mode = False

    # Function to toggle between light and dark themes
    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode   # Toggle the theme

        if self.is_dark_mode:
            self.set_dark_mode()
        else:
            self.set_light_mode()

    # Function to set the light mode theme
    def set_light_mode(self):
        self.is_dark_mode = False
        app.setStyle(QStyleFactory.create("Fusion"))
    
    # Function to set the dark mode theme
    def set_dark_mode(self):
        self.is_dark_mode = True
        app.setStyle(QStyleFactory.create("Fusion"))

        # Set a custom dark palette
        dark_palette = self.get_dark_palette()
        app.setPalette(dark_palette)

    # Function to get the custom dark palette
    def get_dark_palette(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.windowText, Qt.white)
        dark_palette.setColor(QPalette.base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.alternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.toolTipBase, Qt.white)
        dark_palette.setColor(QPalette.toolTipText, Qt.white)
        dark_palette.setColor(QPalette.text, Qt.white)
        dark_palette.setColor(QPalette.button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.buttonText, Qt.white)
        dark_palette.setColor(QPalette.brightText, Qt.red)
        dark_palette.setColor(QPalette.link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.highlightedText, Qt.black)
        return dark_palette