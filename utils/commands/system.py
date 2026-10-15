from pathlib import Path

from commands.apps import open_app
from commands.battery import get_battery
from commands.calculator import calculate
from commands.datetime import get_date, get_day, get_time
from commands.knowledge import answer_question
from commands.system_info import get_cpu_usage, get_ram_usage, get_system_information
from commands.weather import get_weather
from commands.web import open_website, search_web
from memory.memory import get_name


def execute(command):
    command = command.lower().strip()

    # Short conversation replies.
    if "thank you" in command or command == "thanks":
        return "You are welcome."

    if "are you there" in command:
        return "Always listening."

    if "what is my name" in command or "who am i" in command:
        return f"Your name is {get_name()}."

    if "your name" in command or "who are you" in command:
        return "I am JARVIS, your personal desktop assistant."

    # Calculate safely before searching the web.
    response = calculate(command)
    if response:
        return response

    # Search before opening websites.
    response = search_web(command)
    if response:
        return response

    response = open_app(command)
    if response:
        return response

    response = open_website(command)
    if response:
        return response

    # Check system information.
    if "battery" in command or "percentage" in command:
        battery = get_battery()
        if battery is None:
            return "I could not detect a battery on this computer."
        return f"Your battery is {battery} percent."

    if "cpu" in command:
        return get_cpu_usage()

    if "ram" in command or "memory usage" in command:
        return get_ram_usage()

    if "system information" in command:
        return get_system_information()

    if "weather" in command:
        return get_weather()

    if "time" in command:
        return f"The current time is {get_time()}."

    if "date" in command:
        return f"Today's date is {get_date()}."

    if "day" in command:
        return f"Today is {get_day()}."

    if "where am i" in command:
        return f"You are in {Path.cwd()}."

    # Use Wikipedia for normal questions when no local command matches.
    response = answer_question(command)
    if response:
        return response

    return "Sorry, I don't know that command yet."
