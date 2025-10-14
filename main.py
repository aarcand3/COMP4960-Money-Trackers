# Money Trackers - Team 1
# Jack Donahue, Simon, Allison, Sonia

# Library imports & Initial Values
import csv
import math
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from login import Ui_LoginWindow
from dashboard import Ui_MainWindow
from datetime import datetime
import sys

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
                totalincome += float(row[1])
            iteration += 1
        usertotals[3] = totalincome
    # Calculate Networth by subtraacting totaldebt from totalbalence
    usertotals[0] = totalbalence - totaldebt

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

    def logout(self):
        self.close()     


#ui start up 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())















