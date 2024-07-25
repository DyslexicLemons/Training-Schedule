from datetime import datetime
Tasks = ["email", "phone", "chat","Supervisor","Dispatch","Training","lunch"]
SQL_training_schedule = {}
training_template = [

    ["First Day (onboarding)","Canvas Week 1 Training"],
    ["Canvas Week 2 Training" "Canvas Week 3 Training"],
    ["Emails"],
    ["Chat Shadowing", "Chat coaching"],
    ["Call Shadowing", "Call Coaching"]

    ]

# TODO Implement the layout of what a day of training looks like
class DaySchedule:
    """
    Datatype that shows clock-in/clock-out and assigned tasks for single shift
    """
    def __init__(self, start_time: int, end_time: int, task_schedule):
        self.start_time = start_time
        self.end_time = end_time
        self.task_schedule = task_schedule


class WeekSchedule:
    """
    a list of DaySchedules for an employee's week
    """
    def __init__(self, day_schedules_list):
        self.day_schedules_list = day_schedules_list


class Task:
    """
    Data type for task assignments during a shift
    """
    def __init__(self, start_time:int, end_time:int, task_type):
        self.start_time = start_time
        self.end_time = end_time
        self.task_type = task_type

def get_schedules():
    Schedule_data_html = "schedule data from HTML file"
def create_Training_Schedule(trainee, start_day: datetime, week_schedule):
    curr_training_day = start_day
    SQL_training_schedule.update(curr_training_day,trainee)

    num_Of_Training_weeks = 5
 
    SQL_training_schedule.update(curr_training_day,trainee,)


