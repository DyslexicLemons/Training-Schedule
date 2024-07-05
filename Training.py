from Employees import Trainee 
from Schedule import Date



class TrainingCalendar:
    """
    Training Schedule data type for new Consultants until starting shifts
    """
    def __init__(self):
        self.week1 = []
        self.week2 = []
        self.week3 = []
        self.week4 = []
        self.week5 = []


    def create_training_calendar(trainee:Trainee, StartDate: Date):
        """
        Generates the Training Calendar
        """


