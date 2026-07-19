import time
from memory.memory import get_name
from speech.tts import speak
from speech.listen import listen
from commands.system import execute

print(" JARVIS STARTED")

name = get_name()

speak(f"yes {name}?")
time.sleep(0.5)

while True:

    text = listen()

    if not text:
        continue

    # Stop JARVIS
    if "bye jarvis" in text.lower() or "stop jarvis" in text.lower():
        speak(f"Goodbye {name}!")
        break

    # Wake word
    if "jar" in text.lower():

        speak(f"Yes {name}?")

        command = listen()

        if not command:
            speak("I didn't catch that. Please say it again.")
            continue

        response = execute(command)

        if response:
            speak(response)