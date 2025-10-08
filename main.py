# Money Trackers - Team 1
# Jack Donahue, Simon, Allison, Sonia

# Library imports
import csv
import math
import pandas as pd
from PyQt5.QtWidgets import *

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
    
            


# Program start
while not loggedin and not userQuit:
    userdata[0] = input("\nWelcome, please enter your user ID: ")
    userdata[1] = input("Now, please enter your password: ")
    # Imports data from userdata.csv to the userdata list, then logs the signin
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

            
        # When there is a sucessful login this block of code initiates the 'user session' loop
        if loggedin:
            print (userdata)
            print ("\nWelcome " + userdata[1] + " " + userdata[2] + "!")

            # While the user is still loggedin loop operations untill they logout
            while loggedin:
                select = input("Please make a selection\n\n[quit] Logout & Close\n[logout] Return to login page\n[1] Check Networth\n[2] Check total Debt\n[3] Check total income\n[4] Check total balence\n\nPlease make your selection: ")
                if select == "quit":
                    userQuit = True
                    loggedin = False
                elif select == "logout":
                    userdata[0] = "userid"
                    loggedin = False
                elif select == "1":
                    print("\nYour Networth is: "+str(userdata[4])+"\n") # Calculated by subtracting total debt from total balence
                elif select == "2":
                    print("\nYour total debt is: "+str(userdata[5])+"\n")
                elif select == "3":
                    print("\nYour total income is: "+str(userdata[6])+"\n")
                elif select == "4":
                    print("\nThe total balence: "+str(userdata[7])+"\n")
                else:
                    print("\nInvalid, try again\n")
        else:                
            print ("\nInvalid, try again")







