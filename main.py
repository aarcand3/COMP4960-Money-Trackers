# Money Trackers - Team 1
# Jack Donahue, Simon Dean, Allison Arcand, Sonia Yahi

# Library imports & Initial Values
from cProfile import label
import csv
import math
import shutil
import re
from wsgiref import headers
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPainter
from PyQt5.QtChart import QChart, QChartView, QPieSeries ##If not loading for team pip install PyQtChart
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import *
from chatbox import Ui_Dialog as Ui_Chat
from login import Ui_LoginWindow
from dashboard import Ui_MainWindow
from datetime import datetime
import chat 
import sys
import os

userdata = ["userid","userpass","firstname","lastname"]
usertotals = ["networth", "totalbalence", "totaldebt", "totalincome"]
categorytotals = ["Housing", "Food", "Transport", "Personal Care", "Savings", "Debt Repay", "Other"]

# Functions
def importUser(userid):
    global usertotals
# Updates the users data in both the program var & the CSV
    totaldebt = 0
    totalincome = 0
    totalbalence = 0
    # Calculate totaldebt from debt.csv
    with open("data/"+userid+"/debt.csv", mode="r") as data:
        csv_reader = csv.reader(data)
        iteration = 0
        for row in csv_reader:
            if iteration != 0:
                totaldebt += float(row[2])
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

def getBudget():
    preferredTotals = ["housing", "Food", "Transport", "Personal Care", "Savings", "Debt minimums", "Other"]
    preferredTotals[0] = usertotals[3]*0.3 #housing
    preferredTotals[1] = 400  #food
    preferredTotals[2] = usertotals[3]*.2 #transportation
    preferredTotals[3] = 200  # personal care
    preferredTotals[4] = usertotals[3] * 0.1 #savings
    preferredTotals[5] = usertotals[2] *0.08 # debt repayment
    preferredTotals[6] = usertotals[3]*0.2 #other
    importUser(userdata[0])
    income = usertotals[3]
    networth = usertotals[0]

    budget = {
        "Income": round(income),
        "Housing": round(preferredTotals[0], 2),
        "Food": round(preferredTotals[1], 2),
        "Transport": round(preferredTotals[2], 2),
        "Personal Care": round(preferredTotals[3], 2),
        "Savings": round(preferredTotals[4], 2),
        "Debt Repayment": round(preferredTotals[5], 2),
        "Discretionary": round(preferredTotals[6], 2)
    }

    return budget


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

#function reads a user's debt CSV file
def load_debt_data(username):
    csv_path = f"data/{username}/debt.csv"
    debts = []
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    vendor = row['card'].strip()
                    amount = float(row['amount'])   # ✅ use 'amount' instead of 'balance'
                    interest_str = row['interest'].strip().replace('%', '')
                    interest = float(interest_str)

                    debts.append((vendor, amount,interest))
                except Exception as e:
                    print(f"⚠️ Skipping row due to error: {e}")
    except FileNotFoundError:
        print(f"⚠️ Debt file not found for user: {username}")
    except Exception as e:
        print(f"⚠️ Error loading debt data for {username}: {e}")

    return debts
#Calculates total debt
#sort the list by interest rate   

def summarize_debt(debts):
            total_debt = sum(d['balance'] for d in debts)
            for d in debts:
                d['monthly_interest'] = (d['balance'] * d['interest']) / 12 / 100
                d['annual_interest'] = (d['balance'] * d['interest']) / 100
            return total_debt

# function Save or update a savings goal for a specific user.

