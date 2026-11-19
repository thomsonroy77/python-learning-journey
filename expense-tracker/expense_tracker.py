
from datetime import datetime
import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "expenses.json")

expenses = []


def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    return []


def save_expenses():
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


def add_expense():
    try:
        amount = float(input("\nEnter expense amount (€): "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid amount.")
        return

    category = input("Enter category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    description = input("Enter description: ").strip()

    if not description:
        print("Description cannot be empty.")
        return

    expense = {
        "amount": round(amount, 2),
        "category": category,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    expenses.append(expense)
    save_expenses()

    print("\nExpense added successfully!")

def view_expenses():
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\n========== ALL EXPENSES ==========")

    for index, expense in enumerate(expenses, start=1):
        print(f"\nExpense #{index}")
        print(f"Amount: €{expense['amount']:.2f}")
        print(f"Category: {expense['category']}")
        print(f"Description: {expense['description']}")
        print(f"Date: {expense['date']}")

    print("\n==================================")
def calculate_total():
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    total = sum(expense["amount"] for expense in expenses)

    print("\n========== TOTAL SPENDING ==========")
    print(f"Total expenses: €{total:.2f}")
    print("====================================")


def category_summary():
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    category_totals = {}

    for expense in expenses:
        category = expense["category"]

        if category in category_totals:
            category_totals[category] += expense["amount"]
        else:
            category_totals[category] = expense["amount"]

    print("\n========== CATEGORY SUMMARY ==========")

    for category, total in category_totals.items():
        print(f"{category}: €{total:.2f}")

    print("======================================")


def monthly_summary():
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    month = input("\nEnter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format. Use YYYY-MM (example: 2026-11).")
        return

    monthly_expenses = [
        expense for expense in expenses
        if expense["date"].startswith(month)
    ]

    if not monthly_expenses:
        print(f"\nNo expenses found for {month}.")
        return

    total = sum(expense["amount"] for expense in monthly_expenses)

    print(f"\n========== EXPENSES FOR {month} ==========")

    for expense in monthly_expenses:
        print(
            f"{expense['date']} | "
            f"{expense['category']} | "
            f"€{expense['amount']:.2f} | "
            f"{expense['description']}"
        )

    print("------------------------------------------")
    print(f"Monthly total: €{total:.2f}")
    print("==========================================")

def delete_expense():
    if not expenses:
        print("\nNo expenses available to delete.")
        return

    view_expenses()

    try:
        expense_number = int(input("\nEnter the expense number to delete: "))

        if expense_number < 1 or expense_number > len(expenses):
            print("Invalid expense number.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    confirmation = input(
        "Are you sure you want to delete this expense? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        deleted_expense = expenses.pop(expense_number - 1)
        save_expenses()

        print(
            f"\nDeleted: {deleted_expense['category']} - "
            f"€{deleted_expense['amount']:.2f}"
        )
    else:
        print("\nDeletion cancelled.")
def main():
    global expenses
    expenses = load_expenses()

    print(f"Loaded {len(expenses)} saved expense(s).")

    print("\n================================")
    print("       MY EXPENSE TRACKER")
    print("================================")
    print("Welcome! Let's manage your expenses.")

    while True:
        print("\n=== EXPENSE TRACKER MENU ===")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Calculate total spending")
        print("4. Spending by category")
        print("5. Monthly summary")
        print("6. Delete expense")
        print("7. Exit")

        choice = input("\nChoose an option (1-7): ").strip()

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            calculate_total()

        elif choice == "4":
            category_summary()

        elif choice == "5":
            monthly_summary()

        elif choice == "6":
            delete_expense()

        elif choice == "7":
            print("Goodbye! Your expenses have been saved.")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 7.")
if __name__ == "__main__":
    main()
