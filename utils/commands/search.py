import webbrowser


def search_google(query):
    webbrowser.open(
        f"https://www.google.com/search?q={query}"
    )

    return f"Searching Google for {query}."