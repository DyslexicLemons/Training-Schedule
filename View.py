import tkinter as tk
from tkinter import ttk, messagebox
import SQLHelper
from datetime import datetime, timedelta
from collections import defaultdict
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
        schedule_frame = tk.Frame(self.root)
        schedule_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        schedules_frame = tk.Frame(self.root)
        schedules_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Dropdown for selecting trainee
        trainee_label = tk.Label(schedules_frame, text="Select Trainee:")
        trainee_label.pack(pady=10)

        trainees_list = self.SQL.get_trainees()
        trainee_names = [f"{trainee[0]} {trainee[1]} ({trainee[2]})" for trainee in trainees_list]
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
        print(selected)
        if not selected:
            return
        
        print(selected)
        username = selected.split()[2]  # Assuming username is the first part
        print(username)
        cleaned_username = username.strip("()")

        # Convert defaultdict to regular dict for better readability (optional)
        trainee_scheduling_data = self.SQL.get_training_schedule(cleaned_username)

        if not trainee_scheduling_data:
            self.no_tasks_interface()
        else:
            # Initialize a nested dictionary to hold the schedules
            Trainee_Schedules = defaultdict(lambda: defaultdict(lambda: [[], []]))

            # Populate the dictionary
            trainee_scheduling_data = self.SQL.get_all_training_schedules()
            for week, trainee, date, activity in trainee_scheduling_data:
                date_str = date.strftime("%m/%d/%Y")  # Format date as string
                Trainee_Schedules[trainee][f"Week {week}"][0].append(date_str)
                Trainee_Schedules[trainee][f"Week {week}"][1].append(activity)

            # Convert defaultdict to regular dict for better readability (optional)
            Trainee_Schedules = {trainee: dict(weeks) for trainee, weeks in Trainee_Schedules.items()}

            schedule = Trainee_Schedules[cleaned_username]

            self.show_training_calendar(schedule)

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
                self.SQL.add_training_day(week, self.selected_trainee.get().split()[2], task_date.strftime("%Y-%m-%d"), filename)

        # For weeks 4 and 5
        for week, filename, num_tasks in [(4, "ChatTraining", 2), (5, "CallTraining", 2)]:
            for day in range(num_tasks):
                task_date = start_date + timedelta(days=(3 * 5) + day)  # Start from the end of week 3
                self.SQL.add_training_day(week, self.selected_trainee.get().split()[2], task_date.strftime("%Y-%m-%d"), filename)

        messagebox.showinfo("Success", "Training schedule created from template.")

    def show_training_calendar(self, trainee_scheduling_data):
        self.clear_main_content()
        # Create a canvas and scrollbar for the calendar view

        calendar_canvas = tk.Canvas(self.root)
        calendar_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=calendar_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Create a frame inside the canvas to hold the calendar
        calendar_frame = tk.Frame(calendar_canvas)
        
        # Configure the canvas to scroll with the scrollbar
        calendar_canvas.create_window((0, 0), window=calendar_frame, anchor="nw")
        calendar_canvas.configure(yscrollcommand=scrollbar.set)

        # Create a header for the calendar
        header_label = tk.Label(calendar_frame, text="Scott's Training Calendar", font=("Arial", 16))
        header_label.pack(pady=10)

        # Create a calendar for the current month
        self.display_trainee_calendar(calendar_frame, trainee_scheduling_data)

        # Update the scroll region
        calendar_frame.update_idletasks()
        calendar_canvas.config(scrollregion=calendar_canvas.bbox("all"))

        # Bind mouse scroll to work with the canvas
        calendar_frame.bind("<Configure>", lambda e: calendar_canvas.config(scrollregion=calendar_canvas.bbox("all")))
        calendar_canvas.bind_all("<MouseWheel>", lambda event: calendar_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))


    def show_test_calendar_view(self):
        self.clear_main_content()

        
        # Create a canvas and scrollbar for the calendar view
        calendar_canvas = tk.Canvas(self.root)
        calendar_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=calendar_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Create a frame inside the canvas to hold the calendar
        calendar_frame = tk.Frame(calendar_canvas)
        
        # Configure the canvas to scroll with the scrollbar
        calendar_canvas.create_window((0, 0), window=calendar_frame, anchor="nw")
        calendar_canvas.configure(yscrollcommand=scrollbar.set)

        # Create a header for the calendar
        header_label = tk.Label(calendar_frame, text="Test Calendar View", font=("Arial", 16))
        header_label.pack(pady=10)

        # Create a calendar for the current month
        self.display_trainee_calendar(calendar_frame)

        # Update the scroll region
        calendar_frame.update_idletasks()
        calendar_canvas.config(scrollregion=calendar_canvas.bbox("all"))

        # Bind mouse scroll to work with the canvas
        calendar_frame.bind("<Configure>", lambda e: calendar_canvas.config(scrollregion=calendar_canvas.bbox("all")))
        calendar_canvas.bind_all("<MouseWheel>", lambda event: calendar_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))



    def display_trainee_calendar(self, parent, trainee_scheduling_data):
        print('hello')


        # Assuming 'schedule' is your dictionary
        sorted_weeks = sorted(trainee_scheduling_data.keys(), key=lambda x: int(x.split()[1]))

        for week in sorted_weeks:
            data = trainee_scheduling_data[week]
            
            # Week Label
            week_label = tk.Label(parent, text=week, font=("Arial", 12, "bold"), anchor="w")
            week_label.pack(pady=5, padx=5)

            # Dates Row
            date_frame = tk.Frame(parent)
            date_frame.pack(fill=tk.X)
            for date in data[0]:
                date_label = tk.Label(date_frame, text=date, width=14, height=1, relief="flat")
                date_label.pack(side=tk.LEFT, padx=5, pady=1)

            # Activity Row
            activity_frame = tk.Frame(parent)
            activity_frame.pack(fill=tk.X)
            for activity in data[1]:
                activity_label = tk.Label(activity_frame, text=activity, width=14, height=2, relief="flat", wraplength=100, anchor='center')
                activity_label.pack(side=tk.LEFT, padx=5, pady=1)



    def show_trainee_schedule(self, trainee):
        # Placeholder for pop-up window to show individual trainee's schedule
        messagebox.showinfo("Trainee Schedule", f"Showing training schedule for {trainee[0]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingApp(root)
    root.mainloop()
