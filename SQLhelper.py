import psycopg2
import APIHelper

class SQLhelper:
    def __init__(self):
        try:
            # Define your connection parameters
            self.connection = psycopg2.connect(
                user="postgres",
                password="5678",
                host="192.168.1.92",
                port="5432",
                database="iusc"
            )

            # Create a cursor object using the cursor() method
            self.cursor = self.connection.cursor()

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        
    def get_usernames(self):
        self.cursor.execute("SELECT username FROM employees")
        usernames = self.cursor.fetchall()

        return usernames
    
    def add_employee(self, id, username, first_name, last_name, role, training_status):
        insert_query = """INSERT INTO employees (id, username, firstname, lastname, role, trainingstatus) VALUES (%s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(insert_query, (id,username,first_name,last_name,role, training_status))

        self.connection.commit()
        print(f"Employee {username} added successfully")

    def clear_database(self):
        try:
            self.cursor.execute(f"TRUNCATE TABLE employees")
            self.connection.commit()
            print(f"Table 'employees' has been truncated.")
        except Exception as error:
            print(f"Error truncating table: {error}")

    
    def quit(self):
        self.cursor.close()
        self.connection.close()
        print("PostgreSQL connection is closed.")

if __name__ == "__main__":
    SQL = SQLhelper()
    usernames = SQL.get_usernames()
    for username in usernames:
        print(username[0])

    SQL.quit()

