from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "mydatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    expensename = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    

@app.route('/')
def add():
    return render_template("add.html")

@app.route('/delete/<int:id>')
def delete(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect('/expenses')
    
@app.route('/editexpense/<int:id>', methods=['GET', 'POST'])
def editexpense(id):
    expense = Expense.query.get_or_404(id)

    if request.method == 'POST':
        expense.date = request.form['date']
        expense.expensename = request.form['expensename']
        expense.amount = request.form['amount']
        expense.category = request.form['category']

        db.session.commit()
        return redirect('/expenses')

    return render_template('edit.html', expense=expense)   

@app.route('/addexpense', methods=['POST'])
def addexpense():
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    category = request.form['category']
    
    expense = Expense(date=date, expensename=expensename, amount=amount, category=category)
    db.session.add(expense)
    db.session.commit()
  
    return redirect('/')

@app.route('/expenses')
def expenses():
    expenses = Expense.query.all()
    return render_template('expenses.html', expenses=expenses)
    
    










if __name__ == '__main__':
     with app.app_context():
        db.create_all()
        app.run(debug=True)