import sys
import time
import threading

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication

from hud.hud import JarvisHUD
from wake_up import wait_for_clap

from commands.system import execute
from speech.listen import calibrate_microphone, listen
from speech.tts import speak


class JarvisWorker(QObject):

    state_changed = Signal(str)

    def run(self):

        print("JARVIS STARTED")

        # -------------------------------------------------
        # MICROPHONE CALIBRATION
        # -------------------------------------------------

        try:
            calibrate_microphone()
        except Exception as e:
            print("Microphone calibration error:", e)

        # -------------------------------------------------
        # MAIN JARVIS LOOP
        # -------------------------------------------------

        while True:

            try:

                # -----------------------------------------
                # STANDBY
                # -----------------------------------------

                self.state_changed.emit("STANDBY")

                print()
                print("JARVIS is sleeping.")
                print("Waiting for double clap...")

                # -----------------------------------------
                # WAIT FOR DOUBLE CLAP
                # -----------------------------------------

                result = wait_for_clap()

                if result is False:
                    print("Clap detector failed.")
                    time.sleep(1)
                    continue

                # -----------------------------------------
                # AWAKENING
                # -----------------------------------------

                self.state_changed.emit("AWAKENING")

                print("JARVIS waking up...")

                speak("I'm listening.")

                # -----------------------------------------
                # CONVERSATION LOOP
                # -----------------------------------------

                while True:

                    # -------------------------------------
                    # LISTENING
                    # -------------------------------------

                    self.state_changed.emit("LISTENING")

                    print("Listening...")

                    command = listen()

                    # -------------------------------------
                    # NOTHING HEARD
                    # -------------------------------------

                    if not command:

                        self.state_changed.emit("SPEAKING")

                        print("I couldn't understand.")

                        speak(
                            "I did not quite catch that."
                        )

                        continue

                    command = command.lower().strip()

                    print("You:", command)

                    # -------------------------------------
                    # SLEEP COMMANDS
                    # -------------------------------------

                    sleep_commands = [
                        "go to sleep",
                        "sleep",
                        "stop",
                        "bye",
                        "goodbye",
                        "exit",
                        "quit"
                    ]

                    if command in sleep_commands:

                        self.state_changed.emit("SPEAKING")

                        print(
                            "JARVIS: Going to sleep. "
                            "Clap when you need me."
                        )

                        speak(
                            "Going to sleep. "
                            "Clap when you need me."
                        )

                        break

                    # -------------------------------------
                    # PROCESSING
                    # -------------------------------------

                    self.state_changed.emit("PROCESSING")

                    print("Processing...")

                    try:

                        response = execute(command)

                    except Exception as e:

                        print(
                            "Command execution error:",
                            e
                        )

                        response = (
                            "Sorry, something went wrong "
                            "while processing that command."
                        )

                    # -------------------------------------
                    # SPEAKING
                    # -------------------------------------

                    self.state_changed.emit("SPEAKING")

                    if response:

                        print(
                            "JARVIS:",
                            response
                        )

                        speak(response)

                    else:

                        response = (
                            "Sorry, I don't know "
                            "that command yet."
                        )

                        print(
                            "JARVIS:",
                            response
                        )

                        speak(response)

                    # -------------------------------------
                    # SMALL PAUSE
                    # -------------------------------------

                    time.sleep(0.2)

            except KeyboardInterrupt:

                print()
                print("JARVIS stopped.")

                self.state_changed.emit("STANDBY")

                break

            except Exception as e:

                print()
                print("JARVIS ERROR:", e)

                self.state_changed.emit("STANDBY")

                time.sleep(1)


class JarvisApp:

    def __init__(self):

        # -------------------------------------------------
        # QT APPLICATION
        # -------------------------------------------------

        self.app = QApplication(sys.argv)

        # -------------------------------------------------
        # HUD
        # -------------------------------------------------

        self.hud = JarvisHUD()

        self.hud.show()

        # -------------------------------------------------
        # JARVIS WORKER
        # -------------------------------------------------

        self.worker = JarvisWorker()

        self.worker.state_changed.connect(
            self.hud.set_state
        )

        # -------------------------------------------------
        # PYTHON BACKGROUND THREAD
        # -------------------------------------------------

        self.jarvis_thread = threading.Thread(
            target=self.worker.run,
            daemon=True
        )

        self.jarvis_thread.start()

    def run(self):

        return self.app.exec()


# =========================================================
# START JARVIS
# =========================================================

if __name__ == "__main__":

    jarvis = JarvisApp()

    sys.exit(
        jarvis.run()
    )
 