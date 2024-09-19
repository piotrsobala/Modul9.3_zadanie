from flask import Flask, render_template, request, redirect, url_for, jsonify, abort

from forms import ExpenseForm
from models import Expenses

app = Flask(__name__)
app.config["SECRET_KEY"] = "klucznik"

expenses = Expenses("expenses.csv")

@app.route("/")
def index():
    return render_template("index.html", expenses=expenses.all())


@app.route("/add/", methods=["GET", "POST"])
def add_expense():
    form = ExpenseForm()
    if request.method == "POST" and form.validate_on_submit():
        expenses.add(form.data)
        expenses.save_all()
        return redirect(url_for("index"))
    return render_template("add_expense.html", form=form)


@app.route("/update/<int:expense_id>/", methods=["GET", "POST"])
def update_expense(expense_id):
    expense = expenses.get(expense_id)
    form = ExpenseForm(data=expense)
    
    if request.method == "POST" and form.validate_on_submit():
        expenses.update(expense_id, form.data)
        expenses.save_all()
        return redirect(url_for("index"))

    return render_template("update_expense.html", form=form, expense_id=expense_id)

#REST API
@app.route('/api/expenses/', methods=['GET'])
def get_expenses():
    """Get all expenses."""
    return jsonify(expenses.all()), 200

@app.route('/api/expenses/<int:expense_id>/', methods=['GET'])
def get_expense(expense_id):
    """Geta single expense by ID."""
    try:
        expense = expenses.get(expense_id)
        return jsonify(expense), 200
    except IndexError:
        abort(404, description="Expense not found")

@app.route('/api/expenses/', methods=['POST'])
def create_expense():
    """Create a new expense."""
    if not request.json or 'name' not in request.json or 'amount' not in request.json:
        abort(400, description="Invalid input")
    
    new_expense = {
        'name': request.json['name'],
        'amount': request.json['amount']
    }
    
    expenses.add(new_expense)
    expenses.save_all()
    return jsonify(new_expense), 201

@app.route('/api/expenses/<int:expense_id>/', methods=['PUT'])
def api_update_expense(expense_id):
    """Update an existing expense."""
    if not request.json:
        abort(400, description="Invalid input")
    
    try:
        expense = expenses.get(expense_id)
    except IndexError:
        abort(404, description="Expense not found")
    
    updated_data = {
        'name': request.json.get('name', expense['name']),
        'amount': request.json.get('amount', expense['amount'])
    }
    
    expenses.update(expense_id, updated_data)
    expenses.save_all()
    return jsonify(updated_data), 200

@app.route('/api/expenses/<int:expense_id>/', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete an expense by ID."""
    try:
        expense = expenses.get(expense_id)
    except IndexError:
        abort(404, description="Expense not found")
    
    expenses.save_all()
    return jsonify({'result': True}), 200



if __name__ == "__main__":
    app.run(debug=True)
