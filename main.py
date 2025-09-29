# Money Trackers - Team 1
# Jack Donahue, Simon, Allison, Sonia
import sys
import csv
import math
loggedin = False

# Imports data from user-data.csv to the userdata list
# [userid, firstname, lastname, balence]
userdata = ["userid", "firstname", "lastname", 0]
def importUser(userid):
    global loggedin
    global userdata
    # read CSV and look for the userid they entered
    with open("user-data.csv", mode="r") as data:
        csv_reader = csv.reader(data)
        for row in csv_reader:
            if row[0] == userid:
                userdata[1] = row[1]
                userdata[2] = row[2]
                userdata[3] = row[3]
                loggedin = True
                break

# reads the userid-money file and updates thir user-data CSV entry
def updateUser():
    #userid-money contains [index, date, cardtype, purchacetype, ammount] this format will change
    pass




# PROGRAM START: Begining of user interaction
while not loggedin:
    userdata[0] = input("Welcome, please endter your user ID: ")
    if userdata[0] == "quit":
        sys.exit()
    importUser(userdata[0])
    if not loggedin:
        print ("\nInvalid, Please try again or enter 'quit'")


# Checks that the user id was found in the user-data.csv using the loggedin var and if so welcomes the user
if loggedin:
    print ("\nWelcome " + userdata[1] + " " + userdata[2] + "!")
    print ("[DEBUG] userdata: " + userdata[1], userdata[2], userdata[3])
    
    # While the user is still loggedin loop operations untill they loggout
    while loggedin:
        select = input("what would you like to do today?\n\n[quit] Loggout & Close\n[1] Check Balence\n\nPlease make your selection: ")
        if select == "quit":
            loggedin = False
            break
        elif select == 1:
            print("\nYour Balence is: "+ userdata[3]+"\n")
        else:
            print("\nInvalid try again\n")

else:
    print("error: esscaped loggin loop without loggedin var being True")
    sys.exit()
    

