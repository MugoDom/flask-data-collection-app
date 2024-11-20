# user.py

class User:
    def __init__(self, age, gender, income, expenses):
        self.age = age
        self.gender = gender
        self.income = income
        self.expenses = expenses

    def to_dict(self):
        expense_data = {f"expense_{key}": value for key, value in self.expenses.items()}
        user_data = {
            "age": self.age,
            "gender": self.gender,
            "income": self.income
        }
        user_data.update(expense_data)
        return user_data
