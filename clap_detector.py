import sounddevice as sd
import numpy as np
import time

DEVICE = 1
THRESHOLD = 0.06

# Minimum time between two detections
CLAP_COOLDOWN = 0.25

# Maximum time allowed between clap 1 and clap 2
DOUBLE_CLAP_WINDOW = 1.0

last_clap_time = 0
first_clap_time = 0
clap_count = 0


def audio_callback(indata, frames, time_info, status):
    global last_clap_time
    global first_clap_time
    global clap_count

    if status:
        print(status)

    volume = np.sqrt(np.mean(indata ** 2))
    current_time = time.time()

    # Detect a loud sound
    if volume > THRESHOLD:

        # Prevent the same clap from being detected repeatedly
        if current_time - last_clap_time > CLAP_COOLDOWN:

            last_clap_time = current_time

            # First clap
            if clap_count == 0:
                clap_count = 1
                first_clap_time = current_time

                print("Clap 1 detected!")

            # Second clap
            elif clap_count == 1:

                # Check if second clap came soon enough
                if current_time - first_clap_time <= DOUBLE_CLAP_WINDOW:

                    print("DOUBLE CLAP DETECTED!")
                    print("Jarvis waking up...")

                    clap_count = 0

                else:
                    # Too slow — treat this as a new first clap
                    clap_count = 1
                    first_clap_time = current_time

                    print("New clap sequence started.")


print("Using device:", DEVICE)
print("Jarvis clap detector is ready.")
print("Clap TWO times to wake Jarvis.")

with sd.InputStream(
    device=DEVICE,
    samplerate=44100,
    channels=1,
    callback=audio_callback
):
    while True:
        time.sleep(0.1)