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
userdata = ["userid","userpass","firstname","lastname","networth","totaldebt","totalincome"]
userQuit = False
loggedin = False

# login window and validation
class LoginWindow (QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.login_button.clicked.connect(self.check_login)
    def check_login(self):
        username = self.ui.user_box.text()
        password = self.ui.pw_box.text()
    ##validation
        if username == userdata[0] and password == userdata[1]:
            readUser(username)
            self.dashboard = MainWindow()
            self.dashboard.show()
            self.close()
            return
        QMessageBox.warning(self, "Login Failed", "Invalid username or password.")


#ui start up 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())


# Functions
# Updates the users data in both the program var & the CSV
def readUser(userid):
    global userdata
    totaldebt = 0
    totalincome = 0
    with open("data/"+userid+"/debt.csv", mode="r") as data:
        csv_reader = csv.reader(data)
        iteration = 0
        for row in csv_reader:
            if iteration != 0:
                totaldebt += float(row[3])
                print(row)
            iteration += 1
        userdata[5] = totaldebt
    with open("data/"+userid+"/income.csv", mode="r") as data:
        csv_reader = csv.reader(data)
        iteration = 0
        for row in csv_reader:
            if iteration != 0:
                totalincome += float(row[1])
                print(row)
            iteration += 1
        userdata[6] = totalincome
        userdata[4] = totalincome - totaldebt
            
#Program start  #currently not being used?
while not loggedin and not userQuit:

    userdata[0] = input("\nWelcome, please enter your user ID: ")
    userdata[1] = input("Now, please enter your password: ")
    # Imports data from userdata.csv to the userdata list, then logs the signin
    with open("data/userlist.csv", mode="r") as data:
        csv_reader = csv.reader(data)
        for row in csv_reader:
            if row[0] == userdata[0] and row[1] == userdata[1]:
                readUser(userdata[0])
                userdata[2] = row[2] # Firstname
                userdata[3] = row[3] # Lastname
                #userdata[4] = row[4] # Networth
                #userdata[5] = # Total Debt
                #userdata[6] = row[6] # Total Income
                loggedin = True
                log_entry = {
                    "userid": userdata[0],
                    "firstname": userdata[2],
                    "lastname": userdata[3],
                    "balance": userdata[4]
                }
                df = pd.DataFrame([log_entry])
                hashes = pd.util.hash_pandas_object(df)
                hashes.to_csv(
                    "test.log",
                    mode="a",
                    index=False,
                    header=not pd.io.common.file_exists("test.log")
                )
    # Imports data from the users 

            
        # When there is a sucessful login this block of code initiates the 'user session' loop
        if loggedin:
            print (userdata)
            print ("\nWelcome " + userdata[1] + " " + userdata[2] + "!")

            # While the user is still loggedin loop operations untill they logout
            while loggedin:
                select = input("Please make a selection\n\n[quit] Logout & Close\n[logout] Return to login page\n[1] Check Networth\n\nPlease make your selection: ")
                if select == "quit":
                    userQuit = True
                    loggedin = False
                elif select == "logout":
                    userdata[0] = "userid"
                    loggedin = False
                elif select == "1":
                    print("\nYour Balance is: "+ userdata[3]+"\n")
                else:
                    print("\nInvalid, try again\n")
        else:                
            print ("\nInvalid, try again")























