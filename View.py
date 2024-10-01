import tkinter as tk
from tkinter import ttk, messagebox
import SQLHelper
from datetime import datetime, timedelta
from collections import defaultdict
import PIEHelper
import calendar
from tkhtmlview import HTMLLabel
from tkcalendar import DateEntry
from tkinter import messagebox, scrolledtext
import os

class TrainingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training App")
        self.root.geometry("800x600")
        self.SQL = SQLHelper.SQLHelper()
        # self.PIE_data = PIEHelper.get_pie_data()

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

        today = datetime.now().strftime("%m-%d-%y")

        # # Training Plan Section
        # training_plan_label = tk.Label(main_frame, text="Today's Training Plan:")
        # training_plan_label.pack(pady=10)
        training_plan = self.get_training_plan(today)  # Placeholder
        # training_plan_display = tk.Label(main_frame, text=training_plan)
        # training_plan_display.pack(pady=10)

        if training_plan == "No file found.":        
            create_training_plan_button = tk.Button(main_frame, text="Create Training Plan", command=lambda: self.create_training_plan(today))
            create_training_plan_button.pack(pady=10)

        # Trainees Section
        trainees_label = tk.Label(main_frame, text="Trainees:")
        trainees_label.pack(pady=10)

        trainees_list = self.SQL.get_trainees()  # This should return a dictionary of trainees
        todays_tasks = self.SQL.get_training_tasks(today)  # This should return tasks for today

        progress_chart = {
            'Canvas Training Week 1': '10%',
            'Canvas Training Week 2': '20%',
            'Canvas Training Week 3': '30%',
            'Call Coaching': '80%',
            'Chat shadowing': '60%'
        }

        for username, trainee_info in trainees_list.items():  # Loop over the dictionary of trainees
            firstname = trainee_info['firstname']
            lastname = trainee_info['lastname']
            task = todays_tasks.get(username, {}).get('task', 'Unavailable')
            progress = progress_chart.get(task, '0%')
            
            # Convert progress to integer
            progress_value = int(progress.strip('%'))
            
            # Display trainee information
            trainee_label = tk.Label(main_frame, text=f"{firstname} {lastname} ({username}) - {task}")
            trainee_label.pack(pady=5)

            # Create a completion bar
            self.create_completion_bar(main_frame, progress_value)

    def create_completion_bar(self, parent, percentage):
        # Create a frame to hold the progress bar
        bar_frame = tk.Frame(parent)
        bar_frame.pack(pady=5, padx=10, fill=tk.X)

        # Create a canvas to represent the progress bar
        canvas_width = 200
        canvas_height = 20
        canvas = tk.Canvas(bar_frame, width=canvas_width, height=canvas_height)
        canvas.pack()

        # Calculate the fill width based on the percentage
        fill_width = int((percentage / 100) * canvas_width)

        # Get the color based on the percentage (gradient from red to green)
        color = self.get_color_gradient(percentage)

        # Draw the rectangle representing the progress bar
        canvas.create_rectangle(0, 0, fill_width, canvas_height, fill=color)

        # Display the percentage in the center of the bar
        canvas.create_text(canvas_width // 2, canvas_height // 2, text=f"{percentage}%", fill="black")

    def get_color_gradient(self, percentage):
        """Return a color gradient based on the percentage.
        Starts at red (low %) and transitions to green (high %)."""
        red = int(255 * (1 - (percentage / 100)))  # Red decreases as percentage increases
        green = int(255 * (percentage / 100))      # Green increases as percentage increases
        return f'#{red:02x}{green:02x}00'


    def show_trainees(self):
        # Clear the main content area before displaying new content
        self.clear_main_content()

        # Create a frame to hold trainee information
        trainees_frame = tk.Frame(self.root)
        trainees_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Add a label for "Trainees"
        trainees_label = tk.Label(trainees_frame, text="Trainees:")
        trainees_label.pack(pady=10)

        # Get the list of trainees from the database
        trainees_list = self.SQL.get_trainees()  # This should return a dictionary of trainees

        # Loop through the dictionary of trainees
        for username, trainee_info in trainees_list.items():
            # Create a frame for each trainee's info
            trainee_frame = tk.Frame(trainees_frame)
            trainee_frame.pack(pady=5)

            # Display trainee's name and role
            trainee_label = tk.Label(
                trainee_frame, 
                text=f"{trainee_info['firstname']} {trainee_info['lastname']}, {trainee_info['role']}, 50%"
            )
            trainee_label.pack(side=tk.LEFT)

            # Add a button to view the training schedule for the trainee
            view_schedule_button = tk.Button(
                trainee_frame, 
                text="View Training Schedule", 
                command=lambda t=username: self.show_trainee_schedule(t)
            )
            view_schedule_button.pack(side=tk.RIGHT)


    def show_training_plans(self, date=datetime.now().strftime("%m-%d-%y")):
        print(date)
        self.clear_main_content()
        plans_frame = tk.Frame(self.root)
        plans_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        date_label = tk.Label(plans_frame, text=f"Training Plan for: {date}")
        date_label.pack(pady=10)

        content = self.get_training_plan(date)

        # Use HTMLLabel from tkhtmlview to render the HTML content
        training_plan_display = HTMLLabel(plans_frame, html=content)
        training_plan_display.pack(pady=10)

        # update_training_plan_button = tk.Button(plans_frame, text="Update Training Plan")
        # update_training_plan_button.pack(pady=10)

        if content == "No training plan available":
                today = datetime.now().date()
                create_training_plan_button = tk.Button(plans_frame, text="Create Training Plan", command=lambda: self.create_training_plan(date))
                create_training_plan_button.pack(pady=10)
        else:
                edit_training_plan_button = tk.Button(plans_frame, text="Edit Training Plan", command = lambda: self.edit_training_plan(date))
                edit_training_plan_button.pack(pady=10)


        # Convert string back to datetime object
        current_date = datetime.strptime(date, "%m-%d-%y")

        # Get the date before
        date_before = (current_date - timedelta(days=1)).strftime("%m-%d-%y")

        # Get the date after
        date_after = (current_date + timedelta(days=1)).strftime("%m-%d-%y")

        # Add buttons to navigate dates (not implemented)
        prev_day_button = tk.Button(plans_frame, text="< Previous Day", command = lambda:  self.show_training_plans(date_before))
        prev_day_button.pack(side=tk.LEFT, padx=20)

        next_day_button = tk.Button(plans_frame, text="Next Day >", command = lambda:  self.show_training_plans(date_after))
        next_day_button.pack(side=tk.RIGHT, padx=20)


    def get_training_plan(self, date):
        try:
            with open(f"TrainingPlans/TP{date}.html", "r") as file:
                content = file.read()
                print('Content found!')
        except FileNotFoundError:
            print("No file found.")
            content = "No training plan available"

        return content
    def edit_training_plan(self, date):
        self.clear_main_content()

        edit_frame = tk.Frame(self.root)
        edit_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        title_label = tk.Label(edit_frame, text="Edit Training Plan")
        title_label.pack(pady=10)

        # Create a scrolled text area for editing HTML content
        self.text_area = scrolledtext.ScrolledText(edit_frame, wrap=tk.WORD, width=80, height=20)
        self.text_area.pack(padx=10, pady=10)

        # Load the current HTML content into the text area
        content = self.get_training_plan(date)
        self.text_area.insert(tk.END, content)

        # Submit button to save changes
        submit_button = tk.Button(edit_frame, text="Submit", command=lambda: self.save_training_plan(date))
        submit_button.pack(side=tk.LEFT, padx=(10, 5))

        # Delete button to remove the file
        delete_button = tk.Button(edit_frame, text="Delete", command=lambda: self.delete_training_plan(date))
        delete_button.pack(side=tk.LEFT, padx=(5, 10))

    def save_training_plan(self, date):
        # Save the content from the text area back to the file
        with open(f"TrainingPlans/TP{date}.html", "w") as file:
            content = self.text_area.get("1.0", tk.END)  # Get all text from the text area
            file.write(content)
        
        messagebox.showinfo("Success", "Training plan updated successfully!")
        self.show_training_plans(date)  # Reload training plans view

    def delete_training_plan(self, date):
        if os.path.exists(f"TrainingPlans/TP{date}.html"):
            os.remove(f"TrainingPlans/TP{date}.html")
            messagebox.showinfo("Success", "Training plan deleted successfully!")
            self.show_training_plans(date)  # Reload training plans view
        else:
            messagebox.showerror("Error", "File does not exist.")
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
        trainee_names = [f"{trainee_info['firstname']} {trainee_info['lastname']} ({username})" for username, trainee_info in trainees_list.items()]
        selected_trainee = tk.StringVar()
        
        trainee_dropdown = ttk.Combobox(schedules_frame, textvariable=selected_trainee, values=trainee_names)
        trainee_dropdown.pack(pady=10)
        
        view_schedule_button = tk.Button(schedules_frame, text="View Schedule", command=lambda: self.display_trainee_schedule(selected_trainee.get().split('(')[-1].strip(')')))
        view_schedule_button.pack(pady=10)

        # Placeholder for showing training schedule
        self.schedule_display_frame = tk.Frame(schedules_frame)
        self.schedule_display_frame.pack(pady=10)

    def display_trainee_schedule(self, trainee):
        # Clear previous schedule display
        for widget in self.schedule_display_frame.winfo_children():
            widget.destroy()


        username = trainee  # Assuming username is the first part
        print(trainee)


        # Convert defaultdict to regular dict for better readability (optional)
        trainee_scheduling_data = self.SQL.get_training_schedule(username)

        if not trainee_scheduling_data:
            self.no_tasks_interface(username)
        else:
            # Initialize a nested dictionary to hold the schedules
            Trainee_Schedules = defaultdict(lambda: defaultdict(lambda: [[], []]))

            # Populate the dictionary
            trainee_scheduling_data = self.SQL.get_all_training_schedules()
            for week, trainee, date, filename, task in trainee_scheduling_data:
                date_str = date.strftime("%m-%d-%y")  # Format date as string
                Trainee_Schedules[trainee][f"Week {week}"][0].append(date_str)
                Trainee_Schedules[trainee][f"Week {week}"][1].append(task)

            # Convert defaultdict to regular dict for better readability (optional)
            Trainee_Schedules = {trainee: dict(weeks) for trainee, weeks in Trainee_Schedules.items()}

            schedule = Trainee_Schedules[username]

            self.show_training_calendar(schedule, username)

    def no_tasks_interface(self, trainee):
        message = tk.Label(self.schedule_display_frame, text="No training items found.")
        message.pack(pady=10)

        create_from_scratch_button = tk.Button(self.schedule_display_frame, text="Create New Training Schedule from Scratch")
        create_from_scratch_button.pack(pady=5)

        start_date_label = tk.Label(self.schedule_display_frame, text="Enter Start Date (YYYY-MM-DD):")
        start_date_label.pack(pady=5)

        self.start_date_entry = tk.Entry(self.schedule_display_frame)
        self.start_date_entry.pack(pady=5)

        create_from_template_button = tk.Button(self.schedule_display_frame, text="Create Training Schedule from Template", command=lambda: self.create_from_template(trainee))
        create_from_template_button.pack(pady=5)

    def create_from_template(self, trainee):
        start_date_str = self.start_date_entry.get()
        if not start_date_str:
            messagebox.showwarning("Warning", "Please enter a start date.")
            return

        # Convert start date to a datetime object

        start_date = datetime.strptime(start_date_str, "%m-%d-%y")

        for week in range(1, 6):
            for day in range(5):  # 5 tasks per week
                task_date = start_date + timedelta(days=(week - 1) * 5 + day)
                filename = f"CanvasWeek{week}"
                self.SQL.add_training_day(week, trainee, task_date.strftime("%m-%d-%y"), filename)

        # For weeks 4 and 5
        for week, filename, num_tasks in [(4, "ChatTraining", 2), (5, "CallTraining", 2)]:
            for day in range(num_tasks):
                task_date = start_date + timedelta(days=(3 * 5) + day)  # Start from the end of week 3
                self.SQL.add_training_day(week, trainee, task_date.strftime("%m-%d-%y"), filename)

        messagebox.showinfo("Success", "Training schedule created from template.")

    def create_training_plan(self, date=datetime.now().date()):
        # Clear the main content area
        self.clear_main_content()

        # Create a frame to hold the training plan
        plan_frame = tk.Frame(self.root)
        plan_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.task_entries = {}

        # Fetch today's training tasks (returns a dictionary with usernames as keys)
        todays_tasks = self.SQL.get_training_tasks(date)

        for username, task_info in todays_tasks.items():
            trainee = self.SQL.get_employee(username)
            trainee_frame = tk.Frame(plan_frame)
            trainee_frame.pack(fill=tk.X, pady=5)

            # Display trainee name
            trainee_name = trainee['firstname'] + " " + trainee['lastname'] + f" ({trainee['username']})"
            trainee_label = tk.Label(trainee_frame, text=trainee_name)
            trainee_label.pack(side=tk.LEFT)

            # Load the content from the file
            task_filename = task_info['filename']
            file_path = f"TrainingEmailTemplates/{task_filename}"
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
            except FileNotFoundError:
                content = "File not found."

            # Create a text box for editing the task content
            task_text = tk.Text(trainee_frame, width=60, height=5)
            task_text.insert(tk.END, content)
            task_text.pack(side=tk.LEFT, padx=10)

            # Store the text entry widget in a dictionary using the trainee username
            self.task_entries[username] = task_text

            # Add a remove button for the trainee
            remove_button = tk.Button(trainee_frame, text="-", command=lambda u=username, f=trainee_frame: self.remove_trainee(u, f))
            remove_button.pack(side=tk.RIGHT)

        # Submit button to finalize the training plan
        submit_button = tk.Button(plan_frame, text="Submit", command=lambda: self.submit_training_plan(date))
        submit_button.pack(pady=20)


    def remove_trainee(self, username, frame):
        # Remove trainee's entry from the dictionary and destroy the frame
        if username in self.task_entries:
            del self.task_entries[username]  # Remove the text entry widget from the dictionary
        frame.destroy()

    # def add_trainee(self, task_entries):
    #     trainee_name = self.selected_trainee.get()
    #     if trainee_name and trainee_name not in self.task_entries:
    #         # Add trainee to the plan (create new entry for the task content)
    #         trainee_frame = tk.Frame(self.root)
    #         trainee_frame.pack(fill=tk.X, pady=5)

    #         trainee_label = tk.Label(trainee_frame, text=trainee_name)
    #         trainee_label.pack(side=tk.LEFT)

    #         task_text = tk.Text(trainee_frame, width=60, height=5)
    #         task_text.insert(tk.END, "No task assigned.")
    #         task_text.pack(side=tk.LEFT, padx=10)
    #         self.task_entries[trainee_name] = task_text

    #         remove_button = tk.Button(trainee_frame, text="-", command=lambda t=trainee_name: self.remove_trainee(t, trainee_frame))
    #         remove_button.pack(side=tk.RIGHT)

    def submit_training_plan(self, date):
        # Collect the data from the task entries and display in the training plans view
        final_plan = ""
        for username, task_text in self.task_entries.items():
            try:
                # Make sure the text widget is still valid before trying to get the content
                final_plan += f"Trainee: {username}\nTask:\n{task_text.get('1.0', tk.END)}\n\n"
            except tk.TclError:
                print(f"Warning: Could not retrieve data for {username}. Text widget has been removed.")

        file_name = f"TP{date}.html"
        file_path = f"TrainingPlans/{file_name}"

        # Write content to the file (overwrite if it already exists)
        with open(file_path, 'w') as file:
            file.write(final_plan)

        print(f"Training plan saved as: {file_name}")

        self.show_training_plans(date)



    def show_training_calendar(self, trainee_scheduling_data, username):
        employee = self.SQL.get_employee(username)

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
        header_label = tk.Label(calendar_frame, text=f"{employee['firstname']}'s Training Calendar", font=("Arial", 16))
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
