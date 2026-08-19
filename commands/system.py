import webbrowser
import subprocess
from commands.weather import get_weather
from commands.search import search_google
from commands.battery import get_battery
from commands.datetime import get_time, get_date, get_day


def execute(command):

    command = command.lower()

    # Websites
    if "youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."

    elif "google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google."

    elif "github" in command:
        webbrowser.open("https://github.com")
        return "Opening GitHub."

    # Windows Apps
    elif "calculator" in command:
        subprocess.Popen("calc.exe")
        return "Opening Calculator."

    elif "notepad" in command:
        subprocess.Popen("notepad.exe")
        return "Opening Notepad."

    elif "paint" in command:
        subprocess.Popen("mspaint.exe")
        return "Opening Paint."

    elif "command prompt" in command or "cmd" in command:
        subprocess.Popen("cmd.exe")
        return "Opening Command Prompt."

    # Date & Time
    elif "time" in command:
        return f"The current time is {get_time()}"

    elif "date" in command:
        return f"Today's date is {get_date()}"

    elif "day" in command:
        return f"Today is {get_day()}"

    elif "battery" in command:
     battery = get_battery()
     return f"Your battery is {battery} percent."

    elif "search" in command:
     query = command.replace("search", "").strip()

     if query:
        return search_google(query)

        return "What would you like me to search for?"
     elif "weather" in command:
      return get_weather()
    else:
        return "Sorry, I don't know that command yet."