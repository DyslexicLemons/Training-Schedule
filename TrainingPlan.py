
from Schedule import Date
import TrainingScheduleMessages

from datetime import datetime,timedelta,date

import os


SupervisorsEmail = "super@iu.edu"
QATEmail = "scqat@iu.edu"
TrainingEmail = "sctrain@iu.edu"

Onpoint_schedule = {
    'Sunday' : 'albeach',
    'Monday' : 'lruizdom',
    'Tuesday' : 'eljbake',
    'Wednesday' : 'ashsteel',
    'Thursdat' : 'jowamajo',
    'Friday' : 'lruizdom',
    'Saturday' : 'Elijbake'
}

class TrainingEmailGenerator:
    def __init__(self):
        self.training_date =  datetime.today()+timedelta(days=1)

    # TODO Needs further implementation
    # * Remove save_email function call and put it in a Main function somewhere
    # * Implement styling and formatting functionality
    # * 
    def first_day_email(self,consult ):
        """
        Writes First Day Email

        Parameters:
        training_consultants (list): list of training consultants for that day
        """
        file_path = 'TrainingScheduleMessages/FirstDayEmail.txt'
        

        with open(file_path,'r') as file: # Reads existing email template so it can be modified.
            email_draft = file.read()
            
        email_draft += consult.username
        email_draft += self.training_day.weekday + self.training_day.strftime('%Y-%m-%d')
        email_draft += OnPointSchedule[self.training_day.weekday]

        self.save_email(email_draft) # Writes email draft to TrainingScheduleMessages as a new file.


    def save_email(self, email_draft):
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
