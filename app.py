from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from time import time

app = Flask(__name__, static_folder='app/static', template_folder='app/templates')

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['user_database']
collection = db['user_data']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    age = request.form['age']
    gender = request.form['gender']
    income = request.form['income']
    expenses = {
        "utilities": request.form.get('utilities', 0),
        "entertainment": request.form.get('entertainment', 0),
        "school_fees": request.form.get('school_fees', 0),
        "shopping": request.form.get('shopping', 0),
        "healthcare": request.form.get('healthcare', 0),
    }
    data = {
        "age": age,
        "gender": gender,
        "income": income,
        "expenses": expenses,
    }
    collection.insert_one(data)
    return redirect('/success')

@app.route('/success')
def success():
    return render_template('submission.html')

if __name__ == '__main__':
    app.run(debug=True)

