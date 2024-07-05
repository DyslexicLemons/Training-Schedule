from datetime import datetime
Tasks = ["email", "phone", "chat","Supervisor","Dispatch","Training","lunch"]

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

