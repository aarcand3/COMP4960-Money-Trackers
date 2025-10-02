# Money Trackers - Team 1
# Jack Donahue, Simon, Allison, Sonia

# Library imports
import csv
import math
import pandas as pd
from PyQt5.QtWidgets import *

# Inital values 
userdata = ["userid","userpass","firstname","lastname","networth","totaldebt","totalincome"]
userQuit = False
loggedin = False

# Functions
# Updates the users data in both the program var & the CSV
def updateUser():
    global userdata
    pass
    # Read from & sets users totalincome & totaldebt and calculates networth


# Program start
while not loggedin and not userQuit:
    userdata[0] = input("\nWelcome, please enter your user ID: ")
    userdata[1] = input("Now, please enter your password: ")
    # Imports data from userdata.csv to the userdata list, then logs the signin

    with open("data/userlist.csv", mode="r") as data:
        csv_reader = csv.reader(data)
        for row in csv_reader:
            if row[0] == userdata[0] and row[1] == userdata[1]:
                userdata[1] = row[2] # Firstname
                userdata[2] = row[3] # Lastname
                userdata[3] = row[4] # Networth
                userdata[4] = row[5] # Total Debt
                userdata[5] = row[6] # Total Income
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
            print ("[DEBUG] userdata: " + userdata[1], userdata[2], userdata[3])
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









































