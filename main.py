import time
import sounddevice as sd
import numpy as np

from memory.memory import get_name
from speech.tts import speak
from speech.listen import listen
from commands.system import execute


DEVICE = 1
THRESHOLD = 0.02
COOLDOWN = 0.3


print("JARVIS STARTED")

name = get_name()

last_clap_time = 0
clap_detected = False


def detect_clap(indata, frames, time_info, status):
    global last_clap_time
    global clap_detected

    volume = np.sqrt(np.mean(indata ** 2))

    current_time = time.time()

    if volume > THRESHOLD:
        if current_time - last_clap_time > COOLDOWN:
            clap_detected = True
            last_clap_time = current_time


def wait_for_clap():
    global clap_detected

    clap_detected = False

    print("JARVIS is sleeping.")
    print("Waiting for clap...")

    with sd.InputStream(
        device=DEVICE,
        samplerate=44100,
        channels=1,
        callback=detect_clap
    ):
        while not clap_detected:
            time.sleep(0.2)


while True:

    wait_for_clap()

    print("Clap detected!")

    speak(f"Yes {name}?")

    command = listen()

    if not command:
        speak("I didn't catch that. Please say it again.")
        continue

    command = command.lower()

    if "bye jarvis" in command or "stop jarvis" in command:
        speak(f"Goodbye {name}!")
        break

    print("Command:", command)

    response = execute(command)

    if response:
        speak(response)