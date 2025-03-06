from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QFileDialog, QMessageBox
from pathlib import Path
import sys
import pandas as pd
from ai_client import get_ai_response
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Grader")
        
        # Center widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout for widget
        layout = QtWidgets.QGridLayout()
        central_widget.setLayout(layout)

        # Create and align the buttons
        layout.setContentsMargins(0, 50, 0, 0)

        self.upload_button = QPushButton("Upload")
        self.upload_button.setFixedWidth(300)
        self.upload_button.setFixedHeight(50)
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button, 0, 0, 1, 1, QtCore.Qt.AlignTop)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedWidth(300)
        self.submit_button.setFixedHeight(50)
        self.submit_button.clicked.connect(self.process_file)
        layout.addWidget(self.submit_button, 0, 2, 1, 1, QtCore.Qt.AlignTop)

        self.ask_ai_button = QPushButton("Ask AI")
        self.ask_ai_button.setFixedWidth(300)
        self.ask_ai_button.setFixedHeight(50)
        self.ask_ai_button.clicked.connect(self.onClickAI)
        layout.addWidget(self.ask_ai_button, 0, 3, 1, 1, QtCore.Qt.AlignTop)

        self.resize(1000, 800)

        # Store the file path
        self.file_path = None

    def upload_file(self):
        # Open a file dialog to select a CSV file
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")

        if file_path:
            self.file_path = file_path
            QMessageBox.information(self, "File Uploaded", f"File uploaded successfully: {file_path}")

    def process_file(self):
        if not self.file_path:
            QMessageBox.warning(self, "No File", "Please upload a CSV file first.")
            return

        try:
            # Read the CSV file
            df = pd.read_csv(self.file_path)

            # Process the data
            df['is_correct'] = df['response'].apply(lambda x: x.strip().lower() == "the capital of france is paris.")

            # Save the processed data to a new CSV file in the same directory as the uploaded file
            output_file_path = os.path.join(os.path.dirname(self.file_path), "processed_results.csv")
            df.to_csv(output_file_path, index=False)

            # Notify the user that the file has been saved
            QMessageBox.information(self, "File Saved", f"Processed file saved successfully: {output_file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def onClickAI(self):
        print("Clicked")
        print(get_ai_response("Give this sentence a score A to F looking for any mistakes: 'How doot you do?'"))

# Run the application
app = QApplication(sys.argv)

app.setStyleSheet(Path('./styles/styles.qss').read_text())
window = MainWindow()
window.show()

app.exec_()