import tkinter as tk
from tkinter import ttk, messagebox
import SQLHelper
from datetime import datetime, timedelta
import calendar

class TrainingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training App")
        self.root.geometry("800x600")
        self.SQL = SQLHelper.SQLHelper()

        self.create_menu()
        self.show_main_menu()

    def create_menu(self):
        # Create side menu
        self.menu_frame = tk.Frame(self.root, bg="lightgrey", width=200)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Main Menu Button
        self.main_menu_button = tk.Button(self.menu_frame, text="Main Menu", command=self.show_main_menu)
        self.main_menu_button.pack(fill=tk.X)

        # Trainees Button
        self.trainees_button = tk.Button(self.menu_frame, text="Trainees", command=self.show_trainees)
        self.trainees_button.pack(fill=tk.X)

        # Training Plans Button
        self.training_plans_button = tk.Button(self.menu_frame, text="Training Plans", command=self.show_training_plans)
        self.training_plans_button.pack(fill=tk.X)

        # Training Schedules Button
        self.training_schedules_button = tk.Button(self.menu_frame, text="Training Schedules", command=self.show_training_schedules)
        self.training_schedules_button.pack(fill=tk.X)

        # Test Calendar View Button
        self.test_calendar_view_button = tk.Button(self.menu_frame, text="Test Calendar View", command=self.show_test_calendar_view)
        self.test_calendar_view_button.pack(fill=tk.X)

        # Exit Button
        self.exit_button = tk.Button(self.menu_frame, text="Exit", command=self.root.quit)
        self.exit_button.pack(fill=tk.X)

    def clear_main_content(self):
        # Destroy all widgets in main content area
        for widget in self.root.winfo_children():
            if widget not in [self.menu_frame]:
                widget.destroy()

    def show_main_menu(self):
        self.clear_main_content()
        main_frame = tk.Frame(self.root)
        main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Training Plan Section
        training_plan_label = tk.Label(main_frame, text="Today's Training Plan:")
        training_plan_label.pack(pady=10)
        training_plan = "No training plan"  # Placeholder
        training_plan_display = tk.Label(main_frame, text=training_plan)
        training_plan_display.pack(pady=10)

        create_training_plan_button = tk.Button(main_frame, text="Create Training Plan")
        create_training_plan_button.pack(pady=10)

        # Trainees Section
        trainees_label = tk.Label(main_frame, text="Trainees:")
        trainees_label.pack(pady=10)

        trainees_list = self.SQL.get_trainees()
        todays_tasks = self.SQL.get_todays_training_tasks()

        # Create a dictionary for easy lookup of tasks by username
        task_dict = {task[0]: task[1] for task in todays_tasks}

        for trainee in trainees_list:
            trainee_label = tk.Label(main_frame, text=f"{trainee[0]} {trainee[1]}, {trainee[3]}, 50%")
            trainee_label.pack(pady=5)

            # Get the task for the trainee
            task_filename = task_dict.get(trainee[0], None)
            if task_filename:
                task_label = tk.Label(main_frame, text=f"Today's Task: {task_filename}")
                task_label.pack(pady=5)
            else:
                task_label = tk.Label(main_frame, text="No task assigned today.")
                task_label.pack(pady=5)


    def show_trainees(self):
        self.clear_main_content()
        trainees_frame = tk.Frame(self.root)
        trainees_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        trainees_label = tk.Label(trainees_frame, text="Trainees:")
        trainees_label.pack(pady=10)

        
        trainees_list = self.SQL.get_trainees()
        for trainee in trainees_list:
            trainee_frame = tk.Frame(trainees_frame)
            trainee_frame.pack(pady=5)

            trainee_label = tk.Label(trainee_frame, text=f"{trainee[0]} {trainee[1]}, {trainee[3]}, 50%")
            trainee_label.pack(side=tk.LEFT)

            view_schedule_button = tk.Button(trainee_frame, text="View Training Schedule", command=lambda t=trainee: self.show_trainee_schedule(t))
            view_schedule_button.pack(side=tk.RIGHT)

    def show_training_plans(self):
        self.clear_main_content()
        plans_frame = tk.Frame(self.root)
        plans_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        date_label = tk.Label(plans_frame, text="Today's Date: 2024-08-12")  # Placeholder
        date_label.pack(pady=10)

        training_plan = "No training plan for today"  # Placeholder
        training_plan_display = tk.Label(plans_frame, text=training_plan)
        training_plan_display.pack(pady=10)

        update_training_plan_button = tk.Button(plans_frame, text="Update Training Plan")
        update_training_plan_button.pack(pady=10)

        create_training_plan_button = tk.Button(plans_frame, text="Create Training Plan")
        create_training_plan_button.pack(pady=10)

        # Add buttons to navigate dates (not implemented)
        prev_day_button = tk.Button(plans_frame, text="< Previous Day")
        prev_day_button.pack(side=tk.LEFT, padx=20)

        next_day_button = tk.Button(plans_frame, text="Next Day >")
        next_day_button.pack(side=tk.RIGHT, padx=20)

    def show_training_schedules(self):
        self.clear_main_content()
        schedules_frame = tk.Frame(self.root)
        schedules_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Dropdown for selecting trainee
        trainee_label = tk.Label(schedules_frame, text="Select Trainee:")
        trainee_label.pack(pady=10)

        trainees_list = self.SQL.get_trainees()
        trainee_names = [f"{trainee[0]} {trainee[1]}" for trainee in trainees_list]
        self.selected_trainee = tk.StringVar()
        trainee_dropdown = ttk.Combobox(schedules_frame, textvariable=self.selected_trainee, values=trainee_names)
        trainee_dropdown.pack(pady=10)
        
        view_schedule_button = tk.Button(schedules_frame, text="View Schedule", command=self.display_trainee_schedule)
        view_schedule_button.pack(pady=10)

        # Placeholder for showing training schedule
        self.schedule_display_frame = tk.Frame(schedules_frame)
        self.schedule_display_frame.pack(pady=10)

    def display_trainee_schedule(self):
        # Clear previous schedule display
        for widget in self.schedule_display_frame.winfo_children():
            widget.destroy()

        selected = self.selected_trainee.get()
        if not selected:
            return

        username = selected.split()[0]  # Assuming username is the first part

        training_tasks = self.SQL.get_training_schedule(username)

        if not training_tasks:
            self.no_tasks_interface()
        else:
            self.show_training_calendar(training_tasks)

    def no_tasks_interface(self):
        message = tk.Label(self.schedule_display_frame, text="No training items found.")
        message.pack(pady=10)

        create_from_scratch_button = tk.Button(self.schedule_display_frame, text="Create New Training Schedule from Scratch")
        create_from_scratch_button.pack(pady=5)

        start_date_label = tk.Label(self.schedule_display_frame, text="Enter Start Date (YYYY-MM-DD):")
        start_date_label.pack(pady=5)

        self.start_date_entry = tk.Entry(self.schedule_display_frame)
        self.start_date_entry.pack(pady=5)

        create_from_template_button = tk.Button(self.schedule_display_frame, text="Create Training Schedule from Template", command=self.create_from_template)
        create_from_template_button.pack(pady=5)

    def create_from_template(self):
        start_date_str = self.start_date_entry.get()
        if not start_date_str:
            messagebox.showwarning("Warning", "Please enter a start date.")
            return

        # Convert start date to a datetime object

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

        for week in range(1, 6):
            for day in range(5):  # 5 tasks per week
                task_date = start_date + timedelta(days=(week - 1) * 5 + day)
                filename = f"CanvasWeek{week}"
                self.SQL.add_training_day(week, self.selected_trainee.get().split()[0], task_date.strftime("%Y-%m-%d"), filename)

        # For weeks 4 and 5
        for week, filename, num_tasks in [(4, "ChatTraining", 2), (5, "CallTraining", 2)]:
            for day in range(num_tasks):
                task_date = start_date + timedelta(days=(3 * 5) + day)  # Start from the end of week 3
                self.SQL.add_training_day(week, self.selected_trainee.get().split()[0], task_date.strftime("%Y-%m-%d"), filename)

        messagebox.showinfo("Success", "Training schedule created from template.")

    def show_training_calendar(self, training_tasks):
        # Sort tasks by week
        training_tasks.sort(key=lambda x: x[0])  # Assuming x[0] is week_of

        for task in training_tasks:
            week_of, username, date, filename = task

            # Create a row for the week
            row_frame = tk.Frame(self.schedule_display_frame)
            row_frame.pack(pady=5)

            week_label = tk.Label(row_frame, text=f"Week: {week_of}")
            week_label.pack(side=tk.LEFT)

            # Placeholder for connected boxes
            task_label = tk.Label(row_frame, text=f"{date}: {filename}")
            task_label.pack(side=tk.LEFT, padx=10)

            # You can customize the box appearance here if needed

    def show_test_calendar_view(self):
        self.clear_main_content()
        calendar_frame = tk.Frame(self.root)
        calendar_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create a header for the calendar
        header_label = tk.Label(calendar_frame, text="Test Calendar View", font=("Arial", 16))
        header_label.pack(pady=10)

        # Create a calendar for the current month
        self.create_calendar(calendar_frame)

    def create_calendar(self, parent):
        # Get the current year and month
        import datetime
        now = datetime.datetime.now()
        year = now.year
        month = now.month

        # Create a month calendar
        month_calendar = calendar.monthcalendar(year, month)

        # Create labels for the days of the week
        days_label = tk.Frame(parent)
        days_label.pack()
        days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        for day in days:
            label = tk.Label(days_label, text=day, width=5, font=("Arial", 12))
            label.pack(side=tk.LEFT)

        # Create a grid for the days
        for week in month_calendar:
            week_frame = tk.Frame(parent)
            week_frame.pack()
            for day in week:
                if day == 0:
                    label = tk.Label(week_frame, text='', width=5)
                else:
                    label = tk.Label(week_frame, text=day, width=5, relief='solid')
                label.pack(side=tk.LEFT)





    def show_trainee_schedule(self, trainee):
        # Placeholder for pop-up window to show individual trainee's schedule
        messagebox.showinfo("Trainee Schedule", f"Showing training schedule for {trainee[0]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingApp(root)
    root.mainloop()
