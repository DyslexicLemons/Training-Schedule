from datetime import datetime
import SQLHelper
from collections import defaultdict

someSQL = SQLHelper.SQLHelper()

# Sample data
scheduling_data = someSQL.get_all_training_schedules()

# Initialize a nested dictionary to hold the schedules
Trainee_Schedules = defaultdict(lambda: defaultdict(lambda: [[], []]))

# Populate the dictionary
for week, trainee, date, activity in scheduling_data:
    date_str = date.strftime("%m/%d/%Y")  # Format date as string
    Trainee_Schedules[trainee][f"Week {week}"][0].append(date_str)
    Trainee_Schedules[trainee][f"Week {week}"][1].append(activity)

# Convert defaultdict to regular dict for better readability (optional)
Trainee_Schedules = {trainee: dict(weeks) for trainee, weeks in Trainee_Schedules.items()}

# Example output
print(Trainee_Schedules)
