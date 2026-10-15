import psutil


def get_battery():

    battery = psutil.sensors_battery()

    if battery is None:
        return "unknown"

    return round(battery.percent)