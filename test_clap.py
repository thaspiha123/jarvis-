import time
import numpy as np
import sounddevice as sd

DEVICE = 1

def callback(indata, frames, time_info, status):
    volume = float(np.sqrt(np.mean(indata ** 2)))
    print(f"Volume: {volume:.4f}")

print("Starting microphone test...")
print("Stay quiet for a few seconds.")
print("Then clap near the microphone.")
print("Press Ctrl+C to stop.")

try:
    with sd.InputStream(
        device=DEVICE,
        samplerate=44100,
        channels=1,
        callback=callback
    ):
        while True:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\nTest stopped.")
except Exception as error:
    print("Error:", error)