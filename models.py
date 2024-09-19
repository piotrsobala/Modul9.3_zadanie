import csv

class Expenses:
    def __init__(self, filepath):
        self.filepath = filepath
        self.expenses = []
        self._load_expenses()

#_LOAD_EXPENSES DO SPRAWDZENIA
    def _load_expenses(self):
        """Load expenses from the CSV file."""
        self.expenses = []
        try:
            with open(self.filepath, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.expenses.append(row)
        except FileNotFoundError:
            pass  # If the file doesn't exist yet, we'll create it on the first save.

    def all(self):
        """Return all expenses."""
        return self.expenses

    def get(self, expense_id):
        """Return a single expense by its ID."""
        return self.expenses[expense_id]

    def add(self, expense):
        """Add a new expense to the list."""
        expense = {key: value for key, value in expense.items() if key != 'csrf_token'}
        self.expenses.append(expense)

    def update(self, expense_id, expense):
        """Update an existing expense."""
        expense = {key: value for key, value in expense.items() if key != 'csrf_token'}
        self.expenses[expense_id] = expense

    def save_all(self):
        """Save all expenses to the CSV file."""
        with open(self.filepath, 'w', newline='') as csvfile:
            fieldnames = ['name', 'amount']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.expenses)
