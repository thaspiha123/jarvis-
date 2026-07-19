import json

FILE = "memory/user_data.json"


def load_data():
    with open(FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_name():
    data = load_data()
    return data["name"]


def add_note(note):
    data = load_data()
    data["notes"].append(note)
    save_data(data)


def get_notes():
    data = load_data()
    return data["notes"]