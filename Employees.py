import requests     # Http request library for python
import psycopg2     # PostgreSQL library for Python

consultants = {}
SQL_database = {}


def get_new_employees():    # NEEDS UPDATED for SQL database once implemented
    """
    Grabs employee information from PIE andd adds any new employees into PIE
    """

    employee_data = {} # employee dictionary obtained using PIE data
    for employee in employee_data:
        if employee['username'] not in SQL_database:
            insert_employee(employee_data['username'])
        else:
            if employee['position'] != SQL_database[employee['position']]:
                SQL_database.update(employee['position'])      

def insert_employee(employee_data):
    """
    Inserts new employee into the PSQL database
    """
    SQL_database.update(employee_data)