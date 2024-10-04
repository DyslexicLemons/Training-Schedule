import psycopg2
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
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
            self.connection = psycopg2.connect( # to connect manually type in "psql  -h 192.168.4.28 -d iusc -U postgres -p 5432" and for password, type "5678"
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
        raw_trainees = self.cursor.fetchall()

        trainees = {}

        for trainee in raw_trainees:
            username = trainee[2]
            firstname = trainee[0]
            lastname = trainee[1]
            role = trainee[3]

            trainees[username] = {
                'firstname' : firstname,
                'lastname' : lastname,
                'role' : role
            }

        return trainees
    
    def add_employee(self, id, username, first_name, last_name, role, training_status):
        insert_query = """INSERT INTO employees (id, username, firstname, lastname, role, trainingstatus) VALUES (%s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(insert_query, (id,username,first_name,last_name,role, training_status))

        self.connection.commit()
        print(f"Employee {username} added successfully")

    def get_employee(self, username):
        # Use parameterized queries to prevent SQL injection
        self.cursor.execute("SELECT id, firstname, lastname, username, role, trainingstatus FROM employees WHERE username = %s", (username,))
        
        user_data = self.cursor.fetchone()  # Fetch only one record for the given username

        if user_data is None:
            return None  # Return None if the username doesn't exist

        # Map the fetched data to a dictionary
        user = {
            'id': user_data[0],
            'firstname': user_data[1],
            'lastname': user_data[2],
            'username': user_data[3],
            'role': user_data[4],
            'trainingstatus': user_data[5]
        }

        return user

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


#                                                              ---TRAINING SCHEDULE REQUESTS START ----

    def add_task(self, username, firstname, lastname, task, duration, date):
        try:
            # Execute the upsert query (assuming conflict on the username)
            insert_query = """INSERT INTO tasks2 (username, firstname, lastname, task, duration, date) VALUES (%s, %s, %s, %s, %s, %s)"""
            self.cursor.execute(insert_query, (username, firstname, lastname, task, duration, date))

            # Commit the changes
            self.connection.commit()
            # print(f"Task for '{username}' added or updated successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()

    def add_tasks(self, tasks):
        try:
            insert_query = """INSERT INTO tasks2 (username, firstname, lastname, task, duration, date) 
                              VALUES (%s, %s, %s, %s, %s, %s) """
            self.cursor.executemany(insert_query, tasks)
            self.connection.commit()
            # print(f"{len(tasks)} tasks added or updated successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()

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

        
    def visualize_data(self, df, start_date, end_date):
        if df is not None:
            # Ensure total_duration is treated as a timedelta
            df['total_duration'] = pd.to_timedelta(df['total_duration'])

            # Convert total_duration to total hours for easier plotting
            df['total_hours'] = df['total_duration'].dt.total_seconds() / 3600  # Convert seconds to hours

            # Pivot the DataFrame for visualization
            pivot_df = df.pivot_table(
                index=['username', 'firstname', 'lastname'],
                columns='task',
                values='total_hours',
                aggfunc='sum',
                fill_value=0  # Change to 0 instead of timedelta
            )

            # Convert start_date and end_date to just date strings
            start_date_str = pd.to_datetime(start_date).date()
            end_date_str = pd.to_datetime(end_date).date()

            # Plotting
            pivot_df.plot(kind='bar', stacked=True, figsize=(12, 6))
            plt.title(f'Total Duration at Each Task for Each Consultant\nFrom {start_date_str} to {end_date_str}')
            plt.xlabel('Consultants')
            plt.ylabel('Total Duration (in hours)')
            plt.legend(title='Task', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.show()


    def breakdown_employee_tasks(self, data):
        # Convert total_duration to hours for easier aggregation
        data['total_duration'] = data['total_duration'].dt.total_seconds() / 3600  # Convert to hours

        # Group by username and task, then sum total_duration
        breakdown_df = data.groupby(['username', 'task'])['total_duration'].sum().reset_index()

        # Create a summary report
        report = {}
        for _, row in breakdown_df.iterrows():
            username = row['username']
            task = row['task']
            total_time = row['total_duration']

            if username not in report:
                report[username] = {'Total Time': 0, 'Tasks': {}}
            report[username]['Total Time'] += total_time
            report[username]['Tasks'][task] = total_time

        return report
    

    def display_task_distribution(self, data):
        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        # Ensure total_duration is a Timedelta
        df['total_duration'] = pd.to_timedelta(df['total_duration'])

        # Group by employee and task to get the total duration for each
        grouped = df.groupby(['firstname', 'lastname', 'task']).agg({'total_duration': 'sum'}).reset_index()

        # Convert total_duration to hours for better readability
        grouped['total_duration'] = grouped['total_duration'].dt.total_seconds() / 3600  # Convert to hours

        # Create a summary for each employee
        employee_summary = grouped.groupby(['firstname', 'lastname']).agg({'total_duration': 'sum'}).reset_index()

        # Display employee summary
        print("Employee Summary:")
        for _, row in employee_summary.iterrows():
            print(f"{row['firstname']} {row['lastname']}: {row['total_duration']:.2f} hours")

        # Display detailed task breakdown
        print("\nDetailed Task Breakdown:")
        for _, row in grouped.iterrows():
            print(f"{row['firstname']} {row['lastname']} - Task: {row['task']}, Total Time: {row['total_duration']:.2f} hours")
  
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

    def get_training_schedule(self, username):
        self.cursor.execute("""
            SELECT week_of, username, date, filename FROM training_schedule
            WHERE username = %s ORDER BY date;
        """, (username,))
        return self.cursor.fetchall()
    
    def get_all_training_schedules(self):
        self.cursor.execute("""
            SELECT week_of, username, date, filename, task FROM training_schedule;
        """)
        return self.cursor.fetchall()

    def get_training_tasks(self, date):


        self.cursor.execute("""
            SELECT username, date, filename, task 
            FROM training_schedule 
            WHERE date = %s;
        """, (date,))

        tasks = self.cursor.fetchall()

        # Create a dictionary to hold tasks for each trainee
        trainees = {}
        
        for task in tasks:
            username = task[0]
            task_date = task[1]
            filename = task[2]
            task_content = task[3]
            
            # Create a dictionary for each trainee to store task info
            trainees[username] = {
                'date': task_date,
                'filename': filename,
                'task': task_content
            }

        return trainees

    def get_raw_task_data(self):
        # Query to get the aggregated data
        query = """
            SELECT 
                username, 
                firstname, 
                lastname, 
                total_duration,
                date,
                role
            FROM 
                tasks_summary
            ORDER BY 
                username;
        """
        
        # Read data into a DataFrame
        df = pd.read_sql_query(query, self.connection)
        
        return df
    def quit(self):
        self.cursor.close()
        self.connection.close()
        print("PostgreSQL connection is closed.")
    def get_task_usernames(self):
        # Retrieve the current usernames from the database
        self.cursor.execute("SELECT username FROM tasks;")
        # Use a list comprehension to flatten the list of tuples
        return [row[0] for row in self.cursor.fetchall()]
    def insert_role_data(self, data):
        for user in data:
            username = user["username"]
            for assignment in user["scheduledUserMasks"]:
                role = assignment['mask']['name']
                if role in ('Computer Assistant', 'Computer Coordinator', 'PA'):
                    start_date = assignment['startTime']
                    end_date = assignment['endTime']
                    insert_query = """INSERT INTO user_roles (username, role, startDate, endDate) VALUES (%s, %s, %s, %s)"""
                    self.cursor.execute(insert_query, (username, role, start_date, end_date))

                    self.connection.commit()
                    print(f"Employee {username} with role {role} added successfully")

                
    def update_task_table_roles(self):
        update_query = """
        UPDATE tasks2 t
        SET role = ur.role
        FROM user_roles ur
        WHERE t.username = ur.username
        AND (
            -- Task date is between startdate and enddate
            (t.date >= ur.startdate AND t.date <= ur.enddate)
            OR
            -- Task date is after startdate and enddate is null
            (t.date >= ur.startdate AND ur.enddate IS NULL)
        );
        """
        self.cursor.execute(update_query)
        self.connection.commit()

    def create_task_summary_table(self):
        query = """
            INSERT INTO tasks_summary (username, firstname, lastname, total_duration, date, role)
            SELECT 
                username, 
                firstname, 
                lastname, 
                SUM(EXTRACT(EPOCH FROM duration) / 3600) AS total_duration,  -- Convert to hours
                date,
                role
            FROM 
                tasks2
            GROUP BY 
                username, firstname, lastname, date, role;

            """
        self.cursor.execute(query)
        self.connection.commit()



if __name__ == "__main__":

    SQL = SQLHelper()
    table_name = 'tasks'
    file_name = 'Garrettreport.xlsx'
    SQL.export_to_excel(table_name, file_name)
    SQL.quit()

