# Money Trackers - Team 1
# Jack Donahue, Simon, Allison, Sonia

import csv
import math
import pandas as pd
from PyQt5.QtWidgets import *

userQuit = False
loggedin = False
# [userid, firstname, lastname, balance]
userdata = ["userid", "userpass","firstname", "lastname", 0]


# While the user is not logged in, prompt for a valid userid
def loggin():
    global userQuit
    global loggedin 
    while not loggedin and not userQuit:
        userdata[0] = input("\nWelcome, please enter your user ID: ")
        userdata[1] = input("\nNow, please enter your password: ")
        # Imports data from user-data.csv to the userdata list, then logs it
        with open("data/userlist.csv", mode="r") as data:
            csv_reader = csv.reader(data)
            for row in csv_reader:
                if row[0] == userdata[0] and row[1] == userdata[1]:
                    userdata[1] = row[2]
                    userdata[2] = row[3]
                    userdata[3] = row[4]
                    loggedin = True
                    log_entry = {
                        "userid": userdata[0],
                        "firstname": userdata[2],
                        "lastname": userdata[3],
                        "balance": userdata[4]
                    }
                    df = pd.DataFrame([log_entry])
                    df.to_csv(
                        "test.log",
                        mode="a",
                        index=False,
                        header=not pd.io.common.file_exists("test.log")
                    )
                       
            if not loggedin:
                print ("\nInvalid, Please try again or enter")
                
            else:
                print ("[DEBUG] userdata: " + userdata[1], userdata[2], userdata[3])
                print ("\nWelcome " + userdata[1] + " " + userdata[2] + "!")

                # While the user is still loggedin loop operations untill they logout
                while loggedin:
                    select = input("what would you like to do today?\n\n[quit] Logout & Close\n[logout] Return to login page\n[1] Check Balance\n\nPlease make your selection: ")
                    if select == "quit":
                        userQuit = True
                        loggedin = False
                    elif select == "logout":
                        userdata[0] = "userid"
                        loggedin = False
                    elif select == "1":
                        print("\nYour Balance is: "+ userdata[3]+"\n")
                        print("your balance is: "+ userdata[3])
                    else:
                        print("\nInvalid try again\n")


# Main program loop
while not userQuit:
    loggin()

print("[DEBUG] program end")
































