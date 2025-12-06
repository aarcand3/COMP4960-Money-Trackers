import tkinter as tk
from tkinter import ttk, messagebox
from main import add_new_debt, load_debt_data  # Update if your backend file is named differently

# GUI setup
root = tk.Tk()
root.title("Debt Tracker")

# Labels and entry fields
tk.Label(root, text="User ID").grid(row=0, column=0)
userid_entry = tk.Entry(root, width=30)
userid_entry.grid(row=0, column=1)
userid_entry.insert(0, "jdoe")  # Default user ID

tk.Label(root, text="Card").grid(row=1, column=0)
card_entry = tk.Entry(root, width=30)
card_entry.grid(row=1, column=1)

tk.Label(root, text="Amount").grid(row=2, column=0)
amount_entry = tk.Entry(root, width=30)
amount_entry.grid(row=2, column=1)

tk.Label(root, text="Interest (%)").grid(row=3, column=0)
interest_entry = tk.Entry(root, width=30)
interest_entry.grid(row=3, column=1)

tk.Label(root, text="Due Date (MM/DD/YYYY)").grid(row=4, column=0)
due_date_entry = tk.Entry(root, width=30)
due_date_entry.grid(row=4, column=1)

# Submit function
def submit_debt():
    userid = userid_entry.get().strip()
    card = card_entry.get().strip()
    due_date = due_date_entry.get().strip()

    try:
        amount = float(amount_entry.get().strip())
        interest = float(interest_entry.get().strip())
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount and Interest must be numeric.")
        return

    if not all([userid, card, due_date]):
        messagebox.showerror("Missing Info", "Please fill in all fields.")
        return

    add_new_debt(userid, card, amount, interest, due_date)
    refresh_table()

# Refresh function
def refresh_table():
    userid = userid_entry.get().strip()
    debts = load_debt_data(userid)
    for row in tree.get_children():
        tree.delete(row)

    for debt in debts:
        tree.insert("", "end", values=(
            debt.get("due_date", ""),
            debt.get("card", "").title(),
            f"${debt.get('amount', 0):.2f}",
            f"{debt.get('interest', 0):.2f}%",
            f"${debt.get('MonthlyInterest', 0):.2f}",
            f"${debt.get('AnnualInterest', 0):.2f}"
        ))

# Buttons
tk.Button(root, text="Add Debt", command=submit_debt).grid(row=5, column=0, pady=10)
tk.Button(root, text="Refresh Table", command=refresh_table).grid(row=5, column=1)

# Table
columns = ("due_date", "card", "amount", "interest", "MonthlyInterest", "AnnualInterest")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col.replace("_", " ").title())
    tree.column(col, width=120)
tree.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
