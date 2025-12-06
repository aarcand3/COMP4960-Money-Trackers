import tkinter as tk
from tkinter import ttk, messagebox
from main import add_new_bank_entry, load_account_data  # backend functions

# GUI setup
root = tk.Tk()
root.title("Bank Account Tracker")

# Labels and entry fields
tk.Label(root, text="User ID").grid(row=0, column=0)
userid_entry = tk.Entry(root, width=30)
userid_entry.grid(row=0, column=1)
userid_entry.insert(0, "jdoe")  # Default user

tk.Label(root, text="Date (MM/DD/YYYY)").grid(row=1, column=0)
date_entry = tk.Entry(root, width=30)
date_entry.grid(row=1, column=1)

tk.Label(root, text="Bank").grid(row=2, column=0)
bank_entry = tk.Entry(root, width=30)
bank_entry.grid(row=2, column=1)

tk.Label(root, text="Balance").grid(row=3, column=0)
balance_entry = tk.Entry(root, width=30)
balance_entry.grid(row=3, column=1)

# Submit function
def submit_account():
    userid = userid_entry.get().strip()
    date = date_entry.get().strip()
    bank = bank_entry.get().strip()
    balance = balance_entry.get().strip()

    if not all([userid, date, bank, balance]):
        messagebox.showerror("Missing Info", "Please fill in all fields.")
        return

    try:
        balance = float(balance)
    except ValueError:
        messagebox.showerror("Invalid Input", "Balance must be numeric.")
        return

    add_new_bank_entry(userid, date, bank, balance)
    refresh_table()

# Refresh function
def refresh_table():
    userid = userid_entry.get().strip()
    accounts = load_account_data(userid)
    for row in tree.get_children():
        tree.delete(row)

    for acc in accounts:
        tree.insert("", "end", values=(
            acc["date"],
            acc["bank"],
            f"${acc['balance']:.2f}"
        ))

# Buttons
tk.Button(root, text="Add Account", command=submit_account).grid(row=4, column=0, pady=10)
tk.Button(root, text="Refresh Table", command=refresh_table).grid(row=4, column=1)

# Table
columns = ("date", "bank", "balance")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col.title())
    tree.column(col, width=120)
tree.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()