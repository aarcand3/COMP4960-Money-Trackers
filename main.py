# Money Trackers - Team 1
# Jack Donahue, Simon, Allison, Sonia

# Library imports & Initial Values
import csv
import math
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPainter
from PyQt5.QtChart import QChart, QChartView, QPieSeries ##If not loading for team pip install PyQtChart
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from login import Ui_LoginWindow
from dashboard import Ui_MainWindow
from datetime import datetime
import sys
import os

userdata = ["userid","userpass","firstname","lastname"]
usertotals = ["networth", "totalbalence", "totaldebt", "totalincome"]


# Functions
def importUser(userid):
# Updates the users data in both the program var & the CSV
    global usertotals
    totaldebt = 0
    totalincome = 0
    totalbalence = 0
    # Calculate totaldebt from debt.csv
    with open("data/"+userid+"/debt.csv", mode="r") as data:
        csv_reader = csv.reader(data)
        iteration = 0
        for row in csv_reader:
            if iteration != 0:
                totaldebt += float(row[3])
            iteration += 1
        usertotals[2] = totaldebt
    # Calculate totalbalence from accounts.csv
    with open("data/"+userid+"/accounts.csv", mode="r") as data:
        csv_reader = csv.reader(data)
        iteration = 0
        for row in csv_reader:
            if iteration != 0:
                totalbalence += float(row[2])
            iteration += 1
        usertotals[1] = totalbalence
    # Calculate total income from income.csv
    with open("data/"+userid+"/income.csv", mode="r") as data:
        csv_reader = csv.reader(data)
        iteration = 0
        for row in csv_reader:
            if iteration != 0:
                totalincome += float(row[2])
            iteration += 1
        usertotals[3] = totalincome
    # Calculate Networth by subtraacting totaldebt from totalbalence
    usertotals[0] = totalbalence - totaldebt
def addExpense(userid):
    # Manually input expenses to purchaces.csv
    filepath = f"data/{userid}/purchaces.csv"

    # Makes sure the path is a valid path that exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # User Inputs Information Here
    print("\n=== Add New Expense ===")
    date = input("Enter date (MM/DD/YY): ").strip()
    card = input("Enter card used (e.g., Amex, Visa): ").strip()
    category = input("Enter expense type (e.g., Food, Taxi, Electronics): ").strip()
    try:
        amount = float(input("Enter amount: ").strip())
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return
    
    # Creates a dictionary to allow for appending.
    expense_entry = {
        "date": date,
        "card": card,
        "type": category,
        "amount": amount
    }

    # Creates dataframe
    df = pd.DataFrame([expense_entry])

    # Appends to csv file if it exists, creates one if it doesn't.
    file_exists = os.path.exists(filepath)
    if file_exists:
        try:
            df_existing = pd.read_csv(filepath)

            # Ensures columns are consistent
            if not all(col in df_existing.columns for col in df.columns):
                print("Warning: Column mismatch detected. Adjusting...")
                for col in df.columns:
                    if col not in df_existing.columns:
                        df_existing[col] = None
                df_existing = df_existing[df.columns]

            df.to_csv(filepath, mode="a", header=False, index=False)
        except Exception as e:
            print(f"Error appending to existing CSV: {e}")
    else:
        df.to_csv(filepath, mode="w", index=False)


    
    print(f"Expense successfully added for user '{userid}'\n")

def logthis(logname):
    # 
    if logname == "login.log":
        #Gets Current Time and Converts to String
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")


        log_entry = {
            "date": date_str,
            "time": time_str,
            "userid": userdata[0],
            "firstname": userdata[2],
            "lastname": userdata[3]
        }
        df = pd.DataFrame([log_entry])

        #Hashes userid, firstname and lastname without hashing date and time.
        for col in ["userid", "firstname", "lastname"]:
            df[col] = pd.util.hash_pandas_object(df[col], index=False).astype(str)

        df.to_csv(
            "logs/"+logname,
            mode="a",
            index=False,
            header=not pd.io.common.file_exists("logs/"+logname)
        )

    elif False:
        # Put new logging code here!
        pass
        
    else:
        print("ERROR! Could not find: "+logname+" is it configured?")


# login window and validation
class LoginWindow (QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.login_button.clicked.connect(self.check_login)
    def check_login(self):
        userdata[0] = self.ui.user_box.text()
        userdata[1] = self.ui.pw_box.text()
    ##validation
        with open("data/userlist.csv", mode="r") as data:
            csv_reader = csv.reader(data)
            for row in csv_reader:
                if row[0] == userdata[0] and row[1] == userdata[1]:
                    importUser(userdata[0])
                    userdata[0] = row[0] # UserID
                    userdata[1] = row[1] # Password
                    userdata[2] = row[2] # Firstname
                    userdata[3] = row[3] # Lastname
                    logthis("login.log")
                    self
                    self.dashboard_window = MainDashBoard()
                    self.dashboard_window.logged_in(userdata[0])
                    self.dashboard_window.show()
                    self.close()
                    return
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            
class MainDashBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dashboard = Ui_MainWindow()
        self.dashboard.setupUi(self)
        self.dashboard.logoutButton.clicked.connect(self.logout)
        
    def logged_in(self, username):
        self.dashboard.welcome_label.setText(f"Welcome, {username}")
        
        self.load_widgets(username)   
        self.show_charts(username)
    def load_widgets(self, username):
        model = QStandardItemModel()
        try:
            with open(f"data/{username}/purchaces.csv", mode="r") as file:
                reader = csv.reader(file)
                headers = next(reader)
                model.setHorizontalHeaderLabels(headers)
                for row in reader:
                    items = [QStandardItem(cell) for cell in row]
                    model.appendRow(items)
            self.dashboard.transaction_tableView.setModel(model)
        except FileNotFoundError:
            QMessageBox.warning(self,"Missing File", f"Could not find file for {username}")
    def create_chart(self, title, data_dict):
        series = QPieSeries()
        for label, value in data_dict.items():
            series.append(label, value)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        widget.setLayout(layout)
        return widget

    def show_charts(self, username):
        try:
            with open(f"data/{username}/debt.csv", mode="r") as debtfile:
                debtreader = csv.reader(debtfile)
                debt_data = {}
                next(debtreader, None) 
                for row in debtreader:
                    if len(row) >= 2:
                        label = row[1].strip().title()
                        value = float(row[3])
                        debt_data[label] = value
        except FileNotFoundError:
            QMessageBox.warning(self,"Missing File", f"Could not find file for {username}")
        try:
            with open(f"data/{username}/income.csv", mode="r") as incomefile:
                incomereader = csv.reader(incomefile)
                income_data = {}
                next(incomereader, None) 
                for row in incomereader:
                    if len(row) >= 2:
                        label = row[1].strip().title()
                        value = float(row[2])
                        income_data[label] = value
        except FileNotFoundError:
            QMessageBox.warning(self,"Missing File", f"Could not find file for {username}")

        chart_widget = self.create_chart("Debt Breakdown", debt_data)
        self.dashboard.tracking_tabWidget.addTab(chart_widget, "Debt Chart")
        chart_widget = self.create_chart("Income Sources", income_data)
        self.dashboard.tracking_tabWidget.addTab(chart_widget, "Income Chart")
        for i in reversed(range(self.dashboard.tracking_tabWidget.count())):
            tab = self.dashboard.tracking_tabWidget.widget(i)
            if tab.layout() is None or tab.layout().isEmpty():
                self.dashboard.tracking_tabWidget.removeTab(i)

    
    def logout(self):
        self.close()     


#ui start up 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())















