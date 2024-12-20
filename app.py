from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from time import time
import os
import csv
from user import User

app = Flask(__name__, static_folder='app/static', template_folder='app/templates')

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['yaspi_survey_database']
collection = db['survey_data']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Extract basic form data
        age = int(request.form.get('age', 0))
        gender = request.form.get('gender', 'Not Specified')
        income = float(request.form.get('income', 0))

        # Extract and process expenses
        expenses = {}
        for category in ["utilities", "entertainment", "school_fees", "shopping", "healthcare"]:
            if request.form.get(f"{category}-checkbox") == "on":  # Checkbox checked
                expenses[category] = float(request.form.get(category, 0))  # Get amount
            else:
                expenses[category] = 0  # Default to 0 if checkbox not checked

        # Prepare data for MongoDB
        data = {
            "age": age,
            "gender": gender,
            "income": income,
            "expenses": expenses,
        }

        # Debugging output
        print(f"Data to insert: {data}")

        # Insert into MongoDB
        collection.insert_one(data)

        return redirect('/success')
    except Exception as e:
        # Log any errors for debugging
        print(f"Error processing form submission: {e}")
        return "An error occurred while processing your submission.", 500

@app.route('/success')

def success():
    return render_template('submission.html')

# Route to generate CSV
@app.route('/generate_csv')
def generate_csv():
    try:
        # Fetch data from MongoDB
        cursor = collection.find()

        # List to store User instances
        users = []

        # Loop through the MongoDB data and create User instances
        for record in cursor:
            age = record['age']
            gender = record['gender']
            income = record['income']
            expenses = record['expenses']
            
            user = User(age, gender, income, expenses)
            users.append(user)

        data_folder = 'data'
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        # Define the CSV file path inside the 'data' folder
        csv_file_path = os.path.join(data_folder, 'user_data.csv')

        # Write the data to CSV
        with open(csv_file_path, mode='w', newline='') as file:
            fieldnames = ["age", "gender", "income"] + [f"expense_{key}" for key in users[0].expenses.keys()]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write header
            writer.writeheader()

            # Write user data
            for user in users:
                writer.writerow(user.to_dict())

        return f"Data has been successfully written to {csv_file_path}"

    except Exception as e:
        # Log any errors for debugging
        print(f"Error generating CSV: {e}")
        return "An error occurred while generating the CSV.", 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

