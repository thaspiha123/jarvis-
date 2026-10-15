
import pyttsx3

engine = pyttsx3.init()

# Select Microsoft David male voice
voices = engine.getProperty("voices")

for voice in voices:
    if "david" in voice.name.lower():
        engine.setProperty("voice", voice.id)
        break

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)


def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    speak("Hello! I am Jarvis. How can I help you today?")
