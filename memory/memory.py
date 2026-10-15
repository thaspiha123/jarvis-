import os


MEMORY_FILE = os.path.join(
    os.path.dirname(__file__),
    "user_name.txt"
)


def get_name():

    if os.path.exists(MEMORY_FILE):

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            name = file.read().strip()

            if name:
                return name

    name = input(
        "Enter your name: "
    ).strip()

    if not name:
        name = "User"

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(name)

    return name