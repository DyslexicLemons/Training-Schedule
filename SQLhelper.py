import psycopg2
from datetime import datetime

"""
Tips and tools for using Postgres
Connect to postgres database: 


"""

class SQLHelper:
    def __init__(self):
        """
        
        """
        try:
            # Define your connection parameters
            self.connection = psycopg2.connect( # to connect manually type in "psql  -h 192.168.4.28 -d iusc iU postgres -p 5432" and for password, type "5678"
                user="postgres",
                password="5678",
                host="192.168.4.28",
                port="5432",
                database="iusc"
            )

            # Create a cursor object using the cursor() method
            self.cursor = self.connection.cursor()

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        

    def get_usernames(self):
        # Retrieve the current usernames from the database
        self.cursor.execute("SELECT username FROM employees;")
        # Use a list comprehension to flatten the list of tuples
        return [row[0] for row in self.cursor.fetchall()]

    
    def get_trainees(self):
        self.cursor.execute("SELECT firstname, lastname, username, role FROM employees WHERE trainingstatus = 'Trainee'")
        trainees = self.cursor.fetchall()

        return trainees
    
    def add_employee(self, id, username, first_name, last_name, role, training_status):
        insert_query = """INSERT INTO employees (id, username, firstname, lastname, role, trainingstatus) VALUES (%s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(insert_query, (id,username,first_name,last_name,role, training_status))

        self.connection.commit()
        print(f"Employee {username} added successfully")

    def remove_employee(self, username):
        try:
            # Delete the employee from the database by username
            self.cursor.execute("DELETE FROM employees WHERE username = %s;", (username,))
            self.connection.commit()
            print(f'User {username} removed successfully.')

        except Exception as e:
            print(f"An error occurred while removing user {username}: {e}")
            self.connection.rollback()

    def upsert_employee(self, id, username, first_name, last_name, role, training_status):
        try:
            # Execute the upsert query
            self.cursor.execute("""
                INSERT INTO employees (id, username, firstname, lastname, role, trainingstatus)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id, username) DO UPDATE
                SET 
                    firstname = EXCLUDED.firstname,
                    lastname = EXCLUDED.lastname,
                    role = EXCLUDED.role,
                    trainingstatus = EXCLUDED.trainingstatus;
            """, (id, username, first_name, last_name, role, training_status))

            # Commit the changes
            self.connection.commit()
            print(f"Employee '{username}' added or updated successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()




    def clear_employee_database(self):
        double_check = input("Are you sure you want to clear the database?\n Type 'y' or 'n': ")
        if double_check != 'y':
            print(f"User denied clear database")
            return None
        try:
            self.cursor.execute(f"TRUNCATE TABLE employees")
            self.connection.commit()
            print(f"Table 'employees' has been truncated.")
            return 'okay'
        except Exception as error:
            print(f"Error truncating table: {error}")
            return None

    def create_training_schedule(self,username):
        pass
 

    def update_employees(self, json):
        usernames = []

        current_usernames = self.get_usernames()
        training_status = ""
        for shift in json: # each item in the JSON is describing a  shift
            PIErole = shift["shiftGroup"]["role"]["name"]
            if shift["user"] is not None and shift["user"]["username"] not in usernames:
                if PIErole == "PA (Supervisor)" or PIErole == "Comp Coord (Supervisor)":
                    role = "Supervisor"
                else:
                    role = "Consultant"
                    if PIErole == "Trainee":
                        training_status = "Trainee"
                self.upsert_employee(shift["user"]["id"], shift["user"]["username"], shift["user"]["firstName"], shift["user"]["lastName"], role, training_status) 
                usernames = usernames + [shift["user"]["username"]]

        removed_usernames = set(current_usernames) - set(usernames)

        # Remove employees that are no longer present
        for username in removed_usernames:
            self.remove_employee(username)
            print(f'User {username} removed\n')

    def get_todays_training_tasks(self):
        today_date = "2024-09-20"  # You can get today's date dynamically using datetime
        self.cursor.execute("""
            SELECT username, filename FROM training_schedule
            WHERE date = %s;
        """, (today_date,))
        return self.cursor.fetchall()
    

    def add_training_day(self, week_of, username, date, filename):
        try:
            # Insert the new training day into the training_schedule table
            self.cursor.execute("""
                INSERT INTO training_schedule (week_of, username, date, filename)
                VALUES (%s, %s, %s, %s);
            """, (week_of, username, date, filename))

            # Commit the changes
            self.connection.commit()
            print(f"Training day added for user '{username}' for week {week_of} on date {date} with filename '{filename}'.")

        except Exception as e:
            print(f"An error occurred while adding training day for '{username}': {e}")
            # Only rollback if the connection is still open
            if self.connection:
                self.connection.rollback()
            
    def upsert_training_day(self, week_of, username, date, filename):
        try:
            # Upsert the training day into the training_schedule table
            self.cursor.execute("""
                INSERT INTO training_schedule (week_of, username, date, filename)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (username, date) DO UPDATE
                SET 
                    week_of = EXCLUDED.week_of,
                    filename = EXCLUDED.filename;
            """, (week_of, username, date, filename))

            # Commit the changes
            self.connection.commit()
            print(f"Training day upserted for user '{username}' on date {date} with filename '{filename}'.")

        except Exception as e:
            print(f"An error occurred while upserting training day for '{username}': {e}")
            # Only rollback if the connection is still open
            if self.connection:
                self.connection.rollback()

    # Add the get_training_schedule_by_username method in your SQLHelper class to retrieve tasks for a trainee.
    def get_training_schedule(self, username):
        self.cursor.execute("""
            SELECT week_of, username, date, filename FROM training_schedule
            WHERE username = %s ORDER BY week_of;
        """, (username,))
        return self.cursor.fetchall()

    def get_todays_training_tasks(self):
        today = datetime.now().date()
        self.cursor.execute("""
            SELECT week_of, username, date, filename 
            FROM training_schedule 
            WHERE date = %s;
        """, (today,))
        return self.cursor.fetchall()



    def quit(self):
        self.cursor.close()
        self.connection.close()
        print("PostgreSQL connection is closed.")


        
if __name__ == "__main__":
    SQL = SQLHelper()
    trainees = SQL.get_trainees()
    print(trainees)
    SQL.quit()

