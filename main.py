# Money Trackers - Team 1
# Jack Donahue, Simon Dean, Allison Arcand, Sonia Yahi

# Library imports & Initial Values
from cProfile import label
import csv
import math
from wsgiref import headers
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPainter
from PyQt5.QtChart import QChart, QChartView, QPieSeries ##If not loading for team pip install PyQtChart
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import debt
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
            with open(csv_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    vendor = row['card'].strip()
                    balance = float(row['balance'])
                    interest_str = row['interest'].strip().replace('%', '')  # ✅ Strip %
                    interest = float(interest_str)
                    debts.append({
                        'vendor': vendor,
                        'balance': balance,
                        'interest': interest
                    })
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
        path = f"data/{userid}/goals.csv"
        if os.path.exists(path):
            df = pd.read_csv(path)
        else:
            df = pd.DataFrame(columns=["Category", "GoalAmount", "DueDate"])

        if category in df["Category"].values:
            df.loc[df["Category"] == category, ["GoalAmount", "DueDate"]] = [amount, due_date]
        else:
            new_row = pd.DataFrame([{"Category": category, "GoalAmount": amount, "DueDate": due_date}])
            df = pd.concat([df, new_row], ignore_index=True)

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

    accounts_df["balance"] = pd.to_numeric(accounts_df["balance"], errors="coerce").fillna(0)
    total_balance = accounts_df["balance"].sum()

    enriched_goals = []
    for _, row in goals_df.iterrows():
        category = row["category"]
        amount = float(row["amount"])
        due_date = row["due_date"]

        progress_percent = round((total_balance / amount) * 100, 2) if amount > 0 else 0


        enriched_goals.append({
            "Category": category,
            "GoalAmount": amount,
            "DueDate": due_date,
            "ProgressPercent": progress_percent,

        })

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

    goals_df["GoalAmount"] = pd.to_numeric(goals_df["GoalAmount"], errors="coerce").fillna(0)
    total_goal_amount = goals_df["GoalAmount"].sum()

    if total_goal_amount == 0:
        return 0.0

    total_progress = round((total_balance / total_goal_amount) * 100, 2)
    return total_progress
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
    ##creating user
        username = self.ui.usernameEdit.text().strip()
        firstname = self.ui.firstnameEdit.text().strip()
        lastname = self.ui.lastnameEdit.text().strip()
        password = self.ui.passwordEdit.text().strip()
        confirm = self.ui.confirmEdit.text().strip()

        if password != confirm:
            QMessageBox.warning(self, "Invalid", "Passwords do not match.")
            return

        userdata = [username, password, firstname, lastname,]

        with open("data/userlist.csv", mode="r") as data:
            csv_reader = csv.reader(data)
            for row in csv_reader:
                if row[0] == username:
                    QMessageBox.warning(self, "Cannot Create User.", "User already exists.")
                    return
                else:
                    with open("data/userlist.csv", mode = "a", newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(userdata)
                    logthis("login.log")
                    self.dashboard_window= MainDashBoard()
                    self.dashboard_window.logged_in(username)
                    self.dashboard_window.show()
                    self.close()


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
class ChatBox(QDialog) :
    def __init__(self):
        super().__init__()
        self.chatBox = Ui_Chat()
        self.chatBox.setupUi(self)   
#        self.chatBox.sendButton.clicked.connect(self.sendChat)
        self.chatBox.textEdit.setPlaceholderText("Type your message here...")

#   def sendChat(self):


 
 
class MainDashBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dashboard = Ui_MainWindow()
        self.dashboard.setupUi(self)
        self.dashboard.logoutButton.clicked.connect(self.logout)
        self.dashboard.userchoice_comboBox.currentIndexChanged.connect(self.on_dropdown_change)
        self.dashboard.frame.setAcceptDrops(True)
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
        self.dashboard.add_expense_button.clicked.connect(self.addExpense)
    def showChat (self):
        self.chat = ChatBox()
        self.chat.show()

    def populate_accounts_from_purchases(self, combo_box):
        combo_box.clear()
        filepath = f"data/{self.current_username}/purchases.csv"
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
            for widget in self.dashboard.expense_group:
                widget.hide()
        elif index == 1:
            for widget in self.dashboard.csv_group:
                widget.show()
        elif index == 2:
            for widget in self.dashboard.add_account_group:
                widget.hide()#replace with add account ?
        elif index == 3:
            for widget in self.dashboard.expense_group:
                widget.show()
        elif index == 4:
            for widget in self.dashboard.savings_group:
                widget.hide()    # need to replace for whatever we choose to add a savings goal?
        self.dashboard.expense_comboBox.currentIndexChanged.connect(self.on_dropdown_change)

    def addExpense(self, userid):
    # Manually input expenses to purchaces.csv
        filepath = f"data/{userid}/purchases.csv"

    # Makes sure the path is a valid path that exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
        date = self.dashboard.expense_dateEdit.text().strip()
        card = self.dashboard.expense_comboBox.currentText().strip()
        category = self.dashboard.type_lineEdit.text().strip()
        try:
            amount = self.dashboard.ammount_edit.text().strip()
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

        debt_model = QStandardItemModel()
#       try:      get debt to show single line not summary? or maybe summarize debt and savings in one file?
#            debt = load_debt_data(username)
#           debt_summary = summarize_debt(debt)
#            for debt_summary:
#            self.dashboard.debt_tableView.setModel(debt_model)
#        except FileNotFoundError:
#            QMessageBox.warning(self, "Missing File", f"Could not find debt file")
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
    def add_expense(self):
        data = [self.dashboard.expense_dateEdit, self.dashboard.expense_comboBox, ]
        with open("data/purchases.csv", 'a', newline='') as csvfile:
            csv_data = ['date', 'card', 'type', 'amount']
            writer = csv.DictWriter(csvfile, fieldnames=csv_data)
            writer.writeheader()
            writer.writerows(data)
    def logout(self):
        self.close()


#ui start up 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

    