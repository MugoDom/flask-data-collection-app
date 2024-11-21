
# Flask Web Data Collection Application

This project demonstrates how to create a simple web application using **Flask** to collect user data, store it in **MongoDB**, and process the data using **Python** libraries, then visualize it.
It also enmpossases the app deployment on **AWS EC2**.

Live Demo: [http://13.60.198.88:5000/]

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Web Development with Flask](#web-development-with-flask)
4. [Data Storage with MongoDB](#data-storage-with-mongodb)
5. [Data Processing with Python](#data-processing-with-python)
6. [Data Visualization](#data-visualization)
7. [Deploying on AWS](#deploying-on-aws)
8. [Troubleshooting](#troubleshooting)
9. [Improvements](#improvements)

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
4. Run the app on your local machine by running the following on the terminal:
 ```bash
 python app.py

 ```

---

## Data Storage with MongoDB

MongoDB is used to store user data, including **Age**, **Gender**, **Total Income**, and **Expenses**. Ensure that MongoDB is running on your local machine. The installation instructions can be found here:[https://www.mongodb.com/docs/manual/installation/]

- Store data in the `survey_data` collection within the `user_data` database. The name of the database can be adjusted to your preference.
  
---

## Data Processing with Python

### Create a Python class `User` to process the data:
The Class 'User' can be found on the user.py file and is imported into the Flask app.

---

## Data Visualization

Use **matplotlib** and **pandas** for visualization in **Jupyter Notebook**. For instance to:

1. **Show the ages with the highest income**.
2. **Show the gender distribution across spending categories**.

---

## Deploying on AWS

1. **Launch EC2 Instance**: Launch an EC2 instance with Amazon Linux or Ubuntu.
2. **Install Dependencies**: Install necessary packages like Python, Nginx, Gunicorn, etc.
3. **Configure Nginx and Gunicorn**: Set up a reverse proxy with Nginx and use Gunicorn to run your Flask app.
4. **Access Application**: Your Flask app will now be accessible on the internet via your EC2 instance's public IP.

---

## Troubleshooting

- Ensure MongoDB is running properly.
- Make sure all dependencies are installed correctly.
- Check the Flask application for any errors in the console.

## Improvements

- Improvements to the App are welcome.