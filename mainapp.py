from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Network Data Visualization")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Load and process data
        self.load_data()

        # Apply styles
        self.apply_styles()

        # Display components
        self.display_data()

    def apply_styles(self):
        # Set gradient background
        palette = QPalette()
        gradient = 'qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #f6d365, stop:1 #fda085)'
        palette.setBrush(QPalette.Window, QColor(255, 255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        
        # Set stylesheet for buttons and table
        self.setStyleSheet("""
            QPushButton {
                background-color: #fda085;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #f6d365;
                color: black;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f6d365;
                selection-background-color: #fda085;
            }
        """)

    def load_data(self):
        # Path to the dataset
        self.file_path = 'C:/Users/LENOVO/Desktop/Cyber/NetworkData.xlsx'

        # Check if the file exists
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file at {self.file_path} was not found.")

        # Read the dataset
        try:
            self.df = pd.read_excel(self.file_path)
        except Exception as e:
            raise Exception(f"Error reading the Excel file: {e}")

        # Print unique values in the Reputation column for debugging
        print("Unique values in 'Reputation' column:", self.df['Reputation'].unique())

        # Assuming df_final is the same as df for now; replace with actual df_final if different
        self.df_final = self.df

    def display_data(self):
        # Display the first few rows of the dataset
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        self.update_table(self.df.head())

        # Add buttons for different functionalities
        self.buttons_layout = QHBoxLayout()

        self.heatmap_button = QPushButton("Show Heatmap", self)
        self.heatmap_button.clicked.connect(self.show_heatmap)
        self.buttons_layout.addWidget(self.heatmap_button)

        self.reputation_button = QPushButton("Show Reputation Data", self)
        self.reputation_button.clicked.connect(self.show_reputation_data)
        self.buttons_layout.addWidget(self.reputation_button)

        self.malicious_button = QPushButton("Show Malicious Activities", self)
        self.malicious_button.clicked.connect(self.show_malicious_activities)
        self.buttons_layout.addWidget(self.malicious_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.show_initial_data)
        self.buttons_layout.addWidget(self.back_button)

        self.layout.addLayout(self.buttons_layout)

    def update_table(self, data):
        self.table.setColumnCount(len(data.columns))
        self.table.setRowCount(len(data.index))
        self.table.setHorizontalHeaderLabels(data.columns)

        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(data.iat[i, j])))

    def show_heatmap(self):
        df_numeric = self.df_final.select_dtypes(include=[float, int])

        fig, ax = plt.subplots(figsize=(12, 10))  # Increase figure size for better visibility
        sns.heatmap(df_numeric.corr(), annot=True, ax=ax, cmap='coolwarm', linewidths=0.5)  # Add colormap and linewidths

        plt.show()

    def show_reputation_data(self):
        reputation_data = self.preprocess_reputation(self.df)

        fig, ax = plt.subplots()
        reputation_data.plot(kind='bar', ax=ax)
        ax.set_title("Reputation Data")

        plt.show()

    def preprocess_reputation(self, df):
        reputation_counts = df['Reputation'].value_counts(normalize=True)
        reputation_data = pd.Series({'AVERAGE': reputation_counts['AVERAGE'], 'GOOD': reputation_counts['GOOD']})
        return reputation_data

    def show_malicious_activities(self):
        # Filter rows where the 'Reputation' is not 'GOOD' or 'AVERAGE'
        malicious_activities = self.df[~self.df['Reputation'].str.upper().isin(['GOOD', 'AVERAGE'])]

        # Print the first few rows of the filtered data for debugging
        print("Filtered malicious activities:\n", malicious_activities.head())

        self.update_table(malicious_activities.head())

    def show_initial_data(self):
        # Display the initial data (first few rows of the original dataset)
        self.update_table(self.df.head())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
