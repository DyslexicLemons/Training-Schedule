from datetime import datetime, timedelta

# Sample data for the training schedule template
start_date = "2024-08-12"

# Sample work schedule
work_schedule = {
    "Monday": {"start_time": "09:00", "end_time": "17:00"},
    "Tuesday": {"start_time": "09:00", "end_time": "17:00"},
    "Wednesday": {"start_time": "09:00", "end_time": "17:00"},
    "Thursday": {"start_time": "09:00", "end_time": "17:00"},
    "Friday": {"start_time": "09:00", "end_time": "17:00"}
}

# Function to get the date of the next specific day of the week
def get_next_day_of_week(start_date, target_day):
    days_ahead = target_day - start_date.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)

# Generate dates for each day in the work schedule starting from the start_date
start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
dates_by_day_of_week = {}
for day in work_schedule:
    day_index = list(work_schedule.keys()).index(day)
    next_date = get_next_day_of_week(start_date_obj, day_index)
    dates_by_day_of_week[day] = [next_date + timedelta(weeks=i) for i in range(5)]

# Sample training schedule with 5 weeks
training_schedule = []
for week in range(1, 6):
    week_schedule = {
        "week": f"Week {week}",
        "assigned_task": f"Task for week {week}",
        "days": []
    }
    for day, times in work_schedule.items():
        for date in dates_by_day_of_week[day]:
            day_schedule = {
                "day_of_week": day,
                "date": date.strftime("%Y-%m-%d"),
                "first_day": date == dates_by_day_of_week[day][0],
                "assigned_task": f"Task for week {week}"
            }
            week_schedule["days"].append(day_schedule)
    training_schedule.append(week_schedule)

# Complete training schedule template
training_schedule_template = {
    "start_date": start_date,
    "work_schedule": work_schedule,
    "training_schedule": training_schedule
}

# Print the training schedule template
import pprint
pprint.pprint(training_schedule_template)


##########################################################################################################




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