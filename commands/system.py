import webbrowser
import subprocess


def execute(command):

    if "open youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."

    elif "open google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google."

    elif "open github" in command:
        webbrowser.open("https://github.com")
        return "Opening GitHub."

    elif "open calculator" in command:
        subprocess.Popen("calc.exe")
        return "Opening Calculator."

    elif "open notepad" in command:
        subprocess.Popen("notepad.exe")
        return "Opening Notepad."

    elif "open paint" in command:
        subprocess.Popen("mspaint.exe")
        return "Opening Paint."

    elif "open command prompt" in command:
        subprocess.Popen("cmd.exe")
        return "Opening Command Prompt."

    else:
        return "Sorry, I don't know that command yet."