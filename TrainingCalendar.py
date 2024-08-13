training_schedule_template = {
    'start_date' : '',
    'training_schedule' = {
        'week 1' : "Canvas Week 1 Training",
        'Week 2' : "Canvas Week 2 Training",
        'Week 3' : "Canvas Week 3 Training",
        'Week 4' : "Chat Shadowing/coaching",
        'Week 5' : 'Call Shadowing/Coaching'
    },
    'work_schedule' = {}

}
from Schedule import Date




# TODO Implement a format for what each week will be made up of
"""
Training Schedule data type for new Consultants until starting shifts
"""
class TrainingCalendar:

    def __init__(self):
        pass

    # TODO Generate Training calendar
    def generate_training_calendar(self, trainee, start_date: Date):
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