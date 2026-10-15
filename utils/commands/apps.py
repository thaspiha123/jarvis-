import os
import subprocess
import webbrowser
from pathlib import Path


def open_app(command):
    apps = {
        "calculator": "calc.exe",
        "notepad": "notepad.exe",
        "paint": "mspaint.exe",
        "file explorer": "explorer.exe",
        "explorer": "explorer.exe",
    }

    folders = {
        "downloads": Path.home() / "Downloads",
        "documents": Path.home() / "Documents",
        "desktop": Path.home() / "Desktop",
    }

    for name, folder in folders.items():
        if f"open {name}" in command:
            try:
                os.startfile(folder)
                return f"Opening {name}."
            except OSError:
                return f"I could not open {name}."

    for name, program in apps.items():
        if name in command:
            try:
                subprocess.Popen(program)
                return f"Opening {name}."
            except OSError:
                return f"I could not open {name}."

    if "settings" in command:
        try:
            os.startfile("ms-settings:")
            return "Opening Settings."
        except OSError:
            return "I could not open Settings."

    if "chrome" in command:
        chrome_paths = [
            Path(os.environ.get("PROGRAMFILES", "")) / "Google/Chrome/Application/chrome.exe",
            Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Google/Chrome/Application/chrome.exe",
        ]
        for path in chrome_paths:
            if path.is_file():
                subprocess.Popen([str(path)])
                return "Opening Chrome."

        webbrowser.open("https://www.google.com")
        return "Chrome was not found, so I opened your default browser."

    if "take a screenshot" in command or "take screenshot" in command:
        return take_screenshot()

    if "lock my computer" in command or "lock computer" in command:
        try:
            import ctypes
            ctypes.windll.user32.LockWorkStation()
            return "Locking your computer."
        except Exception:
            return "I could not lock the computer."

    return None


def take_screenshot():
    picture = Path.home() / "Pictures" / "jarvis-screenshot.png"
    script = (
        "Add-Type -AssemblyName System.Windows.Forms; "
        "Add-Type -AssemblyName System.Drawing; "
        "$screen = [System.Windows.Forms.SystemInformation]::VirtualScreen; "
        "$image = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height); "
        "$graphics = [System.Drawing.Graphics]::FromImage($image); "
        "$graphics.CopyFromScreen($screen.X, $screen.Y, 0, 0, $image.Size); "
        f"$image.Save('{picture}'); $graphics.Dispose(); $image.Dispose()"
    )

    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            check=True,
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        return "Screenshot saved in your Pictures folder."
    except Exception:
        return "I could not take the screenshot."
