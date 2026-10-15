import sounddevice as sd
import numpy as np
import time
import threading


DEVICE = 1

THRESHOLD = 0.06

CLAP_COOLDOWN = 0.25

DOUBLE_CLAP_WINDOW = 1.0


def wait_for_clap():

    first_clap_time = None
    last_clap_time = 0

    clap_detected = threading.Event()

    print("Jarvis is sleeping.")
    print("Waiting for double clap...")

    def audio_callback(indata, frames, time_info, status):

        nonlocal first_clap_time
        nonlocal last_clap_time

        if status:
            print(status)

        volume = np.sqrt(np.mean(indata ** 2))

        current_time = time.time()

        # Ignore normal background noise
        if volume <= THRESHOLD:
            return

        # Prevent one clap from being detected multiple times
        if current_time - last_clap_time < CLAP_COOLDOWN:
            return

        last_clap_time = current_time

        # First clap
        if first_clap_time is None:

            first_clap_time = current_time

            print("Clap 1 detected!")

            return

        # Time between first and second clap
        time_between_claps = (
            current_time - first_clap_time
        )

        # Second clap within allowed window
        if time_between_claps <= DOUBLE_CLAP_WINDOW:

            print("DOUBLE CLAP DETECTED!")
            print("Jarvis waking up...")

            clap_detected.set()

        else:

            print("New clap sequence started.")

            first_clap_time = current_time

    # -------------------------------------------------
    # START MICROPHONE
    # -------------------------------------------------

    try:

        with sd.InputStream(
            device=DEVICE,
            samplerate=44100,
            channels=1,
            callback=audio_callback
        ):

            # Keep microphone active until
            # double clap is detected
            while not clap_detected.is_set():

                time.sleep(0.05)

    except Exception as e:

        print("Clap detector error:", e)

        return False

    return True


# -----------------------------------------------------
# TEST
# -----------------------------------------------------

if __name__ == "__main__":

    wait_for_clap()

    print()
    print("Double clap test completed successfully.")