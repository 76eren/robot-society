import random
from datetime import datetime, timedelta

current_time = "2025-01-01 00:00:00.000000+0000"

def get_time():
    global current_time
    current_time = increase_time(current_time)
    return current_time

def increase_time(current_time):
    minutes = random.randint(20, 180)
    current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S.%f%z")
    current_time += timedelta(minutes=minutes)
    return current_time.strftime("%Y-%m-%d %H:%M:%S.%f%z")