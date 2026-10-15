import pyttsx3


def speak(text):
    print("JARVIS:", text)

    try:
        engine = pyttsx3.init()

        engine.setProperty("rate", 170)

        voices = engine.getProperty("voices")

        if len(voices) > 0:
            engine.setProperty("voice", voices[0].id)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("TTS Error:", e)