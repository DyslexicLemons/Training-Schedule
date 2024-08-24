import tkinter as tk
from tkinter import ttk, messagebox

class TrainingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training App")
        self.root.geometry("800x600")

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

        trainees_list = [("John Doe", "Position A", "50%"), ("Jane Smith", "Position B", "75%")]  # Placeholder
        for trainee in trainees_list:
            trainee_label = tk.Label(main_frame, text=f"{trainee[0]}, {trainee[1]}, {trainee[2]}")
            trainee_label.pack(pady=5)

    def show_trainees(self):
        self.clear_main_content()
        trainees_frame = tk.Frame(self.root)
        trainees_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        trainees_label = tk.Label(trainees_frame, text="Trainees:")
        trainees_label.pack(pady=10)

        
        trainees_list = [("John Doe", "Position A", "50%"), ("Jane Smith", "Position B", "75%")]  # Placeholder
        for trainee in trainees_list:
            trainee_frame = tk.Frame(trainees_frame)
            trainee_frame.pack(pady=5)

            trainee_label = tk.Label(trainee_frame, text=f"{trainee[0]}, {trainee[1]}, {trainee[2]}")
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

        # Placeholder calendar view
        calendar_label = tk.Label(schedules_frame, text="Training Schedules Calendar View")
        calendar_label.pack(pady=10)

    def show_trainee_schedule(self, trainee):
        # Placeholder for pop-up window to show individual trainee's schedule
        messagebox.showinfo("Trainee Schedule", f"Showing training schedule for {trainee[0]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingApp(root)
    root.mainloop()
