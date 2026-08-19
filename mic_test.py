import speech_recognition as sr

recognizer = sr.Recognizer()

print("Say something...")

with sr.Microphone() as source:
    audio = recognizer.listen(source)

print("I heard you!")