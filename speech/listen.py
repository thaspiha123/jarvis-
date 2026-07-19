import speech_recognition as sr

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8


def listen():
    with sr.Microphone() as source:

        print("🎤 Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=0.2)

        try:
            audio = recognizer.listen(
                source,
                timeout=3,
                phrase_time_limit=3
            )

            text = recognizer.recognize_google(audio)

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