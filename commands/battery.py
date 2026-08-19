import psutil


def get_battery():
    battery = psutil.sensors_battery()

    if battery is None:
        return "I couldn't detect the battery."

    return battery.percent