def saveCategoryGoal(userid, category, amount, due_date):
    try:
        # Validate amount
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            return {"error": f"Invalid goal amount: {amount}"}

        # Normalize date format (accept MM/DD/YYYY or DD-MM-YYYY, output YYYY-MM-DD)
        parsed_date = None
        for fmt in ("%m/%d/%Y", "%d-%m-%Y", "%Y-%m-%d"):
            try:
                parsed_date = datetime.strptime(due_date.strip(), fmt)
                break
            except ValueError:
                continue
        if not parsed_date:
            return {"error": f"Invalid due date format: {due_date}"}
        due_date = parsed_date.strftime("%Y-%m-%d")

        # Path setup
        path = f"data/{userid}/goals.csv"
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Load or initialize DataFrame
        if os.path.exists(path):
            df = pd.read_csv(path)
        else:
            df = pd.DataFrame(columns=["Category", "GoalAmount", "DueDate"])

        # Ensure consistent headers
        df = df.rename(
            columns={
                "category": "Category",
                "goalamount": "GoalAmount",
                "duedate": "DueDate"
            }
        )

        # Update or insert
        if "Category" in df.columns and category in df["Category"].values:
            df.loc[df["Category"] == category, ["GoalAmount", "DueDate"]] = [amount, due_date]
        else:
            new_row = pd.DataFrame([{"Category": category, "GoalAmount": amount, "DueDate": due_date}])
            df = pd.concat([df, new_row], ignore_index=True)

        # Save back
        df.to_csv(path, index=False)
        return True

    except Exception as e:
        return {"error": str(e)}

#Returns a list of all saved goals (category, amount, due date), progress

def getAllGoalsWithProgress(userid):
    accounts_path = f"data/{userid}/accounts.csv"
    goals_path = f"data/{userid}/goals.csv"

    if not os.path.exists(accounts_path) or not os.path.exists(goals_path):
        return []

    accounts_df = pd.read_csv(accounts_path)
    goals_df = pd.read_csv(goals_path)

    # Safely convert balances to numeric
    accounts_df["balance"] = pd.to_numeric(accounts_df["balance"], errors="coerce").fillna(0)
    total_balance = accounts_df["balance"].sum()

    enriched_goals = []
    for _, row in goals_df.iterrows():
        category = str(row.get("category", "")).strip()
        goalamount_raw = row.get("goalamount", "")
        duedate_raw = row.get("duedate", "")

        # Validate goalamount
        try:
            amount = float(goalamount_raw)
        except (ValueError, TypeError):
            print(f"⚠️ Skipping invalid goalamount: {goalamount_raw}")
            continue

        # Validate duedate format
        try:
            due_date = datetime.strptime(str(duedate_raw).strip(), "%d-%m-%Y").date()
        except (ValueError, TypeError):
            print(f"⚠️ Skipping invalid duedate: {duedate_raw}")
            continue

        progress_percent = round((total_balance / amount) * 100, 2) if amount > 0 else 0
        enriched_goals.append((category, amount, str(due_date), progress_percent))

    return enriched_goals

def getTotalSavingsProgress(userid):
    accounts_path = f"data/{userid}/accounts.csv"
    goals_path = f"data/{userid}/goals.csv"

    if not os.path.exists(accounts_path) or not os.path.exists(goals_path):
        return None

    accounts_df = pd.read_csv(accounts_path)
    goals_df = pd.read_csv(goals_path)

    # Use lowercase 'balance' column
    accounts_df["balance"] = pd.to_numeric(accounts_df["balance"], errors="coerce").fillna(0)
    total_balance = accounts_df["balance"].sum()

    goals_df["goalamount"] = pd.to_numeric(goals_df["goalamount"], errors="coerce").fillna(0)
    total_goal_amount = goals_df["goalamount"].sum()

    if total_goal_amount == 0:
        return 0.0

    total_progress = round((total_balance / total_goal_amount) * 100, 2)
    return total_progress

def create_new_user_account(userid, firstname, lastname, password, confirm_password):
    # Basic validation
    if not all([userid, firstname, lastname, password, confirm_password]):
        return {"error": "All fields are required."}

    if password != confirm_password:
        return {"error": "Passwords do not match."}

    if len(password) < 6:
        return {"error": "Password must be at least 6 characters."}

    if not re.match(r"^[a-zA-Z0-9_]+$", userid):
        return {"error": "User ID must be alphanumeric (underscores allowed)."}

    # File path setup
    user_dir = f"data/{userid}"
    user_file = f"{user_dir}/user.csv"

    if os.path.exists(user_file):
        return {"error": "User ID already exists."}

    try:
        os.makedirs(user_dir, exist_ok=True)
        with open(user_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["UserID", "FirstName", "LastName", "Password"])
            writer.writerow([userid, firstname, lastname, password])
        return {"success": f"Account created for {userid}."}
    except Exception as e:
        return {"error": str(e)}
