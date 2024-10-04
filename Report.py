import tkinter as tk
from tkinter import ttk
import pandas as pd
import psycopg2
from datetime import datetime, timedelta
import SQLHelper
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

class TaskDistributionApp:
    def __init__(self):
        self.SQLWizard = SQLHelper.SQLHelper()
        # self.root = tk.Tk()
        # self.root.title("Employee Task Distribution")


        # # Task selection
        # self.selected_tasks = tk.StringVar(value="All")
        # self.tasks = self.get_unique_tasks()
        # self.dropdown = ttk.Combobox(self.root, textvariable=self.selected_tasks, values=["All"] + self.tasks, state='normal')
        # self.dropdown.pack(pady=10)

        # # Button to generate report
        # self.report_button = tk.Button(self.root, text="Generate Report", command=self.show_report)
        # self.report_button.pack(pady=5)

        # self.report_text = tk.Text(self.root, wrap=tk.WORD, width=50, height=20)
        # self.report_text.pack(pady=10)

        # self.root.mainloop()

    def fetch_data(self):
        # Establish connection to the PostgreSQL database
        df = self.SQLWizard.get_data_from_db()

        return df.to_dict(orient='records')

    def get_unique_tasks(self):
        # Extract unique tasks from the data
        return sorted(set(item['task'] for item in self.data))

    def show_report(self):
        selected_task = self.selected_tasks.get()
        self.report_text.delete(1.0, tk.END)  # Clear existing text
        report = self.generate_report(selected_task)
        self.report_text.insert(tk.END, report)

    def generate_report(self, selected_task):
        # Create a DataFrame from the data
        df = pd.DataFrame(self.data)

        # Filter the DataFrame based on selected task
        if selected_task != "All":
            df = df[df['task'] == selected_task]

        # Group by employee and task to get the total duration for each
        grouped = df.groupby(['firstname', 'lastname', 'task']).agg({'total_duration': 'sum'}).reset_index()
        
        # Convert total_duration to hours for better readability
        grouped['total_duration'] = grouped['total_duration'].dt.total_seconds() / 3600  # Convert to hours

        # Create a summary for each employee
        employee_summary = grouped.groupby(['firstname', 'lastname']).agg({'total_duration': 'sum'}).reset_index()

        # Format the report
        report_lines = []
        for _, row in employee_summary.iterrows():
            report_lines.append(f"Employee: {row['firstname']} {row['lastname']}, Total Time: {row['total_duration']:.2f} hours")

        # Return the report as a string
        return "\n".join(report_lines)
    
    def export_to_excel(self, data, file_name):
        # Fetch all data from the database table
        
        
        # Export the DataFrame to an Excel file
        data.to_excel(file_name, index=False)
        print(f"Data successfully exported to {file_name}")

    def get_PA_hours(self):
        pass
    


if __name__ == "__main__":
    app = TaskDistributionApp()
    file_name = 'task_summary.xlsx'
    data = app.SQLWizard.get_raw_task_data()
    app.export_to_excel(data, file_name)


