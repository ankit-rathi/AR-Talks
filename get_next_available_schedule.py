import datetime

# Define the available weekdays and time windows
available_schedule = {
    "Monday": [(8, 0), (12, 0)],   # Example: Monday from 8:00 AM to 12:00 PM
    "Tuesday": [(8, 0), (12, 0)],  # Example: Tuesday from 8:00 AM to 12:00 PM
    "Wednesday": [],               # Example: Wednesday unavailable
    "Thursday": [(8, 0), (12, 0)], # Example: Thursday from 8:00 AM to 12:00 PM
    "Friday": [(8, 0), (12, 0)]     # Example: Friday from 8:00 AM to 12:00 PM
    # Add more days and time windows as needed
}

def find_next_available_datetime():
    # Get the current date and time
    current_datetime = datetime.datetime.now()
    current_weekday = current_datetime.strftime("%A")

    # Check if the current weekday is available
    if current_weekday in available_schedule:
        current_time = current_datetime.time()
        for window_start, window_end in available_schedule[current_weekday]:
            window_start_time = datetime.time(window_start, 0)
            window_end_time = datetime.time(window_end, 0)
            if window_start_time <= current_time <= window_end_time:
                # If current time is within an available window, return the current datetime
                return current_datetime.replace(second=0, microsecond=0)

        # If the current time is outside of all available windows, find the next available window
        for window_start, window_end in available_schedule[current_weekday]:
            window_start_time = datetime.time(window_start, 0)
            if window_start_time > current_time:
                next_available_datetime = current_datetime.replace(hour=window_start, minute=0, second=0, microsecond=0)
                return next_available_datetime

    # If the current weekday is not available or if no available time is found,
    # find the next available day and time
    for i in range(1, 8):  # Check the next 7 days
        next_weekday = datetime.datetime.now() + datetime.timedelta(days=i)
        next_weekday_str = next_weekday.strftime("%A")
        if next_weekday_str in available_schedule:
            next_available_datetime = next_weekday.replace(hour=available_schedule[next_weekday_str][0][0], minute=0, second=0, microsecond=0)
            return next_available_datetime

    # If no available time is found in the next 7 days, return None
    return None

# Test the function
next_available_datetime = find_next_available_datetime()
if next_available_datetime:
    print("Next available date and time:", next_available_datetime)
else:
    print("No available time found in the next 7 days.")


import datetime

# Define the time windows when the system is not available
unavailable_windows = {
    "Monday": [(8, 0), (12, 0)],   # Example: Monday from 8:00 AM to 12:00 PM
    "Tuesday": [(8, 0), (12, 0)],  # Example: Tuesday from 8:00 AM to 12:00 PM
    "Wednesday": [],               # Example: Wednesday unavailable
    "Thursday": [(8, 0), (12, 0)], # Example: Thursday from 8:00 AM to 12:00 PM
    "Friday": [(8, 0), (12, 0)]     # Example: Friday from 8:00 AM to 12:00 PM
    # Add more days and time windows as needed
}

def find_next_available_datetime():
    # Get the current date and time
    current_datetime = datetime.datetime.now()
    current_weekday = current_datetime.strftime("%A")

    # Check if the current time falls within an unavailable window
    if current_weekday in unavailable_windows:
        for window_start, window_end in unavailable_windows[current_weekday]:
            window_start_time = datetime.time(window_start, 0)
            window_end_time = datetime.time(window_end, 0)
            if window_start_time <= current_datetime.time() <= window_end_time:
                # Find the next available time after the current unavailable window
                next_available_datetime = current_datetime.replace(hour=window_end, minute=0, second=0, microsecond=0)
                return next_available_datetime

    # If the current time is outside of all defined unavailable windows,
    # find the next available time slot on the next available weekday
    current_day_index = datetime.datetime.today().weekday()
    for i in range(1, 8):  # Check the next 7 days
        next_day_index = (current_day_index + i) % 7
        next_weekday = datetime.datetime.now() + datetime.timedelta(days=i)
        next_weekday_str = next_weekday.strftime("%A")
        if next_weekday_str in unavailable_windows:
            continue
        else:
            next_available_datetime = next_weekday.replace(hour=0, minute=0, second=0, microsecond=0)
            return next_available_datetime

    # If no available time is found in the next 7 days, return None
    return None

# Test the function
next_available_datetime = find_next_available_datetime()
if next_available_datetime:
    print("Next available date and time:", next_available_datetime)
else:
    print("No available time found in the next 7 days.")

