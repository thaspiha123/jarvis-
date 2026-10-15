import speech_recognition as sr

recognizer = sr.Recognizer()
DEVICE = 1

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 1.2
recognizer.non_speaking_duration = 0.3


def calibrate_microphone():
    """Calibrate once when JARVIS starts."""
    try:
        with sr.Microphone(device_index=DEVICE) as source:
            print("Calibrating microphone...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print(f"Microphone threshold: {recognizer.energy_threshold:.0f}")
    except Exception as error:
        print("Microphone calibration error:", error)


def listen():
    try:
        source = sr.Microphone(device_index=DEVICE)
    except Exception as error:
        print("Microphone error:", error)
        return ""

    with source as source:

        print("Listening...")

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=12
            )

            text = recognizer.recognize_google(audio, language="en-IN")

            print("You:", text)

            return text.lower()

        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            print("I couldn't understand.")
            return ""

        except sr.RequestError:
            print("No internet connection.")
            return ""

        except Exception as e:
            print("Error:", e)
            return ""
