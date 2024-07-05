import requests     # Http request library for python
import psycopg2     # PostgreSQL library for Python

consultants = {}
trainers = {}
trainees = {}



class Supervisor:
    def __init__(self, first_name):
        self.first_name = first_name

    def __init__(self, username, first_name, last_name, week_schedule, training_team:bool):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.week_schedule = week_schedule
        self.training_team = training_team

class Consultant:
    def __init__(self, first_name):
        self.first_name=first_name
        
    def __init__(self, username, first_name, last_name, week_schedule, trainer:bool):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.week_schedule = week_schedule
        self.trainer = trainer

class Trainee:
    def __init__(self, username, first_name, last_name, week_schedule, trainer:bool, training_calendar):
        super().__init__(username, first_name, last_name, week_schedule, trainer)
        self.training_calendar = training_calendar





def get_consultants():
    """
    Grabs consultants schedule information using PIE and intitializes them as Consultant or Trainee
    """
    
    new_consultant = Consultant()
    username = ""
    consultants[username] = new_consultant
def get_supervisors():
    """
    Grabs Supervisors schedule information using PIE and intitializes them as Supervisor
    """