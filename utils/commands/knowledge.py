from urllib.parse import quote

import requests


last_topic = ""


def answer_question(command):
    global last_topic

    question_starts = ("who ", "what ", "when ", "where ", "why ", "how ", "explain ", "tell me about ")
    if not command.startswith(question_starts):
        return None

    topic = clean_topic(command)
    if not topic:
        return None

    try:
        title = find_article(topic)
        if not title:
            return "I could not find a clear answer for that."

        response = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title)}",
            headers={"User-Agent": "JarvisStudentProject/1.0"},
            timeout=8,
        )
        response.raise_for_status()
        summary = response.json().get("extract", "")

        if not summary:
            return "I could not find a clear answer for that."

        last_topic = title
        return short_answer(summary)
    except requests.RequestException as error:
        print("Knowledge request error:", error)
        return "I could not reach Wikipedia. Please check your internet connection."
    except ValueError as error:
        print("Knowledge data error:", error)
        return "I could not find a clear answer for that."


def find_article(topic):
    response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "list": "search",
            "srsearch": topic,
            "srlimit": 1,
            "format": "json",
        },
        headers={"User-Agent": "JarvisStudentProject/1.0"},
        timeout=8,
    )
    response.raise_for_status()
    results = response.json().get("query", {}).get("search", [])
    return results[0]["title"] if results else ""


def short_answer(summary):
    sentences = summary.split(". ")
    answer = ". ".join(sentences[:2]).strip()
    if answer and answer[-1] not in ".!?":
        answer += "."
    return answer


def clean_topic(command):
    if any(word in command for word in (" he ", " she ", " it ", " they ")) and last_topic:
        return last_topic

    for phrase in ("who is ", "what is ", "what are ", "explain ", "tell me about "):
        if command.startswith(phrase):
            return command.replace(phrase, "", 1).strip()

    return command.strip()
