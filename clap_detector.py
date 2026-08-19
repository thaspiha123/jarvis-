import sounddevice as sd
import numpy as np
import time

DEVICE = 1
THRESHOLD = 0.06
COOLDOWN = 0.5

last_clap_time = 0


def audio_callback(indata, frames, time_info, status):
    global last_clap_time

    if status:
        print(status)

    volume = np.sqrt(np.mean(indata ** 2))

    print("Volume:", round(float(volume), 4))

    current_time = time.time()

    if volume > THRESHOLD:
        if current_time - last_clap_time > COOLDOWN:
            print("Clap detected!")
            last_clap_time = current_time


print("Using device:", DEVICE)
print("Clap detector is ready.")
print("Clap near the microphone.")

with sd.InputStream(
    device=DEVICE,
    samplerate=44100,
    channels=1,
    callback=audio_callback
):
    while True:
        time.sleep(0.1)