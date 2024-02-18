import datetime

from Backend.main import initialize_database_and_session

db = None
session = None

# Initialize the database and session
db, session = initialize_database_and_session()


# Define the next_sunday function to be used as the default value
def next_sunday():
    today = datetime.date.today()
    days_until_sunday = (6 - today.weekday() + 7) % 7
    return today + datetime.timedelta(days=days_until_sunday)


next_sunday = next_sunday()

DAYS_OF_WEEK = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
