
# Flask Web Application with MongoDB, Data Processing, and AWS Deployment

This project demonstrates how to create a simple web application using **Flask** to collect user data, store it in **MongoDB**, and process the data using **Python** libraries, then visualize it.
It also enmpossases the app deployment on **AWS EC2**.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Web Development with Flask](#web-development-with-flask)
4. [Data Storage with MongoDB](#data-storage-with-mongodb)
5. [Data Processing with Python](#data-processing-with-python)
6. [Data Visualization](#data-visualization)
7. [Deploying on AWS](#deploying-on-aws)
8. [Troubleshooting](#troubleshooting)

---
## Prerequisites

Make sure to install the following. It is recommended to use a Virtual environment. 

- **Python 3.9 or greater**.
- **Flask** framework (`pip install flask`).
- **MongoDB** locally installed or use a cloud database service (like MongoDB Atlas).
- **AWS Account** for deployment.
- **Jupyter Notebook** (for data processing and visualization).
- **matplotlib** and **pandas** libraries (For data manipulation and visualization)

---

## Project Setup

### Clone the Repository

Clone the project repository to your local machine:

```bash
git clone https://github.com/MugoDom/flask-data-collection-app.git
cd flask-data-collection-app
```

### Install Dependencies

Create and activate a virtual environment for your project, then install the necessary dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/MacOS
venv\Scripts\activate     # For Windows
pip install -r requirements.txt 
```

The requirements txt file includes the necessary libraries such as `Flask`, `pymongo`, `gunicorn`, `pandas`, `matplotlib`, etc.

---

## Web Development with Flask

1. Create a **Flask app** (`app.py`) to serve as the main entry point of your web application.
2. The app collects **Age**, **Gender**, **Total Income**, and **Expenses** through a simple form.
3. The app also generates a csv file from the data collected.

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
