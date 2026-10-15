import webbrowser
from urllib.parse import quote_plus


def open_website(command):
    sites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "github": "https://github.com",
        "whatsapp": "https://web.whatsapp.com",
    }

    for name, url in sites.items():
        if f"open {name}" in command or command == name:
            webbrowser.open(url)
            return f"Opening {name.title()}."

    return None


def search_web(command):
    if "search youtube for" in command:
        query = command.replace("search youtube for", "").strip()
        if query:
            webbrowser.open(f"https://www.youtube.com/results?search_query={quote_plus(query)}")
            return f"Searching YouTube for {query}."

    if "search google for" in command:
        query = command.replace("search google for", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={quote_plus(query)}")
            return f"Searching Google for {query}."

    if command.startswith("search "):
        query = command.replace("search", "", 1).strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={quote_plus(query)}")
            return f"Searching Google for {query}."

    return None
