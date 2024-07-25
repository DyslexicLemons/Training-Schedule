from Employees import Trainee 
from Schedule import Date
Onpoint_schedule = {
    'Sunday' : 'albeach',
    'Monday' : 'lruizdom',
    'Tuesday' : 'eljbake',
    'Wednesday' : 'ashsteel',
    'Thursdat' : 'jowamajo',
    'Friday' : 'lruizdom',
    'Saturday' : 'Elijbake'
}

training_schedule_template = {
    'week 1' : "Canvas Week 1 Training",
    'Week 2' : "Canvas Week 2 Training",
    'Week 3' : "Canvas Week 3 Training",
    'Week 4' : "Chat Shadowing/coaching",
    'Week 5' : 'Call Shadowing/Coaching'
}

# TODO Implement a format for what each week will be made up of
"""
Training Schedule data type for new Consultants until starting shifts
"""
class TrainingCalendar:

    def __init__(self):
        pass

    # TODO Generate Training calendar
    def generate_training_schedule(self, trainee, start_date: Date):
        """
        Generates the Training Calendar (week 1 - week 5)
        """
        pass

    # TODO Access PSQL and update training schedule date to "Absent"
    def absent(self, trainee, day_absent: Date):
        """
        changes day in the calendar to absent
        """

    # TODO access PSQL database with training calendar info and update it accordingly
    def extend(self, trainee):
        """
        Adds extra day to training calendar
        """
        pass

    # TODO Access PSQL database with training calendar and adjust remaining week's activites to the extra task for that week
    def finish_early(self,trainee):
        """
        Moves client's week activites to extra tasks
        """
        pass

    # TODO creates and formats that training plan email. Includes:
    # Get on-point supervisor
    # scheduling trainers to work with trainees
    # adding text based on training day.
    def generate_Training_plan(self,trainee, training_day: Date):
        """
        Generates the training plan email specified day (or today's date if not specified)
        """
        file_path = 'TrainingScheduleMessages/FirstDayEmail.txt'
        

        with open(file_path,'r') as file: # Reads existing email template so it can be modified.
            email_draft = file.read()
            
        email_draft += "potato"
        self.save_email_draft(email_draft) # Writes email draft to TrainingScheduleMessages as a new file.

    def save_email_draft(self,email_draft):
        """
        Saves email draft to /TrainingScheduleMessages

        Parameters:
        email_draft (str): text of the email draft to be saved
        """
        subfolder_path = 'TrainingScheduleMessages'
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

        new_file_name = f'TrainingEmail_{self.training_date.strftime("%Y%m%d")}.txt'
        new_file_path = os.path.join(subfolder_path, new_file_name)
        
        with open(new_file_path, 'w') as new_file:
                new_file.write(email_draft)

        print(f"Modified content saved to '{new_file_path}'")
