

from main import add_new_debt, load_debt_data  # ✅ import your functions

def run_test():
    userid = "jdoe"

    # ✅ Add sample debts
    add_new_debt(userid, "Amex", 893.44, "10%", "12/05/2025")
    add_new_debt(userid, "car", 1100.00, "4.3%", "01/01/2026")
    add_new_debt(userid, "school", 1100.00, "4.3%", "01/01/2026")  # duplicate

    # ✅ Load and display
    debts = load_debt_data(userid)
    print("\n Debt Summary")
    print("-" * 70)
    for debt in debts:
        print(f"{debt['DueDate']} | {debt['Card']:10} | ${debt['amount']:8.2f} | "
              f"{debt['InterestRate']:6} | Monthly: ${debt['MonthlyInterest']:6.2f} | "
              f"Annual: ${debt['AnnualInterest']:6.2f}")
    print("-" * 70)
    print(f" Total entries: {len(debts)}")

if __name__ == "__main__":
    run_test()
