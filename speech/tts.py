import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 170)

voices = engine.getProperty("voices")

# Female voice (if available)
if len(voices) > 1:
    engine.setProperty("voice", voices[1].id)


def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()