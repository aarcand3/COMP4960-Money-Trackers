# Money Trackers - Team 1
# Jack Donahue, Simon, Allison, Sonia

# Library imports
import csv
import math
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from login import Ui_LoginWindow
from dashboard import MainWindow
import sys

# Inital values 
userdata = ["userid","userpass","firstname","lastname","networth","totaldebt","totalincome", "totalbalence"]
userQuit = False
loggedin = False

# Functions
# Updates the users data in both the program var & the CSV
def importUser(userid):
    global userdata
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
        userdata[5] = totaldebt
    # Calculate totalbalence from accounts.csv
    with open("data/"+userid+"/accounts.csv", mode="r") as data:
        csv_reader = csv.reader(data)
        iteration = 0
        for row in csv_reader:
            if iteration != 0:
                totalbalence += float(row[2])
            iteration += 1
        userdata[7] = totalbalence
    # Calculate total income from income.csv
    with open("data/"+userid+"/income.csv", mode="r") as data:
        csv_reader = csv.reader(data)
        iteration = 0
        for row in csv_reader:
            if iteration != 0:
                totalincome += float(row[1])
            iteration += 1
        userdata[6] = totalincome
    # Calculate Networth by subtraacting totaldebt from totalbalence
    userdata[4] = totalbalence - totaldebt


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
                    userdata[2] = row[2] # Firstname
                    userdata[3] = row[3] # Lastname
                    #userdata[4] = row[4] # Networth
                    #userdata[5] = row[5] # Total Debt
                    #userdata[6] = row[6] # Total Income
                    #userdata[7] = row[7] # Total account value
                    loggedin = True
                    log_entry = {
                        "userid": userdata[0],
                        "firstname": userdata[2],
                        "lastname": userdata[3]
                    }
                    df = pd.DataFrame([log_entry])
                    hashes = pd.util.hash_pandas_object(df)
                    hashes.to_csv(
                        "test.log",
                        mode="a",
                        index=False,
                        header=not pd.io.common.file_exists("test.log")
                    )
                    MainDashBoard.logged_in(self, userdata[0])
                    self.close()
                    return
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
class MainDashBoard(QMainWindow):
    def __init__(self):
        super.__init__()
        self.dashboard = MainWindow()
        self.dashboard.setupUi(self)
    def logged_in(self, username):
            self.dashboard = MainWindow()
            self.dashboard.show()


#ui start up 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())


