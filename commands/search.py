import webbrowser
import urllib.parse


def search_google(query):

    encoded_query = urllib.parse.quote(query)

    url = (
        "https://www.google.com/search?q="
        + encoded_query
    )

    webbrowser.open(url)

    return f"Searching Google for {query}."