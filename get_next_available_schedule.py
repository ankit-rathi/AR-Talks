import datetime

def find_next_available_time(input_json):
    # Extract values from input JSON
    include_exclude = input_json.get('include_exclude', 'include')
    weekdays = input_json.get('weekdays', [])
    start_time = input_json.get('start_time', '00:00')
    end_time = input_json.get('end_time', '23:59')

    # Convert start_time and end_time to datetime.time objects
    start_hour, start_minute = map(int, start_time.split(':'))
    end_hour, end_minute = map(int, end_time.split(':'))
    start_time_obj = datetime.time(start_hour, start_minute)
    end_time_obj = datetime.time(end_hour, end_minute)

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Find the next available time
    if include_exclude == 'include':
        # Find the next available time for the provided weekdays and time range
        for i in range(7):  # Check the next 7 days
            next_date = current_datetime + datetime.timedelta(days=i)
            next_weekday = next_date.strftime('%a')
            print(next_weekday)
            if next_weekday in weekdays:
                next_available_datetime = datetime.datetime.combine(next_date, start_time_obj)
                if next_available_datetime > current_datetime:
                    return next_available_datetime
    elif include_exclude == 'exclude':
        # Find the next available time excluding the provided weekdays and time range
        for i in range(7):  # Check the next 7 days
            next_date = current_datetime + datetime.timedelta(days=i)
            next_weekday = next_date.strftime('%a')
            if next_weekday in weekdays:
                next_unavailable_datetime = datetime.datetime.combine(next_date, start_time_obj)
                next_available_datetime = datetime.datetime.combine(next_date, end_time_obj)
                if next_unavailable_datetime > current_datetime:
                    return current_datetime
                else:
                    return next_available_datetime

    # If no available time is found in the next 7 days, return None
    return None

# Test the function
input_json = {'include_exclude':'exclude', 'weekdays':['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], 'start_time':'04:00', 'end_time':'06:00'}
next_available_datetime = find_next_available_time(input_json)
if next_available_datetime:
    print("Next available date and time:", next_available_datetime)
else:
    print("No available time found in the next 7 days.")