#
# login window and validation
class LoginWindow (QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        self.ui.login_button.clicked.connect(self.check_login)
        self.ui.createaccount_button.clicked.connect(self.create_user)


    def create_user(self):
        # Collect input from GUI
        userid = self.ui.usernameEdit.text().strip()
        firstname = self.ui.firstnameEdit.text().strip()
        lastname = self.ui.lastnameEdit.text().strip()
        password = self.ui.passwordEdit.text().strip()
        confirm = self.ui.confirmEdit.text().strip()

        # Validate input
        if not all([userid, firstname, lastname, password, confirm]):
            QMessageBox.warning(self, "Invalid", "All fields are required.")
            return

        if password != confirm:
            QMessageBox.warning(self, "Invalid", "Passwords do not match.")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Invalid", "Password must be at least 6 characters.")
            return

        # Check for existing user in userlist.csv
        try:
            with open("data/userlist.csv", mode="r") as data:
                csv_reader = csv.reader(data)
                for row in csv_reader:
                    if not row or len(row) < 1:
                        continue
                    if row[0] == userid:
                        QMessageBox.warning(self, "Cannot Create User", "User already exists.")
                        return
        except FileNotFoundError:
            pass  # userlist.csv doesn't exist yet — will be created below

        # Save new user to userlist.csv
        try:
            with open("data/userlist.csv", mode="a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([userid, password, firstname, lastname])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to write userlist: {e}")
            return

        # Create user folder and starter files
        try:
            user_dir = f"data/{userid}"
            os.makedirs(user_dir, exist_ok=True)

            starter_files = {
                "accounts.csv": ["date", "bank", "balance"],
                "debt.csv": ["due_date", "card", "amount", "interest"],
                "goals.csv": ["Category", "goalamount", "DueDate"],
                "purchases.csv": ["date", "card", "type", "amount"],
                "income.csv": ["date", "from", "amount"]
            }

            for filename, headers in starter_files.items():
                filepath = os.path.join(user_dir, filename)
                with open(filepath, mode="w", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to create user files: {e}")
            return

        # Log and launch dashboard
        logthis("login.log")
        self.dashboard_window = MainDashBoard()
        self.dashboard_window.logged_in(userid)
        self.dashboard_window.show()
        self.close()

    def createfiles(self, username):
        # Define the path for user data
        base_path = os.path.join("data", "users", username)
        os.makedirs(base_path, exist_ok=True)

        purchases_file = os.path.join(base_path, "purchases.csv")
        savings_file = os.path.join(base_path, "goals.csv")
        accounts_file = os.path.join(base_path, "accounts.csv")

    # Create each file Should we do more?
        with open(purchases_file, mode="w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Card", "Type","Amount"])

        with open(savings_file, mode="w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["UserID", "Category", "Ammount", "Deadline"]) 

        with open(accounts_file, mode="w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Bank", "Balance"])


    def check_login(self):
        userdata[0] = self.ui.user_box.text()
        userdata[1] = self.ui.pw_box.text()
    ##validation
        with open("data/userlist.csv", mode="r") as data:
            csv_reader = csv.reader(data)
            for row in csv_reader:
                if len(row) < 4:
                   continue
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
class ChatBox(QDialog) :
    def __init__(self):
        super().__init__()
        self.chatBox = Ui_Chat()
        self.chatBox.setupUi(self)  
        self.response = []
        welcomeMessage =  ("Welcome to chat")
        self.updateChat(welcomeMessage)
        self.chatBox.sendButton.clicked.connect(self.sendChat)
        self.chatBox.lineEdit.setPlaceholderText("Type your message here...")


    def sendChat(self):
        text = self.chatBox.lineEdit.text().strip() # get text to send 
        response = chat.startChat(text)
        self.updateChat(response)

    def updateChat(self, newResponse):
         #add text to window
        if newResponse:
            label = QtWidgets.QLabel(newResponse)
            label.setWordWrap(True)  # wrap long messages
            self.chatBox.chatLayout.insertWidget(self.chatBox.chatLayout.count()-1, label)
            self.chatBox.lineEdit.clear()

            # Auto-scroll to bottom
        self.chatBox.chatWindow.verticalScrollBar().setValue(
                self.chatBox.chatWindow.verticalScrollBar().maximum())

class WarningBox(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Warning")
        self.layout = QVBoxLayout()
        self.setModal(True)
        self.label = QLabel(message)
        self.checkbox = QCheckBox("I understand the risks")
        self.checkbox.stateChanged.connect(self.toggle_ok_button)
        self.button = QPushButton("OK")
        self.button.setEnabled(False)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
    
    def toggle_ok_button(self, state):
        self.button.setEnabled(state == Qt.Checked)
        self.chat = ChatBox()
        self.button.clicked.connect(self.proceed_to_chat)
    def proceed_to_chat(self):
        self.close()
        self.chat = ChatBox()
        self.chat.show()

    def showWarning(self):
        self.exec_()
 
 
class MainDashBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dashboard = Ui_MainWindow()
        self.dashboard.setupUi(self)
        self.dashboard.logoutButton.clicked.connect(self.logout)
        self.dashboard.userchoice_comboBox.currentIndexChanged.connect(self.on_dropdown_change)
        self.dashboard.chatButton.clicked.connect(self.showChat)
        self.dashboard.frame.setAcceptDrops(True)
        self.dashboard.frame.installEventFilter(self)
        self.dashboard.add_expense_button.clicked.connect(self.addExpense)
        self.dashboard.add_account_button.clicked.connect(self.addAccount)
        self.dashboard.add_saving_button.clicked.connect(self.addNewSavings)
        self.dashboard.budget_button.clicked.connect(self.showBudget)

        self.setStyleSheet(f"""
        QWidget {{
            background-color:  #D8E4DC;  /* Light sage green */;
        }}
        QPushButton {{
            background-color: #4B6B50;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
        }}
        QPushButton:hover {{
            background-color: #5F7F65;
        }}
        QPushButton:pressed {{
            background-color: #3F5B40;
        }}
        """)
    def logged_in(self, username):
        self.dashboard.welcome_label.setText(f"Welcome, {username}")
        self.load_widgets(username)   
        self.show_charts(username)
        self.on_dropdown_change(self.dashboard.userchoice_comboBox.currentIndex())

        percentage = getTotalSavingsProgress(username)
        if percentage is not None:
            percentage = int(percentage)
        else:
            percentage = 0  #fallback value
        self.dashboard.debt_progressBar.setValue(percentage)

        self.populate_accounts_from_purchases(self.dashboard.expense_comboBox, username )
    def addAccount(self):
        account = self.dashboard.add_account_name.text()
        self.dashboard.expense_comboBox.addItem(account)
        self.dashboard.add_account_name.clear()

    def addNewSavings(self):
        filepath = f"data/{userdata[0]}/goals.csv"

        # Get raw inputs
        category = self.dashboard.savings_category.text().strip()
        amount_str = self.dashboard.saving_ammount_edit.text().strip()
        date_str= self.dashboard.saving_dateEdit.date().toString("dd-MM-yyyy")

        # Validate category
        if not category:
            QMessageBox.warning(self, "Invalid Input", "Category cannot be empty.")
            return

        # Validate amount
        try:
            amount = float(amount_str)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Goal amount must be a number.")
            return

        # Validate date format (YYYY-MM-DD)
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Due date must be in MM-DD-YYYY format.")
            return

        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Write validated data
        goaldata = [category, amount, date_str]
        with open(filepath, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(goaldata)

        # Update table
        self.load_widgets(userdata[0])

    def showChat (self):
        self.WarningBox = WarningBox("Warning. This Application is not responsible for any financial advice given. Please consult a professional for serious matters. By clicking ok you acknowledge responsibility for your own actions.")
        self.WarningBox.showWarning()
    def showBudget(self):
        self.dashboard.tableLabel.setText("This is a sample budget to be used for educational purposes only. ")
        self.dashboard.budget_button.setText("Debt Table")
      #  self.dashboard.goals_tableView.setParent(None)
        budget_model = getBudget()
        table = QStandardItemModel()
        table.setColumnCount(2)
        table.setRowCount(len(budget_model))
        table.setHorizontalHeaderLabels(["Category", "Amount"])

        for category, amount in budget_model.items():
                if not None:
                    row = [
                    QStandardItem(str(category)),
                    QStandardItem(str(amount)),
                    ]
                    table.appendRow(row)
                else:
                    pass
        self.dashboard.debt_tableView.setModel(table)

    def populate_accounts_from_purchases(self, combo_box, userid):
        combo_box.clear()
        filepath = f"data/{userid}/purchases.csv"
        seen_cards = set()

        try:
            with open(filepath, newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    card = row.get("card", "").strip()
                    if card and card not in seen_cards:
                     combo_box.addItem(card)
                     seen_cards.add(card)

            if not seen_cards:
                combo_box.addItem("No cards found")

        except FileNotFoundError:
            combo_box.addItem("No purchases file found")
    def on_dropdown_change(self, index):
        for widget in self.dashboard.csv_group:
                widget.hide()
        for widget in self.dashboard.expense_group:
                widget.hide()
        for widget in self.dashboard.add_account_group:
                widget.hide()
        for widget in self.dashboard.savings_group:
                widget.hide() 
        if index == 0:
            for widget in self.dashboard.csv_group:
                widget.hide()
            for widget in self.dashboard.expense_group:
                widget.hide()
            for widget in self.dashboard.add_account_group:
                widget.hide()
            for widget in self.dashboard.savings_group:
                widget.hide()            
        elif index == 1:
            for widget in self.dashboard.csv_group:
                widget.show()
                self.dashboard.frame.setAcceptDrops(True)
        elif index == 2:
            for widget in self.dashboard.add_account_group:
                widget.show()
        elif index == 3:
            for widget in self.dashboard.expense_group:
                widget.show()
        elif index == 4:
            for widget in self.dashboard.savings_group:
                widget.show()  
    def addExpense(self):
    # Manually input expenses to purchaces.csv
        filepath = f"data/{userdata[0]}/purchases.csv"

    # Makes sure the path is a valid path that exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
        date = self.dashboard.expense_dateEdit.text().strip()
        card = self.dashboard.expense_comboBox.currentText().strip()
        category = self.dashboard.category_comboBox.currentText().strip()
        amount = self.dashboard.ammount_edit.text().strip()
        expensedata = [date, card, category, amount]
        try:        
            with open(filepath, mode = "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(expensedata)
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return
        #update expense table
        self.load_widgets(userdata[0])
    

    def eventFilter(self, obj, event):
        if obj == self.dashboard.frame:
            if event.type() == QEvent.DragEnter:
                if event.mimeData().hasUrls():
                    for url in event.mimeData().urls():
                        if url.toLocalFile().lower().endswith(".csv"):
                            event.acceptProposedAction()
                            return True
                event.ignore()
                return True

            elif event.type() == QEvent.DragMove:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                    return True

            elif event.type() == QEvent.Drop:
                for url in event.mimeData().urls():
                    filePath = url.toLocalFile()
                    if filePath.lower().endswith(".csv"):
                        userFolder = os.path.join("data", userdata[0])
                        os.makedirs(userFolder, exist_ok=True)
                        destinationPath = os.path.join(userFolder, os.path.basename(filePath))
                        shutil.copy(filePath, destinationPath)
                        self.dashboard.label.setText(f"CSV file accepted: {filePath}")
                        self.load_widgets(userdata[0])
                        event.acceptProposedAction()
                    else:
                        print("Rejected non‑CSV file:", filePath)
                        event.ignore()
                return True
            return super().eventFilter(obj, event)

    def load_csv(self, filepath):
        try:
            with open(filepath, newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    print(row)  # Replace with logic to update your UI
        except Exception as e:
            print(f"Error reading CSV: {e}")
            
#imports a csv from an application (Excel for now)
    def import_csv_from_app(self, userid, target_name, file_path):
        try:
            #Makes sure there is a folder for user
            user_folder = os.path.join("data", userid)
            os.makedirs(user_folder, exist_ok=True)

            #Checks for output file    
            output_path = os.path.join(user_folder, f"{target_name}.csv")

            #Reads CSV
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='latin1')
            except pd.errors.ParserError:
            #Checks for Excel (which can use semicolons)
                df = pd.read_csv(file_path, sep=';')
            #Clean up column names
            df.columns = [col.strip().lower() for col in df.columns]

        #Normalize column names
            rename_map = {
                'date': 'date',
                'card': 'card',
                'type': 'type',
                'category': 'type',
                'amount': 'amount',
                'balance': 'balance',
                'interest': 'interest'
            }
            df.rename(columns={col: rename_map.get(col, col) for col in df.columns}, inplace=True)

            #Write/Append to existing file
            file_exists = os.path.exists(output_path)
            if file_exists:
                existing = pd.read_csv(output_path)
                # Align columns and concatenate
                combined = pd.concat([existing, df], ignore_index=True)
                combined.to_csv(output_path, index=False)
                rows_added = len(df)
            else:
               df.to_csv(output_path, index=False)
               rows_added = len(df)

            return {
                'status': 'success',
                'rows_imported': rows_added,
                'message': f"Imported {rows_added} rows into {target_name}.csv"
            }

    
        except Exception as e:
            return {
               'status': 'error',
                'rows_imported': 0,
                'message': f"⚠️ Import failed: {str(e)}"
            }

    def load_widgets(self, username):
        self.dashboard.tableLabel.setText("All Debt and All savings goals. ")
        model = QStandardItemModel()
        try:
            with open(f"data/{username}/purchases.csv", mode="r") as file:
                reader = csv.reader(file)
                headers = next(reader)
                model.setHorizontalHeaderLabels(headers)
                for row in reader:
                    items = [QStandardItem(cell) for cell in row]
                    model.appendRow(items)
            self.dashboard.transaction_tableView.setModel(model)
        except FileNotFoundError:
            QMessageBox.warning(self,"Missing File", f"Could not find file for {username}")
        
        goals_model = QStandardItemModel()
        try:
            goals = getAllGoalsWithProgress(username)
            headers = ["Category", "GoalAmount", "DueDate", "ProgressPercent"]
            goals_model.setColumnCount(len(headers))
            for category, amount, due_date, progress_percent in goals:
                row = [
                QStandardItem(str(category)),
                QStandardItem(str(amount)),
                QStandardItem(str(due_date)),
                QStandardItem(f"{progress_percent}%")
                ]
                goals_model.appendRow(row)
            goals_model.setHorizontalHeaderLabels(headers)


            self.dashboard.goals_tableView.setModel(goals_model)
        except FileNotFoundError:
            QMessageBox.warning(self, "Missing File", f"Could not find goals file")

        debt_model = QStandardItemModel()
        try:
            debt = load_debt_data(userdata[0])
            headers = ["Vendor", "Amount", "Interest"]
            debt_model.setColumnCount(len(headers))
            for vendor, amount, interest in debt:
                row = [
                QStandardItem(str(vendor)),
                QStandardItem(str(amount)),
                QStandardItem(f"{interest}%")
                ]
                debt_model.appendRow(row)
            debt_model.setHorizontalHeaderLabels(headers)
            self.dashboard.debt_tableView.setModel(debt_model)
        except FileNotFoundError:
            QMessageBox.warning(self, "Missing File", f"Could not find debt file")

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
        chart_view.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.setContentsMargins(0, 0, 0, 0)

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
        userdata.clear()
        self.window = LoginWindow()
        self.window.show()
        self.close()


#ui start up 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

    