import psycopg2

class SQLhelper:
    def __init__(self):
        self.conn.
def connect_SQL_database():
    try:
        # Define your connection parameters
        connection = psycopg2.connect(
            user="postgres",
            password="5678",
            host="192.168.1.92",
            port="5432",
            database="iusc"
        )

        # Create a cursor object using the cursor() method
        cursor = connection.cursor()

        # Define the insert query and the data to be inserted
        insert_query = """ INSERT INTO Employees (id, name, position) VALUES (%s, %s, %s)"""
        employee_data = (1, 'John Doe', 'Software Engineer')  # Replace with actual employee data

        # Execute the insert query
        cursor.execute(insert_query, employee_data)

        # Commit the transaction
        connection.commit()
        print("Employee added successfully.")


    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        # Close the database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")
    
def get_usernames():
