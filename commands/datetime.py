from datetime import datetime


def get_time():
    current_time = datetime.now()
    return current_time.strftime("%I:%M %p")


def get_date():
    current_date = datetime.now()
    return current_date.strftime("%d %B %Y")


def get_day():
    current_day = datetime.now()
    return current_day.strftime("%A")