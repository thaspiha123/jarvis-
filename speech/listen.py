import speech_recognition as sr


recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.non_speaking_duration = 0.4
recognizer.phrase_threshold = 0.3


def calibrate_microphone():

    try:

        with sr.Microphone(device_index=1) as source:

            print("Calibrating microphone...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            recognizer.energy_threshold = max(
                recognizer.energy_threshold,
                300
            )

            print(
                f"Microphone calibrated. "
                f"Energy threshold: "
                f"{recognizer.energy_threshold:.0f}"
            )

    except Exception as e:

        print(
            "Microphone calibration error:",
            e
        )


def listen():

    try:

        with sr.Microphone(device_index=1) as source:

            print("Listening...")

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=6
            )

        print("Processing voice...")

        try:

            text = recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print("You:", text)

            return text.lower().strip()

        except sr.UnknownValueError:

            print("I couldn't understand.")

            return ""

        except sr.RequestError as e:

            print(
                "Speech recognition service unavailable:",
                e
            )

            return ""

    except sr.WaitTimeoutError:

        print("No speech detected.")

        return ""

    except Exception as e:

        print(
            "Listening error:",
            
        )

        return ""