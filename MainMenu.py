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
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
     QListWidget, QCheckBox, QMessageBox, QDialog, QHBoxLayout, QTextBrowser, QGridLayout, QStyleFactory, QToolButton, QInputDialog
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QColor, QPalette
import csv
import sqlite3
from pyfiglet import Figlet
from ContactTracingApp import ContactTracingApp

# Define the Main Menu class that inherits from QDialog
class MainMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Space Trace")
        layout = QVBoxLayout()

        # Create buttons and connect them to their respective functions
        self.button_start = QPushButton("Start")
        self.button_start.clicked.connect(self.start_contact_tracing)

        self.button_search = QPushButton("Search")
        self.button_search.clicked.connect(self.search_contacts)

        self.button_exit = QPushButton("Exit")
        self.button_exit.clicked.connect(self.close)

        # Button for the dark mode toggle switch
        self.button_dark_mode = QToolButton()
        self.button_dark_mode.setText("☾ Dark Mode")
        self.button_dark_mode.setCheckable(True)
        self.button_dark_mode.toggled.connect(self.toggle_dark_mode)

        self.button_overview = QPushButton("?")
        self.button_overview.clicked.connect(self.show_overview)

        # Add buttons to the layout
        layout.addWidget(self.button_start)
        layout.addWidget(self.button_dark_mode)
        layout.addWidget(self.button_search)
        layout.addWidget(self.button_overview)
        layout.addWidget(self.button_exit)

        self.setLayout(layout)

        # Initialize the theme setting
        self.is_dark_mode = False
        self.set_light_mode()

        # Create a connection to the SQLite database and initialize the cursor
        try:
            self.conn = sqlite3.connect('contact_tracing.db')
            self.c = self.conn.cursor()
        except sqlite3.Error as e:
            self.show_error_message("Database Error", str(e))
            sys.exit()

    # Function to toggle between light and dark themes
    def toggle_dark_mode(self, is_dark_mode):
        self.is_dark_mode = is_dark_mode

        if self.is_dark_mode:
            self.set_dark_mode()
        else:
            self.set_light_mode()

    # Function to set the light mode theme
    def set_light_mode(self):
        self.is_dark_mode = False
        QApplication.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(Qt.white))
        palette.setColor(QPalette.WindowText, QColor(Qt.black))
        QApplication.setPalette(palette)
        self.button_dark_mode.setText("☾ Dark Mode")
    
    # Function to set the dark mode theme
    def set_dark_mode(self):
        self.is_dark_mode = True
        QApplication.setStyle("Fusion")
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(dark_palette)
        self.button_dark_mode.setText("☀ Light Mode")
    
    # Function to start the contact tracing app
    def start_contact_tracing(self):
        self.close()
        self.contact_tracing_app = ContactTracingApp()
        self.contact_tracing_app.show()
    
    # Function to show the introduction message
    def show_overview(self):
        # Introduction message HTML content
        introduction_text = """
        <p style="text-align: justify;">Welcome to Space Trace!</p>

        <p style="text-align: justify;">This application is designed to help track COVID-19 exposure and symptoms for individuals.
        It allows you to add new entries in accordance to your inputted personal details for procured records and tracking within the database.</p>

        <p style="text-align: justify;">Usage:
        <ol>
        <li>Click on "Start" to enter contact tracing information for an individual.</li>
        <li>Fill in all the required details and answer the questions.</li>
        <li>Click on "Add Entry" to save the information to the database.</li>
        <li>You will be notified if you need to stay home and observe quarantine based on your symptoms or exposure.</li>
        <li>Use the "Search" button to find specific entries in the database.</li>
        <li>Use the "☾" button to switch between light and dark themes.</li>
        <li>Click on the "Exit" to close the application.</li>
        </ol>
        </p>

        <p style="text-align: justify;">Thank you for using Space Trace!</p>
        """
        self.show_message_box("Overview", introduction_text)

    # Function to show a message box
    def show_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    # Function to search contacts and display the results
    def search_contacts(self):
        # Open a new window to display the search results
        self.search_result_window = QDialog(self)
        self.search_result_window.setWindowTitle("Search Results")
        self.search_result_window.setMinimumWidth(400)

        # Create a layout for the search result window
        layout = QVBoxLayout()
        text_browser = QTextBrowser()
        layout.addWidget(text_browser)
        self.search_result_window.setLayout(layout)

        # Get the search term from the user
        search_term, ok = QInputDialog.getText(self, "Search Contacts", "Enter search term:")
        if ok and search_term.strip():
            try:
                # Search for entries in the database that match the search term
                self.c.execute('''SELECT * FROM contacts WHERE
                                  name LIKE ? OR phone LIKE ? OR email LIKE ? OR address LIKE ? OR last_place_visited LIKE ?''',
                               ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%',
                                '%' + search_term + '%', '%' + search_term + '%'))
                results = self.c.fetchall()

                if not results:
                    self.show_message_box("No Results", "No matching entries found.")
                    return

                # Display the search results in the text browser
                output = ""
                for result in results:
                    output += f"Name: {result[1]}\n"
                    output += f"Phone: {result[2]}\n"
                    output += f"Email: {result[3]}\n"
                    output += f"Address: {result[4]}\n"
                    output += f"Last Place Visited: {result[5]}\n"
                    output += f"Vaccinated: {result[6]}\n"
                    output += f"Symptoms: {result[7]}\n"
                    output += f"Exposure: {result[8]}\n"
                    output += f"Contact with Symptoms: {result[9]}\n"
                    output += f"Tested: {result[10]}\n\n"

                text_browser.setText(output)
                self.search_result_window.exec_()

            except sqlite3.Error as e:
                self.show_error_message("Database Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())