import flask
from flask import Blueprint,request, jsonify
from datetime import datetime

from models.Expense import Expense, db
from datetime import date


expenses = Blueprint('expenses', __name__)

@expenses.route('/expenses', methods=['GET'])
def get_expenses():
    all_expenses = Expense.query.all()

    serialized_expenses = [expense.as_dict() for expense in all_expenses]
    res = jsonify({"data": serialized_expenses})
    return res

@expenses.route('/expense', methods=['POST'])
def save_expense() -> flask.Response:
    try:
        res = request.get_json()

        new_expense = Expense(
            name=res['name'],
            description=res['description'],
            amount=res['amount'],
            date=datetime.strptime(res['date'], '%Y-%m-%d').date()
        )

        db.session.add(new_expense)
        db.session.commit()

        return jsonify({
            "message": "expense_created",
            "result": new_expense.as_dict()
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@expenses.route('/expense/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id: int) -> flask.Response:
    try:
        req_data = request.get_json()

        expense = Expense.query.get(expense_id)

        if not expense:
            return jsonify({"error": "Expense not found"}), 404
        
        expense.name = req_data.get('name', expense.name)
        expense.description = req_data.get('description', expense.description)
        expense.amount = req_data.get('amount', expense.amount)
        
        date_str = req_data.get('date')
        if date_str:
            expense.date = datetime.strptime(date_str, '%Y-%m-%d').date()

        db.session.commit()

        return jsonify({"message": "Expense updated", "result": expense.as_dict()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@expenses.route('/expense/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id: int) -> flask.Response:
    try:

        expense = Expense.query.get(expense_id)

        if not expense:
            return jsonify({"error": "Expense not found"}), 404

        db.session.delete(expense)
        db.session.commit()

        return jsonify({"message": "Expense deleted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500