
# Flask Web Application with MongoDB, Data Processing, and AWS Deployment

This project demonstrates how to create a web application using **Flask** to collect user data, store it in **MongoDB**, process it using **Python**, visualize it, and deploy the app on **AWS EC2**.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Web Development with Flask](#web-development-with-flask)
4. [Data Storage with MongoDB](#data-storage-with-mongodb)
5. [Data Processing with Python](#data-processing-with-python)
6. [Data Visualization](#data-visualization)
7. [Deploying on AWS](#deploying-on-aws)
8. [Optional: PowerPoint Export](#optional-powerpoint-export)
9. [Troubleshooting](#troubleshooting)
10. [Conclusion](#conclusion)

---

## Prerequisites

Before starting, ensure you have the following:

- **Python 3.x** installed.
- **Flask** framework installed (`pip install flask`).
- **MongoDB** installed locally or use a cloud database service (like MongoDB Atlas).
- **AWS Account** for deployment.
- **Jupyter Notebook** installed (for data processing and visualization).
- **matplotlib** and **pandas** libraries installed in Python.

---

## Project Setup

### Clone the Repository

Clone the project repository to your local machine:

```bash
git clone https://github.com/your-repository.git
cd your-repository
```

### Install Dependencies

Create and activate a virtual environment for your project, then install the necessary dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/MacOS
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
```

Make sure that `requirements.txt` includes the necessary libraries such as `Flask`, `pymongo`, `gunicorn`, `pandas`, `matplotlib`, etc.

---

## Web Development with Flask

1. Create a **Flask app** (`app.py`) to serve as the main entry point of your web application.
2. The app collects **Age**, **Gender**, **Total Income**, and **Expenses** through a simple form with checkboxes and corresponding textboxes for each expense category (utilities, entertainment, school fees, shopping, healthcare).

### Example of `app.py`:

```python
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # Update with your connection string
db = client['user_data']
collection = db['survey']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Extract form data
        age = int(request.form.get('age', 0))
        gender = request.form.get('gender', 'Not Specified')
        income = float(request.form.get('income', 0))
        
        # Handle expense fields
        expenses = {
            "utilities": float(request.form.get('utilities', 0)),
            "entertainment": float(request.form.get('entertainment', 0)),
            "school_fees": float(request.form.get('school_fees', 0)),
            "shopping": float(request.form.get('shopping', 0)),
            "healthcare": float(request.form.get('healthcare', 0)),
        }

        # Prepare data for MongoDB
        data = {
            "age": age,
            "gender": gender,
            "income": income,
            "expenses": expenses,
        }
        
        # Insert data into MongoDB
        collection.insert_one(data)

        return redirect('/success')
    except Exception as e:
        return f"Error occurred: {e}"

@app.route('/success')
def success():
    return "Data submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
```

### Example of `index.html` (Form for user data):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Survey</title>
</head>
<body>
    <h1>User Survey Form</h1>
    <form action="/submit" method="POST">
        <label for="age">Age:</label>
        <input type="number" id="age" name="age" required><br>

        <label for="gender">Gender:</label>
        <select id="gender" name="gender" required>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
        </select><br>

        <label for="income">Total Income($):</label>
        <input type="number" id="income" name="income" required><br>

        <label>Expenses:</label><br>
        <input type="checkbox" id="utilities" name="expenses[utilities]"> Utilities:
        <input type="number" id="utilities-amount" name="expenses[utilities]" placeholder="Amount"><br>

        <input type="checkbox" id="entertainment" name="expenses[entertainment]"> Entertainment:
        <input type="number" id="entertainment-amount" name="expenses[entertainment]" placeholder="Amount"><br>

        <input type="checkbox" id="school_fees" name="expenses[school_fees]"> School Fees:
        <input type="number" id="school-fees-amount" name="expenses[school_fees]" placeholder="Amount"><br>

        <input type="checkbox" id="shopping" name="expenses[shopping]"> Shopping:
        <input type="number" id="shopping-amount" name="expenses[shopping]" placeholder="Amount"><br>

        <input type="checkbox" id="healthcare" name="expenses[healthcare]"> Healthcare:
        <input type="number" id="healthcare-amount" name="expenses[healthcare]" placeholder="Amount"><br>

        <button type="submit">Submit</button>
    </form>
</body>
</html>
```

---

## Data Storage with MongoDB

MongoDB is used to store user data, including **Age**, **Gender**, **Total Income**, and **Expenses**. Ensure that MongoDB is running on your local machine or use a cloud database like MongoDB Atlas.

- Store data in the `survey` collection within the `user_data` database.
  
---

## Data Processing with Python

### Create a Python class `User` to process the data:

```python
import pandas as pd
import pymongo

class User:
    def __init__(self, age, gender, income, expenses):
        self.age = age
        self.gender = gender
        self.income = income
        self.expenses = expenses

    def to_dict(self):
        return {
            "age": self.age,
            "gender": self.gender,
            "income": self.income,
            "expenses": self.expenses
        }

def fetch_data_from_mongo():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['user_data']
    collection = db['survey']
    data = collection.find()
    
    users = []
    for record in data:
        user = User(record['age'], record['gender'], record['income'], record['expenses'])
        users.append(user.to_dict())

    return users

def save_data_to_csv():
    data = fetch_data_from_mongo()
    df = pd.DataFrame(data)
    df.to_csv('user_data.csv', index=False)
```

---

## Data Visualization

Use **matplotlib** and **pandas** for visualization:

1. **Show the ages with the highest income**.
2. **Show the gender distribution across spending categories**.

### Example Code for Visualization in Jupyter:

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV
df = pd.read_csv('user_data.csv')

# Show ages with the highest income
top_ages = df[['age', 'income']].sort_values(by='income', ascending=False).head(10)
top_ages.plot(x='age', y='income', kind='bar', title="Top 10 Ages with Highest Income")
plt.savefig('charts/top_ages_by_income.png', dpi=300)

# Gender distribution across spending categories
expenses = ['utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare']
gender_expenses = df.groupby('gender')[expenses].sum()
gender_expenses.plot(kind='bar', stacked=True, title="Gender Distribution Across Spending Categories")
plt.savefig('charts/gender_distribution.png', dpi=300)
```

---

## Deploying on AWS

1. **Launch EC2 Instance**: Launch an EC2 instance with Amazon Linux or Ubuntu.
2. **Install Dependencies**: Install necessary packages like Python, Nginx, Gunicorn, etc.
3. **Configure Nginx and Gunicorn**: Set up a reverse proxy with Nginx and use Gunicorn to run your Flask app.
4. **Access Application**: Your

 Flask app will now be accessible on the internet via your EC2 instance's public IP.

---

## Optional: PowerPoint Export

Use Python libraries such as **python-pptx** to create slides from the visualized data (charts). Here's a quick example:

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()

# Add slide with a chart
slide_layout = prs.slide_layouts[5]  # Blank slide
slide = prs.slides.add_slide(slide_layout)
title = slide.shapes.title
title.text = "Data Visualizations"

# Add image (chart)
slide.shapes.add_picture('charts/top_ages_by_income.png', Inches(1), Inches(1), width=Inches(8))

prs.save('presentation.pptx')
```

---

## Troubleshooting

- Ensure MongoDB is running properly.
- Make sure all dependencies are installed correctly.
- Check the Flask application for any errors in the console.
