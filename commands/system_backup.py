import webbrowser
import subprocess

from commands.weather import get_weather
from commands.search import search_google
from commands.battery import get_battery
from commands.datetime import get_time, get_date, get_day

from commands.tasks import (
    add_task,
    list_tasks,
    toggle_task,
    delete_task
)


def execute(command):

    command = command.lower().strip()

    print("Command:", command)

    # -------------------------
    # WEBSITES
    # -------------------------

    if "youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."

    elif "google" in command and "search" not in command:
        webbrowser.open("https://google.com")
        return "Opening Google."

    elif "github" in command:
        webbrowser.open("https://github.com")
        return "Opening GitHub."

    elif "chrome" in command:
        subprocess.Popen(
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )
        return "Opening Chrome."

    # -------------------------
    # WINDOWS APPLICATIONS
    # -------------------------

    elif "calculator" in command:
        subprocess.Popen("calc.exe")
        return "Opening Calculator."

    elif "notepad" in command:
        subprocess.Popen("notepad.exe")
        return "Opening Notepad."

    elif "paint" in command:
        subprocess.Popen("mspaint.exe")
        return "Opening Paint."

    elif "command prompt" in command or command == "cmd":
        subprocess.Popen("cmd.exe")
        return "Opening Command Prompt."

    elif "file explorer" in command or command == "explorer":
        subprocess.Popen("explorer.exe")
        return "Opening File Explorer."

    elif "settings" in command:
        subprocess.Popen(
            "start ms-settings:",
            shell=True
        )
        return "Opening Settings."

    # -------------------------
    # DATE AND TIME
    # -------------------------

    elif "time" in command:
        return f"The current time is {get_time()}."

    elif "date" in command:
        return f"Today's date is {get_date()}."

    elif "day" in command:
        return f"Today is {get_day()}."

    # -------------------------
    # BATTERY
    # -------------------------

    elif "battery" in command:
        battery = get_battery()

        return f"Your battery is {battery} percent."

    # -------------------------
    # WEATHER
    # -------------------------

    elif "weather" in command or "temperature" in command:
        return get_weather()

    # -------------------------
    # GOOGLE SEARCH
    # -------------------------

    elif command.startswith("search "):

        query = command.replace(
            "search ",
            "",
            1
        ).strip()

        if query:
            return search_google(query)

        return "What would you like me to search for?"

    # -------------------------
    # TASKS
    # -------------------------

    elif command == "add a task":

        return "Say add task followed by the task name."

    elif command.startswith("add task "):

        title = command.replace(
            "add task ",
            "",
            1
        ).strip()

        if title:
            return add_task(title)

        return "What task would you like me to add?"

    elif command in (
        "show tasks",
        "list tasks",
        "my tasks",
        "what are my tasks"
    ):

        return list_tasks()

    elif command.startswith("complete task "):

        number = command.replace(
            "complete task ",
            "",
            1
        ).strip()

        try:
            return toggle_task(int(number))

        except ValueError:
            return "Please tell me the task number."

    elif command.startswith("delete task "):

        number = command.replace(
            "delete task ",
            "",
            1
        ).strip()

        try:
            return delete_task(int(number))

        except ValueError:
            return "Please tell me the task number."

    # -------------------------
    # DAILY BRIEFING
    # -------------------------

    elif command in (
        "briefing",
        "daily briefing",
        "give me a briefing"
    ):

        tasks_message = list_tasks()

        return (
            f"Good day. "
            f"It is {get_time()}. "
            f"Today is {get_day()}, {get_date()}. "
            f"{tasks_message}"
        )

    # -------------------------
    # FOCUS MODE
    # -------------------------

    elif command in (
        "start focus",
        "start focus mode",
        "focus mode",
        "start a focus session"
    ):

        return (
            "Focus mode started. "
            "Choose one task and work for 25 minutes."
        )

    # -------------------------
    # HELP
    # -------------------------

    elif command in (
        "help",
        "what can you do"
    ):

        return (
            "I can open applications and websites, "
            "tell you the time, date, day, weather "
            "and battery status, search Google, "
            "and manage your tasks."
        )

    # -------------------------
    # UNKNOWN COMMAND
    # -------------------------

    else:
        return "Sorry, I don't know that command yet."