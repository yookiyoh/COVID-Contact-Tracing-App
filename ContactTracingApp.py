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
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
     QListWidget, QCheckBox, QMessageBox, QDialog, QHBoxLayout, QTextBrowser, QGridLayout, QStyleFactory
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QColor, QPalette
import csv
import sqlite3
from pyfiglet import Figlet

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

        # Create checkboxes for additional questions
        self.label_vaccinated = QLabel("Have you been vaccinated for COVID-19? "
                                       "Please select one only.")
        self.checkbox_vaccinated_not_yet = QCheckBox("Not Yet")
        self.checkbox_vaccinated_1st_dose = QCheckBox("1st Dose")
        self.checkbox_vaccinated_2nd_dose = QCheckBox("2nd Dose (Fully Vaccinated)")
        self.checkbox_vaccinated_1st_booster = QCheckBox("1st Booster Shot")
        self.checkbox_vaccinated_2nd_booster = QCheckBox("2nd Booster Shot")

        self.label_symptoms = QLabel("Are you experiencing any symptoms in the past 7 days?")
        self.checkbox_symptoms_fever = QCheckBox("Fever")
        self.checkbox_symptoms_cough = QCheckBox("Cough")
        self.checkbox_symptoms_colds = QCheckBox("Colds")
        self.checkbox_symptoms_body_pains = QCheckBox("Muscle/Body Pains")
        self.checkbox_symptoms_sore_throat = QCheckBox("Sore Throat")
        self.checkbox_symptoms_diarrhea = QCheckBox("Diarrhea")
        self.checkbox_symptoms_headache = QCheckBox("Headache")
        self.checkbox_symptoms_shortness_breath = QCheckBox("Shortness of Breath")
        self.checkbox_symptoms_difficulty_breathing = QCheckBox("Difficulty of Breathing")
        self.checkbox_symptoms_loss_taste = QCheckBox("Loss of Taste")
        self.checkbox_symptoms_loss_smell = QCheckBox("Loss of Smell")
        self.checkbox_symptoms_none = QCheckBox("None of the Above")

        self.label_exposure = QLabel("Have you had exposure to a probable or confirmed case in the last 14 days? "
                                     "Please select one only.")
        self.checkbox_exposure_yes = QCheckBox("Yes")
        self.checkbox_exposure_no = QCheckBox("No")
        self.checkbox_exposure_uncertain = QCheckBox("Uncertain")

        self.label_contact_with_symptoms = QLabel(
            "Have you had contact with somebody with body pains, headache, sore throat, fever, diarrhea, "
            "cough, colds, shortness of breath, loss of taste, or loss of smell in the past 7 days? " 
            "Please select one only.")
        self.checkbox_contact_with_symptoms_yes = QCheckBox("Yes")
        self.checkbox_contact_with_symptoms_no = QCheckBox("No")

        self.label_tested = QLabel("Have you been tested for COVID-19 in the last 14 days? "
                                     "Please select one only")
        self.checkbox_tested_no = QCheckBox("No")
        self.checkbox_tested_positive = QCheckBox("Yes-Positive")
        self.checkbox_tested_negative = QCheckBox("Yes-Negative")
        self.checkbox_tested_pending = QCheckBox("Yes-Pending")

        # Create buttons
        self.button_add = QPushButton("Add Entry")        
        self.button_add.clicked.connect(self.add_entry)

        self.button_search = QPushButton("Search")        
        self.button_search.clicked.connect(self.search_entry)
        
        self.button_clear = QPushButton("Clear")        
        self.button_clear.clicked.connect(self.clear_entry)

        # Set up the layout
        layout = QGridLayout()

        layout.addWidget(self.label_name, 0, 0)
        layout.addWidget(self.entry_name, 0, 1)
        
        layout.addWidget(self.label_phone, 1, 0)
        layout.addWidget(self.entry_phone, 1, 1)

        layout.addWidget(self.label_email, 2, 0)
        layout.addWidget(self.entry_email, 2, 1)

        layout.addWidget(self.label_address, 3, 0)
        layout.addWidget(self.entry_address, 3, 1)

        layout.addWidget(self.label_last_place_visited, 4, 0)
        layout.addWidget(self.entry_last_place_visited, 4, 1)

        layout.addWidget(self.label_vaccinated, 5, 0)
        layout.addWidget(self.checkbox_vaccinated_not_yet, 6, 0)
        layout.addWidget(self.checkbox_vaccinated_1st_dose, 7, 0)
        layout.addWidget(self.checkbox_vaccinated_2nd_dose, 8, 0)
        layout.addWidget(self.checkbox_vaccinated_1st_booster, 9, 0)
        layout.addWidget(self.checkbox_vaccinated_2nd_booster, 10, 0)

        layout.addWidget(self.label_symptoms, 5, 1)
        layout.addWidget(self.checkbox_symptoms_fever, 6, 1)
        layout.addWidget(self.checkbox_symptoms_cough, 7, 1)
        layout.addWidget(self.checkbox_symptoms_colds, 8, 1)
        layout.addWidget(self.checkbox_symptoms_body_pains, 9, 1)
        layout.addWidget(self.checkbox_symptoms_sore_throat, 10, 1)
        layout.addWidget(self.checkbox_symptoms_diarrhea, 11, 1)
        layout.addWidget(self.checkbox_symptoms_headache, 12, 1)
        layout.addWidget(self.checkbox_symptoms_shortness_breath, 13, 1)
        layout.addWidget(self.checkbox_symptoms_difficulty_breathing, 14, 1)
        layout.addWidget(self.checkbox_symptoms_loss_taste, 15, 1)
        layout.addWidget(self.checkbox_symptoms_loss_smell, 16, 1)
        layout.addWidget(self.checkbox_symptoms_none, 17, 1)

        layout.addWidget(self.label_exposure, 18, 0)
        layout.addWidget(self.checkbox_exposure_yes, 19, 0)
        layout.addWidget(self.checkbox_exposure_no, 20, 0)
        layout.addWidget(self.checkbox_exposure_uncertain, 21, 0)

        layout.addWidget(self.label_contact_with_symptoms, 18, 1, 4, 1)
        layout.addWidget(self.checkbox_contact_with_symptoms_yes, 22, 1)
        layout.addWidget(self.checkbox_contact_with_symptoms_no, 23, 1)

        layout.addWidget(self.label_tested, 24, 0)
        layout.addWidget(self.checkbox_tested_no 25, 0)
        layout.addWidget(self.checkbox_tested_positive, 26, 0)
        layout.addWidget(self.checkbox_tested_negative, 27, 0)
        layout.addWidget(self.checkbox_tested_pending, 28, 0)

        layout.addWidget(self.button_add, 29, 0)
        layout.addWidget(self.button_search, 29, 1)
        layout.addWidget(self.button_clear, 29, 2)

        self.entry_search = QLineEdit()
        layout.addWidget(self.entry_search, 30, 0, 1, 3)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set up the animations
        self.fade_in_animation = self.create_fade_animation(central_widget, start_opacity=0.0, end_opacity=1.0)
        self.fade_out_animation = self.create_fade_animation(central_widget, start_opacity=1.0, end_opacity=0.0)

        # Start the fade-in animation
        self.fade_in_animation.start()
        
    def create_fade_animation(self, target, start_opacity, end_opacity):
        animation = QPropertyAnimation(target, b"windowOpacity")
        animation.setDuration(500)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        return animation
    
    def add_entry(self):
        name = self.entry_name.text()
        phone = self.entry_phone.text()
        email = self.entry_email.text()
        address = self.entry_address.text()
        last_place_visited = self.entry_last_place_visited.text()

        # Check if all fields are filled
        if not name or not phone or not email or not address or not last_place_visited:
            self.show_message_box("Incomplete Fields", "Please input all fields.")
            return
        
        # Get the selected checkboxes
        vaccinated = self.get_selected_checkbox_value([
            self.checkbox_vaccinated_not_yet,
            self.checkbox_vaccinated_1st_dose,
            self.checkbox_vaccinated_2nd_dose,
            self.checkbox_vaccinated_1st_booster,
            self.checkbox_vaccinated_2nd_booster
        ])

        symptoms = self.get_selected_checkbox_value([
            self.checkbox_symptoms_fever,
            self.checkbox_symptoms_cough,
            self.checkbox_symptoms_colds,
            self.checkbox_symptoms_body_pains,
            self.checkbox_symptoms_sore_throat,
            self.checkbox_symptoms_diarrhea,
            self.checkbox_symptoms_headache,
            self.checkbox_symptoms_shortness_breath,
            self.checkbox_symptoms_difficulty_breathing,
            self.checkbox_symptoms_loss_taste,
            self.checkbox_symptoms_loss_smell,
            self.checkbox_symptoms_none
        ])

        exposure = self.get_selected_checkbox_value([
            self.checkbox_exposure_yes,
            self.checkbox_exposure_no,
            self.checkbox_exposure_uncertain
        ])

        contact_with_symptoms = self.get_selected_checkbox_value([
            self.checkbox_contact_with_symptoms_yes,
            self.checkbox_contact_with_symptoms_no
        ])

        tested = self.get_selected_checkbox_value([
            self.checkbox_tested_no,
            self.checkbox_tested_positive,
            self.checkbox_tested_negative,
            self.checkbox_tested_pending
        ])

        try:
            # Insert the entry into the database
            self.c.execute('''INSERT INTO contacts (name, phone, email, address, last_place_visited, vaccinated, symptoms, exposure,
                           contact_with_symptoms, tested) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (name, phone, email, address, last_place_visited, vaccinated, symptoms, exposure, contact_with_symptoms, tested))
            self.conn.commit()

            # Clear the input fields
            self.entry_name.clear()
            self.entry_phone.clear()
            self.entry_email.clear()
            self.entry_address.clear()
            self.entry_last_place_visited.clear()

            # Write the entry to the records file
            with open('contact_tracing_records.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, phone, email, address, last_place_visited, vaccinated, symptoms, exposure, contact_with_symptoms, tested])

            if vaccinated == "Not Yet" or symptoms != "None of the above" or exposure != "No" or contact_with_symptoms == "Yes" or tested == "Yes-Positive":
                self.show_message_box("Stay Home", "Please stay home and observe quarantine. Please take care of yourself.")
            
            # Clear other fields
            self.clear_other_fields()

        except sqlite3.Error as e:
            self.show_error_message("Database Error", str(e))

    def search_entry(self):
        search_term = self.entry_search.text()

        try:
            # Search for entries in the database that match the search term
            self.c.execute('''SELECT * FROM contacts WHERE
                              name LIKE ? OR phone LIKE ? OR email LIKE ? OR address LIKE ? OR last_place_visited LIKE ?'''
                           ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%',
                            '%' + search_term + '%', '%' + search_term + '%'))
            results = self.c.fetchall()

            if not results:
                self.show_message_box("No Results", "No matching entries found.")
                return
            
            # Open a new window to display the search results
            dialog = QDialog(self)
            dialog.setWindowTitle("Search Results")
            dialog.setMinimumWidth(400)

            layout = QHBoxLayout()
            text_browser = QTextBrowser()
            layout.addWidget(text_browser)
            dialog.setLayout(layout)

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
                output += f"Tested: {result[10]}\n"

            text_browser.setText(output)
            dialog.exec_()

            # Clear other fields
            self.clear_other_fields()

        except sqlite3.Error as e:
            self.show_error_message("Database Error", str(e))

    def get_selected_checkbox_value(self, checkboxes):
        for checkbox in checkboxes:
            if checkbox.isChecked():
                return checkbox.text()
            
        return ""
    
    def show_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def clear_fields(self):
        self.entry_name.clear()
        self.entry_phone.clear()
        self.entry_email.clear()
        self.entry_address.clear()
        self.entry_last_place_visited.clear()

        self.clear_checkboxes([
            self.checkbox_vaccinated_not_yet,
            self.checkbox_vaccinated_1st_dose,
            self.checkbox_vaccinated_2nd_dose,
            self.checkbox_vaccinated_1st_booster,
            self.checkbox_vaccinated_2nd_booster,
            self.checkbox_symptoms_fever,
            self.checkbox_symptoms_cough,
            self.checkbox_symptoms_colds,
            self.checkbox_symptoms_body_pains,
            self.checkbox_symptoms_sore_throat,
            self.checkbox_symptoms_diarrhea,
            self.checkbox_symptoms_headache,
            self.checkbox_symptoms_shortness_breath,
            self.checkbox_symptoms_difficulty_breathing,
            self.checkbox_symptoms_loss_taste,
            self.checkbox_symptoms_loss_smell,
            self.checkbox_symptoms_none,
            self.checkbox_exposure_yes,
            self.checkbox_exposure_no,
            self.checkbox_exposure_uncertain,
            self.checkbox_contact_with_symptoms_yes,
            self.checkbox_contact_with_symptoms_no,
            self.checkbox_tested_no,
            self.checkbox_tested_positive,
            self.checkbox_tested_negative,
            self.checkbox_tested_pending
        ])

    def clear_other_fields(self):
        self.entry_search.clear()
        self.clear_fields()
    
    def clear_checkboxes(self, checkboxes):
        for checkbox in checkboxes:
            checkbox.setChecked(False)
    
    def closeEvent(self, event):
        # Prompt a confirmation dialog when closing the window
        reply = QMessageBox.question(self, 'Confirmation', "Are you sure you want to close this application?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Start the fade-out animation
            self.fade_out_animation.start()

            # Close the database connection when the app is closed
            try:
                self.conn.close()
            except sqlite3.Error as e:
                self.show_error_message("Database Error", str(e))
            
            # Wait for the fade-out animation to finish before exiting the application
            self.fade_out_animation.finished.connect(lambda: self.close_message_box())
        
        else:
            event.ignore()
    
    def close_message_box(self):
        # Show a message box after closing the window
        self.show_message_box("Thank you", "Thank you for using the COVID-19 Tracer App!")
        self.close()

    @staticmethod
    def show_error_message(title, message):
        print("\n" + "#" * 50)
        print(title.center(50))
        print("#" * 50)
        print(f"\n{message}\n")

        # Use pyfiglet for error message styling
        f = Figlet(font='slant')
        error_message = f.renderText("Error!")
        print(error_message)