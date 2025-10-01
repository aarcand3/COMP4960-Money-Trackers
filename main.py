# Money Trackers - Team 1
# Jack Donahue, Simon, Allison, Sonia
import csv
import math
import pandas as pd

from PyQt5.QtWidgets import *


userQuit = False
loggedin = False
# [userid, firstname, lastname, balance]
userdata = ["userid", "firstname", "lastname", 0]


# reads the userid-money file and updates thir user-data CSV entry
def updateUser():
    #userid-money contains [index, date, cardtype, purchasetype, amount] this format will change
    pass


# While the user is not logged in, prompt for a valid userid
def loggin():
    global userQuit
    global loggedin 
    while not loggedin and not userQuit:
        userdata[0] = input("\nWelcome, please enter your user ID: ")
        if userdata[0] == "quit":
            userQuit = True
            loggedin = True
        else:
            # Imports data from user-data.csv to the userdata list, then logs it
            with open("data/userlist.csv", mode="r") as data:
                csv_reader = csv.reader(data)
                for row in csv_reader:
                    if row[0] == userdata[0]:
                        userdata[1] = row[1]
                        userdata[2] = row[2]
                        userdata[3] = row[3]
                        loggedin = True

                        log_entry = {
                            "userid": userdata[0],
                            "firstname": userdata[1],
                            "lastname": userdata[2],
                            "balance": userdata[3]
                        }
                        df = pd.DataFrame([log_entry])
                        df.to_csv(
                            "test.log",
                            mode="a",
                            index=False,
                            header=not pd.io.common.file_exists("test.log")
                        )

                        
                if not loggedin:
                    print ("\nInvalid, Please try again or enter [quit]")

# Reads a potential csv file and logs it to test, using comma as a delimiter


# Checks that the user id was found in the user-data.csv using the loggedin var and if so welcomes the user
def userSession():
    global userQuit
    global loggedin
    global userdata
    if loggedin:
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
    else:
        print("[ERROR] Escaped login loop without loggedin == True")


# Main program loop
while not userQuit:

    loggin()
    if loggedin and not userQuit:
        userSession()

print("[DEBUG] program end")
























